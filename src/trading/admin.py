from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from .models import ( 
                        ShareName, 
                        PrimaryShareData
 
                   )

@admin.register(ShareName)
class ShareNameAdmin(ImportExportModelAdmin):
    list_display = ('name','symbol', 'code')
    search_fields= ('name', 'symbol', 'code')   


@admin.register(PrimaryShareData)
class PrimaryShareDataAdmin(ImportExportModelAdmin):
    list_display = (
                     'id',
                    'share_name', 
                    'code',
                    'timestamp',
                    'open',
                    'high',
                    'low',
                    'close',
                    'turnover'
                ) 
    search_fields = ('id', 'share_name__name', 'code', 'timestamp')   


