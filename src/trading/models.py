from django.db import models
from django.utils import timezone 
from django.db.models.signals import post_save
from datetime import datetime, timedelta, date
#import datetime
from trading.utility import send_remider_mail

class ShareName(models.Model):
    name = models.CharField(max_length=200, help_text = "Company Name", blank=True, null=True) 
    symbol = models.CharField(max_length=200, help_text = "company symbol", blank=True, null=True)
    code = models.CharField(max_length=200, help_text = "company code", default="INE228A01035")

    def __str__(self):
        return self.name  
 

class PrimaryShareData(models.Model):
    share_name =  models.ForeignKey(ShareName, related_name='primary_share_data',blank=True, null=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=200, help_text = "company code", default="INE228A01035")
    timestamp = models.DateField(max_length=100) 
    open = models.CharField(max_length=200, blank=True, null=True)
    high = models.CharField(max_length=200, blank=True, null=True)
    low = models.CharField(max_length=200, blank=True, null=True) 
    close = models.CharField(max_length=200, blank=True, null=True)
    #number of share traded ie # volume : turnover(rs)
    turnover = models.CharField(max_length=200, blank=True, null=True) 
    attribute1 = models.CharField(max_length=100, blank=True, null=True)
    attribute2 = models.CharField(max_length=100, blank=True, null=True)
    
    
    class Meta:
        indexes = [
                models.Index(fields=['code']),
                models.Index(fields=['code'], name='primary_code_name_idx'),
            ] 

    def __str__(self):
        return str(self.close) 


















