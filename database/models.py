from django.db import models
from django.contrib import admin
from django.utils import timezone


class PesticidalProteinDatabase(models.Model):
    """
    """
    name = models.CharField(max_length=15, blank=True, null=False)
    oldname = models.CharField(max_length=15, blank=True, null=False)
    accession = models.CharField(max_length=25, blank=True, null=False)
    year = models.CharField(max_length=5, blank=True, null=False)
    fastasequence = models.TextField(blank=True, null=False)

    class Meta:
        ordering = ('name',)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name


class PesticidalProteinDatabaseAdmin(admin.ModelAdmin):
    """
    """
    search_fields = ('name', 'oldname', 'accession', 'year')


class Description(models.Model):
    """
    """
    name = models.CharField(max_length=7)
    description = models.TextField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class UserUploadData(models.Model):
    """
    """
    session_key = models.CharField(max_length=40, default=None)
    name = models.CharField(max_length=15, blank=True, null=False)
    fastasequence = models.TextField(blank=True, null=False)
