from rest_framework import serializers

from .models import Repository


class StringRelatedField(serializers.ListField):
    label = serializers.CharField(max_length=25)

class RepositorySerializer(serializers.Serializer):

    url = serializers.URLField()
    github_token = serializers.CharField(max_length=45)

    must_have_labels = StringRelatedField()
    must_not_have_labels = StringRelatedField()
