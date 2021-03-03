from django.urls import include, path
from . import views 
from commodity.views import goldWithEquityTrading
from commodity import views as commodity_views
from trading import api_views 

app_name = 'trading'

urlpatterns = [

    #path("test/", views.testView, name="test"),
]


