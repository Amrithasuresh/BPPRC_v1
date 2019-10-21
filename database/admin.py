from django.contrib import admin
from .models import PesticidalProteinDatabase, \
    Description


class PesticidalProteinDatabaseAdmin(admin.ModelAdmin):
    search_fields = ('name', 'oldname', 'accession','year')
    fields = ('name', 'oldname', 'accession','year')
    list_display = ('name','oldname', 'accession','year',)
    ordering = ('name',)

class DescriptionAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description')
    fields = ('name', 'description')
    list_display = ('name', 'description')
    ordering = ('name',)


admin.site.register(PesticidalProteinDatabase, PesticidalProteinDatabaseAdmin)
admin.site.register(Description, DescriptionAdmin)
