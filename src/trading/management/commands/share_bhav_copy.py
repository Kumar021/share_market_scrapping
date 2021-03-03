
from django.core.management.base import BaseCommand
import rpa as r
from datetime import date
from datetime import datetime
from urllib.parse import urljoin
import pandas as pd 

from urllib.parse import urljoin
from urllib.error import HTTPError
from urllib.error import URLError
import urllib.parse
import urllib

import time
#import datetime
from datetime import datetime 

import requests 
import pandas as pd
import os
from csv import writer
from django.conf import settings
from koolbuch.settings import base as BASE_SETTINGS
#get url from aimf website
from urllib.request import urlopen
from bs4 import BeautifulSoup

from finance.models import ShareName, PrimaryShareData, SecondaryShareData
from task.models import WebScrapTask
from trading.utility import send_remider_mail

def getMonth(value):

    mlist = {
        '01': 'JAN',
        '02': 'FEB',
        '03': 'MAR',
        '04': 'APR',
        '05': 'MAY',
        '06': 'JUN',
        '07': 'JUL',
        '08': 'AUG',
        '09': 'SEP',
        '10': 'OCT',
        '11': 'NOV',
        '12': 'DEC' 
    }
    month = ''

    if value in mlist:
        return mlist[value]

    return month

class Command(BaseCommand):
    help = "collect jobs"
    # define logic of command
    def handle(self, *args, **options): 

        now = datetime.now() 
        year = now.strftime("%Y")
        month = now.strftime("%m")
        get_month = getMonth(str(month))
        day = now.strftime("%d")

        zip_file_name = 'cm' + day + get_month + year + 'bhav'+ '.csv' + '.zip' # same as file name
        csv_file_name = 'cm' + day + get_month + year + 'bhav'+ '.csv'

        try:
            base_url = 'https://archives.nseindia.com/content/historical/EQUITIES/'
            dynamic_url = year + '/' + get_month + '/' + zip_file_name
            url_ = urljoin(base_url, dynamic_url)
            #test_url = "https://archives.nseindia.com/content/historical/EQUITIES/2021/FEB/cm11FEB2021bhav.csv.zip"
            
            os.chdir(BASE_SETTINGS.SHARE_DATA)
            if url_:
                r.init()
                r.download(test_url)
                r.unzip(zip_file_name)
                # r.close()

                #Read csv file
                if os.path.exists(csv_file_name):
                    df = pd.read_csv(csv_file_name) #csv_file_name)
                    print("Read csv file - pandas")
                    if len(df) > 0:
                        for i, j in df.iterrows():
                            date_value = j[10]
                            current_date = datetime.strptime(date_value, "%d-%b-%Y")
                            data_format = current_date.strftime("%Y-%m-%d")
                            
                            timestamp = data_format
                            open_ = j[2]
                            close = j[5]
                            turnover = j[9]
                            high = j[3]
                            low = j[4]
                            f_close = str(close).replace(",", "")
                            f_turnover = str(turnover).replace(",", "")
                            f_open = str(open_).replace(",", "")
                            f_high = str(high).replace(",", "")
                            f_low = str(low).replace(",", "")

                            if f_close is None:
                                f_close = 0.00

                            if f_turnover is None:
                                f_turnover = 0.00 

                            if f_open is None:
                                f_open = 0.00 

                            if f_high is None:
                                f_high = 0.00

                            share_name_qs = ShareName.objects.filter(
                                    symbol = j[0],
                                    # code = j[12]
                                )
                            if share_name_qs.count() == 1:
                                primary_qs = PrimaryShareData.objects.filter(timestamp=timestamp, share_name=share_name_qs.first())  
                                if primary_qs.count() == 1:
                                    print("Updated Primary share data.")
                                    primary_qs.update(
                                        share_name = share_name_qs.first(),
                                        code = j[12],
                                        open = f_open,
                                        high = f_high,
                                        low = f_low,
                                        close = f_close,
                                        turnover = f_turnover,
                                        timestamp = timestamp
                                    )
                                    secondary = SecondaryShareData.objects.create(
                                        primary_share = primary_qs.first(),
                                        code = j[12],
                                        prev_close = j[7],
                                        last = j[6],
                                        total_traded_quantity = j[11],
                                        number_of_trade = j[8],
                                        timestamp = timestamp,
                                    )
                                    task_obj = WebScrapTask.objects.create(name="Bhav copy", timestamp=current_date, status="Pass")
                                    #Send mail alert 
                                    send_mail = send_remider_mail(current_date, "Share Bhav Copy Scraping Is Updated!!")

                                else:
                                    print("Created Primary share data")
                                    primary_obj = PrimaryShareData.objects.create(
                                        share_name = share_name_qs.first(),
                                        code = j[12],
                                        open = f_open,
                                        high = f_high,
                                        low = f_low,
                                        close = f_close,
                                        turnover = f_turnover,
                                        timestamp = timestamp,
                                    )
                                    secondary = SecondaryShareData.objects.create(
                                        primary_share = primary_obj,
                                        code = j[12],
                                        prev_close = j[7],
                                        last = j[6],
                                        total_traded_quantity = j[11],
                                        number_of_trade = j[8],
                                        timestamp = timestamp,
                                    )
                                    task_obj = WebScrapTask.objects.create(name="Bhav copy", timestamp=current_date, status="Pass")
                                    #Send mail alert 
                                    send_mail = send_remider_mail(current_date, "Share Bhav Copy Scraping Is Created!!")

                            else:
                                print("Pass - Now new entry ShareName and PrimaryShareData")
                                # share_obj = ShareName.objects.create(
                                #     name = j[0],
                                #     symbol = j[0],
                                #     code = j[12] 
                                # )
                                # print("Created Primary share data")
                                # primary_obj = PrimaryShareData.objects.create(
                                #     share_name = share_obj,
                                #     code = j[12],
                                #     open = j[2],
                                #     high = j[3],
                                #     low = j[4],
                                #     close = j[5],
                                #     turnover = j[9],
                                #     timestamp = timestamp,
                                # )
                                # secondary = SecondaryShareData.objects.create(
                                #     primary_share = primary_obj,
                                #     code = j[12],
                                #     prev_close = j[7],
                                #     last = j[6],
                                #     total_traded_quantity = j[11],
                                #     number_of_trade = j[8],
                                #     timestamp = timestamp,
                                # )  
                        print('Share Market Data Bhav copy completed')
                        r.close() 
                else:
                    print("Unzip file name not found - Bhav copy not scrap!!")
                    #Send mail alert 
                    send_mail = send_remider_mail(current_date, "Share Bhav Copy Scraping Is Fail!!")

        except HTTPError as e:
            print("HTTP Error :", e)
            task_obj = WebScrapTask.objects.create(name="Bhav copy", timestamp=current_date, status="Fail")
            #Send mail alert 
            send_mail = send_remider_mail(current_date, "Share Bhav Copy Scraping Is Fail!!")
        except URLError as e:
            print("Website can't be reached")
            task_obj = WebScrapTask.objects.create(name="Bhav copy", timestamp=current_date, status="Fail")
            #Send mail alert 
            send_mail = send_remider_mail(current_date, "Share Bhav Copy Scraping Is Fail!!")



