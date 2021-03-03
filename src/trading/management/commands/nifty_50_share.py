from django.core.management.base import BaseCommand
import rpa as r
from datetime import date
from datetime import datetime
from urllib.parse import urljoin

from urllib.parse import urljoin
from urllib.error import HTTPError
from urllib.error import URLError
import urllib.parse
import urllib

import time
#import datetime
from datetime import datetime 

import requests 
import os
from csv import writer
from django.conf import settings

#get url from aimf website
from urllib.request import urlopen
from bs4 import BeautifulSoup

from trading.models import ShareName, PrimaryShareData, SecondaryShareData
from task.models import WebScrapTask
from trading.utility import send_remider_mail

def getShareCode(key):

    share_name_dict = {
        'Adani Ports': 'ADANIPORTS',
        'Asian Paints': 'ASIANPAINT',
        'Axis Bank': 'AXISBANK',
        'Bajaj Auto': 'BAJAJ-AUTO',
        'Bajaj Finance': 'BAJFINANCE',
        'Bajaj Finserv': 'BAJAJFINSV',
        'Bharti Airtel': 'BHARTIARTL',
        'BPCL': 'BPCL',
        'Britannia': 'BRITANNIA',
        'Cipla': 'CIPLA',
        'Coal India': 'COALINDIA',
        'Divis Labs': 'DIVISLAB',
        'Dr Reddys Labs': 'DRREDDY',
        'Eicher Motors': 'EICHERMOT',
        'GAIL': 'GAIL',
        'Grasim': 'GRASIM',
        'HCL Tech': 'HCLTECH',
        'HDFC': 'HDFC',
        'HDFC Bank': 'HDFCBANK',
        'HDFC Life': 'HDFCLIFE',
        'Hero Motocorp': 'HEROMOTOCO',
        'Hindalco': 'HINDALCO',
        'HUL': 'HINDUNILVR', #not
        'ICICI Bank': 'ICICIBANK',
        'IndusInd Bank': 'INDUSINDBK',
        'Infosys': 'INFY',
        'IOC': 'IOC',
        'ITC': 'ITC',
        'JSW Steel': 'JSWSTEEL',
        'Kotak Mahindra': 'KOTAKBANK',
        'Larsen': 'LT',
        'M&M': 'M&M',
        'Maruti Suzuki': 'MARUTI',
        'Nestle': 'NESTLEIND',
        'NTPC': 'NTPC',
        'ONGC': 'ONGC',
        'Power Grid Corp': 'POWERGRID',
        'Reliance': 'RELIANCE',
        'SBI': 'SBIN',
        'SBI Life Insura': 'SBILIFE',
        'Shree Cements': 'SHREECEM',
        'Sun Pharma': 'SUNPHARMA',
        'Tata Motors': 'TATAMOTORS',
        'Tata Steel': 'TATASTEEL',
        'TCS': 'TCS',
        'Tech Mahindra': 'TECHM',
        'Titan Company': 'TITAN',
        'UltraTechCement': 'ULTRACEMCO',
        'UPL': 'UPL',
        'Wipro': 'WIPRO'
    }

    if key in share_name_dict:
        return key, share_name_dict[key] 
    return None, None


class Command(BaseCommand):
    help = "collect jobs"
    # define logic of command
    def handle(self, *args, **options): 

        now = datetime.now() 
        
        html = None
        try:
            # money https://www.moneycontrol.com/markets/indian-indices/top-nse-50-companies-list/9?classic=true
            html = urlopen('https://www.moneycontrol.com/markets/indian-indices/top-nse-50-companies-list/9?classic=true')
            soup = BeautifulSoup(html.read(), 'html.parser')
            table_ = soup.find('table', {'class': 'responsive'})

            data = []
            rows = table_.find_all('tr')
            for row in rows:
                if row is not None:
                    cols = row.find_all('td')
                    cols_ = [ele.text for ele in cols]
                    data.append([ele for ele in cols_ if ele])  

            #write data into
            current_date = now.strftime("%Y-%m-%d")
            if data is not None:
                for i in range(1, len(data)):
                    # store data without comma(,) - close and turnover
                    obj_name = data[i][0]
                    close = data[i][1]
                    turnover = data[i][3]
                    f_close = str(close).replace(",", "")
                    f_turnover = str(turnover).replace(",", "")
                    if obj_name is None:
                        f_close = 0.00
                        f_turnover = 0.00
                    get_share_name, get_share_code = getShareCode(obj_name)
                    if get_share_code is not None:
                        share_name_obj = ShareName.objects.filter(
                                    symbol = get_share_code
                                )

                        if get_share_code and share_name_obj.count() == 1:
                            primary_qs = PrimaryShareData.objects.filter(timestamp=current_date, share_name=share_name_obj.first())  
                            if primary_qs.count()== 1:
                                print("update - primary share data")
                                primary_qs.update(
                                    share_name = share_name_obj.first(),
                                    close = f_close,
                                    open = 0.0,
                                    high = 0.0,
                                    low = 0.0,
                                    turnover = f_turnover,
                                )
                                task_obj = WebScrapTask.objects.create(name="NIFTY 50 Share Scraping", timestamp=current_date, status="Pass")
                            else:
                                print("create - primary share data")
                                # primary = PrimaryShareData.objects.create(
                                #         share_name = share_name_obj.first(),
                                #         open = 0.0,
                                #         high = 0.0,
                                #         close = 0.0,
                                #         turnover = f_turnover,
                                #         timestamp = current_date,
                                #     )
                                task_obj = WebScrapTask.objects.create(name="NIFTY 50 Share Scraping", timestamp=current_date, status="Pass")
                                #Send mail alert 
                                send_mail = send_remider_mail(current_date, "NIFTY 50 Share Scraping")
                            
                        else:
                            print("Pass - Now new entry ShareName and PrimaryShareData")
                            # share_name_ = ShareName.objects.create(
                            #         name = get_share_name,
                            #         symbol = get_share_code
                            #     )
                            # primary = PrimaryShareData.objects.create(
                            #         share_name = share_name_.first(),
                            #         close = close,
                            #         turnover = turnover,
                            #         timestamp = current_date,
                            #     )
                    else:
                        print("Share name object not found!")
                        task_obj = WebScrapTask.objects.create(name="NIFTY 50 Share Scraping", timestamp=current_date, status="Fail")


        except HTTPError as e:
            print("HTTP Error :", e)
            task_obj = WebScrapTask.objects.create(name="NIFTY 50", timestamp=current_date, status="Fail")

        except URLError as e:
            print("Website can't be reached")
            task_obj = WebScrapTask.objects.create(name="NIFTY 50", timestamp=current_date, status="Fail")

        
        



