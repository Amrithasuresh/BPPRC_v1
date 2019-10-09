from django.contrib import admin
from .models import PesticidalProteinDatabase, \
    PesticidalProteinDatabaseAdmin, Description


admin.site.register(PesticidalProteinDatabase,
                    PesticidalProteinDatabaseAdmin)


class PesticidalProteinDatabaseAdmin(admin.ModelAdmin):
    search_fields = ('name')

    def get_ordering(self, request):
        return('name')


@admin.register(Description)
class DefaultAdmin(admin.ModelAdmin):
    pass
