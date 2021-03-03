from django.contrib import admin

# Register your models here.
from .models import WebScrapTask

class WebScrapTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'timestamp', 'status')


admin.site.register(WebScrapTask, WebScrapTaskAdmin)