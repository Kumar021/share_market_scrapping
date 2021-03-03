
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .api import router
#api
from trading import api_views as trdaing_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/', include(router.urls)),

    path("api/v1/share-name/create/", trdaing_views.ShareNameCreate.as_view(), name="create"),
    path("api/v1/share-name/<int:pk>/retrieve/", trdaing_views.ShareNameRetrieve.as_view(), name="share-name-retrieve"),
    path('api/v1/share-name/', trdaing_views.ShareNameList.as_view(), name="share-name-list"),
    path('api/v1/share-market/create/', trdaing_views.ShareMarketCreate.as_view(), name="share-market-create"),
    path('api/v1/share-market/<int:pk>/retrieve/', trdaing_views.ShareMarketRetrieve.as_view(), name="share-market-retrieve"),
    path('api/v1/share-data/', trdaing_views.ShareMarketDataDetail.as_view(), name="share-market-detail"),
    path("trading/", include('trading.urls')),
   
]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
