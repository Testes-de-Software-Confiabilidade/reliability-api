from django.shortcuts import render
from django.db.utils import IntegrityError
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import mixins

import django_rq
from rq.registry import StartedJobRegistry

from .models import Repository, AsyncTask
from .serializers import RepositorySerializer
from .utils import process


def index(request):
    return render(request, 'repository/index.html', {})

class RepositoryViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

    # POST /repository
    def create(self, request, *args, **kwargs):
        serializer = RepositorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url                  = serializer.data.get('url', None)
        must_have_labels     = serializer.data.get('must_have_labels', None)
        must_not_have_labels = serializer.data.get('must_not_have_labels', None)
        github_token_list    = serializer.data.get('github_token', None)

        repositories = Repository.objects.filter(
            url=url, 
            must_have_labels = str(sorted(list(set(must_have_labels))))
        )

        if(repositories.exists()):

            tasks = AsyncTask.objects.filter(
                url=url, 
                must_have_labels=must_have_labels, 
                must_not_have_labels=must_not_have_labels
            )

            if(tasks.exists()):
                if(tasks.first().finished != True):
                    domain = get_current_site(request)
                    data = {
                        'message': ("The issues in this repository are being processed. "
                                    "Access the following link to follow the processing."),
                        'link': f'https://{domain}/processing?status_token={tasks.first().id}'
                    }
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    image_url = tasks.first().image
            else:
                image_url = process(repositories.first(), must_not_have_labels)
            
            data = {
                'message': ('The issues in this repository have been '
                            'completely processed. Access the '
                            'following link to see the '
                            'resulting image.'),
                'link': image_url,
            }

            return Response(data, status=status.HTTP_200_OK)

        Repository.objects.create(
            url=url,
            must_have_labels=str(sorted(list(set(must_have_labels))))
        )

        job = django_rq.enqueue(
            'repository.utils.process_async', 
            github_token_list,
            url,
            must_have_labels,
            must_not_have_labels
        )

        domain = get_current_site(request)

        data = {
            'message': ("The repository has been successfully added to "
                        "the processing queue! Follow the link to check "
                        "the processing status."
                       ),
            'link': f'https://{domain}/processing?status_token={job.get_id()}'
        }

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        

        
@api_view(['GET',])
def processing(request):
    status_token = request.query_params.get('status_token', None)

    if not status_token:
        return Response({'message': 'Token not defined'}, status=status.HTTP_400_BAD_REQUEST)

    ids = django_rq.get_queue('default').get_job_ids()
    
    for i, id in enumerate(ids):
        if id == status_token:
            registry = StartedJobRegistry('default', connection=django_rq.get_connection('default'))
            current = registry.get_job_ids()[0]
            return Response(
                {
                    'message': f'This repository is in the queue to be processed. Its processing queue number is {i+1}. In the meantime keep up with current processing.',
                    'link': f'https://{get_current_site(request)}/processing?status_token={current}'
                }, 
                status=status.HTTP_200_OK
            )
    
    tasks = AsyncTask.objects.filter(id=status_token)

    if tasks.exists() == False:
        return Response({'message': 'This token is not valid'}, status=status.HTTP_404_NOT_FOUND)
    
    task = tasks.first()

    # processing is completed
    if task.finished and task.failed==False:
        return Response({
                'message': ('The issues in this repository have been '
                            'completely processed. Access the '
                            'following link to see the '
                            'resulting image.'),
                'link': task.image
            }, 
            status=status.HTTP_200_OK
        )

    job = django_rq.get_queue('default').fetch_job(status_token)

    if task.finished and task.failed:
        job.meta.pop('ERRORS')

        return Response({
                'message': ('Something went wrong while processing this repository. '
                            'Check the error below '),
                'errors': job.meta
            }, 
            status=status.HTTP_409_CONFLICT
        )

    if task.finished == False:
        return Response({
                'message': 'This repository is still being processed. ',
                'status': job.meta
            }, 
            status=status.HTTP_200_OK
        )
