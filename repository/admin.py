from django.contrib import admin

from .models import Repository, Issue, Label, AsyncTask

# Register your models here.
admin.site.register(Repository)
admin.site.register(Issue)
admin.site.register(Label)
admin.site.register(AsyncTask)