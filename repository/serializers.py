from rest_framework import serializers
from rest_framework.serializers import StringRelatedField

from .models import Repository

class StringRelatedField(serializers.ListField):
    label = serializers.CharField(max_length=55)



class RepositorySerializer(serializers.Serializer):

    url = serializers.URLField()
    # github_token = serializers.CharField(max_length=45)
    github_token = StringRelatedField()

    must_have_labels = StringRelatedField()
    must_not_have_labels = StringRelatedField()
