from django.db import models


# Create your models here.
class Repository(models.Model):
    url = models.URLField()
    must_have_labels = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = 'Repositories'
        unique_together = ('url', 'must_have_labels')
    
    def __str__(self):
        return f'{self.url}, must_have_labels = {self.must_have_labels}'


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Issue(models.Model):
    repository = models.ForeignKey(
        Repository, 
        on_delete=models.CASCADE,
        related_name='issues',
    )

    closed_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField()
    
    html_url = models.URLField()
    api_url = models.URLField()

    is_closed = models.BooleanField()

    labels = models.ManyToManyField(Label)

    def __str__(self):
        return self.html_url


class AsyncTask(models.Model):

    id = models.CharField(unique=True, max_length=40, primary_key=True)
    image = models.URLField(null=True)

    url = models.URLField()
    must_have_labels = models.CharField(max_length=500)
    must_not_have_labels = models.CharField(max_length=500)

    failed = models.BooleanField()
    finished = models.BooleanField()

    # class Meta:
    #     unique_together = ('url', 'must_have_labels', 'must_not_have_labels')

    def __str__(self):
        return self.id
