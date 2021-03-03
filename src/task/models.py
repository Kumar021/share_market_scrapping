# Create your models here.
from django.db import models

# Create your models here.
PASS_FAIL = (
        ('Pass', 'PASS'),
        ('Fail', 'FAIL'),
    )
SCRAPE_NAME = (
        ('Gold', 'GOLD'),
        ('NIFTY 50', 'NIFTY 50 Share Scraping'),
        ('Bhav copy', 'BHAV COPY'),
        ('Mitual', 'MITUAL')
    )
class WebScrapTask(models.Model):
    name 		= models.CharField(max_length=200, choices=SCRAPE_NAME, help_text = "Scraping name", blank=True, null=True) 
    timestamp 	= models.DateField(max_length=100) 
    status  	= models.CharField(max_length=200, choices=PASS_FAIL, help_text="Scrape status!!")

    def __str__(self):
    	return str(self.name)

