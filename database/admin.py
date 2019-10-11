from django.contrib import admin
from .models import PesticidalProteinDatabase, \
    Description


class PesticidalProteinDatabaseAdmin(admin.ModelAdmin):
    search_fields = ('name', 'oldname', 'accession','year')
    fields = ('name', 'oldname', 'accession','year')
    list_display = ('name','oldname', 'accession','year',)
    ordering = ('name',)


admin.site.register(PesticidalProteinDatabase, PesticidalProteinDatabaseAdmin)
