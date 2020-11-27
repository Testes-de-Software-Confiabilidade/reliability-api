from django.urls import path, include

from .views import RepositoryViewSet, index, processing

urlpatterns = [
    path('', index, name='home'),
    path('repository/', RepositoryViewSet.as_view({'post': 'create'}), name='repository_create'),
    path('processing/', processing, name='processing'),
    path('django-rq/', include('django_rq.urls'))
]