from django.core.management.base import BaseCommand
#import rpa as r
from datetime import datetime, date

from urllib.parse import urljoin
from urllib.error import HTTPError
from urllib.error import URLError
import urllib.parse
import urllib

import time 

import requests 
import pandas as pd
import os
from csv import writer
from django.conf import settings

#get url from aimf website
from urllib.request import urlopen
from bs4 import BeautifulSoup

from commodity.models import CommodityName, Commodity
from task.models import WebScrapTask


class Command(BaseCommand):
    help = "collect jobs"
    # define logic of command
    def handle(self, *args, **options): 
        try:
            currency_html = urlopen('https://in.finance.yahoo.com/quote/INR=X/')
            currency_soup = BeautifulSoup(currency_html.read(), 'html.parser')
            find_div = currency_soup.find('div', {'data-reactid': '31'})
            find_span = find_div.find('span', {'class': 'Trsdu(0.3s)'})
            find_currency = find_span.text
            currency_value = None
            if find_currency is not None:
                currency_value = float(find_currency)
            
            # print(abc)
            gold_html = urlopen('https://finance.yahoo.com/quote/GC=F/')
            gold_soup = BeautifulSoup(gold_html.read(), 'html.parser')
            gold_find_div = gold_soup.find('div', {'data-reactid': '31'})
            gold_find_span = gold_find_div.find('span', {'class': 'Trsdu(0.3s)'})
            gold_value = gold_find_span.text
            gold_final_value = None
            if gold_value is not None:
                gold_final_value = float(gold_value.replace(',', ''))

            # get system current date
            now = datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            close_value = None
            if gold_final_value is not None and currency_value is not None:
                close_value = gold_final_value * currency_value

            if close_value is not None:
                #GET gold obj
                gold_obj = CommodityName.objects.filter(name="gold")
                #check current date data exist or not 
                if gold_obj.first():
                    gold_data_obj = Commodity.objects.filter(name=gold_obj.first(), timestamp=current_date)
                    # save gold data in db
                    if gold_data_obj.count() == 1:
                        pass
                        print("{} gold data is already exist!!!".format(current_date)) 
                    else :
                        gold_data = Commodity.objects.create(
                                name=gold_obj.first(),
                                timestamp=current_date,
                                open = 0.0,
                                high = 0.0,
                                low = 0.0,
                                close = close_value,
                                volume = 0.0
                            )
                        print("Gold data object created!!!")
                        task_obj = WebScrapTask.objects.create(name="Gold", timestamp=current_date, status="Pass")
            else:
                print("Not getting live data value - Gold data not created!!!")
                task_obj = WebScrapTask.objects.create(name="Gold", timestamp=current_date, status="Fail")




        except HTTPError as e:
            print("HTTP Error :", e)
            task_obj = WebScrapTask.objects.create(name="Gold", timestamp=current_date, status="Fail")
            
        except URLError as e:
            print("Website can't be reached")
            task_obj = WebScrapTask.objects.create(name="Gold", timestamp=current_date, status="Fail")

        
        



