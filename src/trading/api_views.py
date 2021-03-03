import json
from rest_framework import viewsets
from . import models
from . import serializers 
from rest_framework.permissions import IsAuthenticated 
from rest_framework import permissions, generics, mixins 
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from datetime import datetime



class ShareNameList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ShareNameSerializer

    def get_queryset(self):
        queryset = models.ShareName.objects.all()
        share_name = self.request.query_params.get('name', None)

        if share_name:
            queryset = models.ShareName.objects.filter(name=share_name)
        return queryset 



class ShareNameCreate(APIView):
    """
    List all country, or create a new country.
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        queryset = models.ShareName.objects.all()
        serializer = serializers.ShareNameSerializer(queryset, many=True)
        return Response(serializer.data) 

    def post(self, request, format=None):
        serializer = serializers.ShareNameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShareNameRetrieve(APIView):
    """
    Retrieve, update or delete a country instance.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return models.ShareName.objects.get(pk=pk)
        except models.ShareName.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        share_name = self.get_object(pk)
        serializer = serializers.ShareNameSerializer(share_name)
        return Response(serializer.data) 

    def put(self, request, pk, format=None):
        share_name = self.get_object(pk)
        serializer = serializers.ShareNameSerializer(share_name, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        share_name = self.get_object(pk)
        share_name.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ShareMarketDataDetail(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ShareMarketSerializer

    def get_queryset(self):
        queryset = models.PrimaryShareData.objects.all().order_by('timestamp')
        share_name = self.request.query_params.get('id', None)
        from_date = self.request.query_params.get('from_date', None)
        to_date = self.request.query_params.get('to_date', None)

        if from_date and to_date:
            queryset = models.PrimaryShareData.objects.filter(share_name=share_name, timestamp__range=[from_date, to_date]).order_by('timestamp')
        elif share_name and from_date is None:
            queryset = models.PrimaryShareData.objects.filter(share_name=share_name).order_by('timestamp')
        return queryset



class ShareMarketCreate(APIView):
    """
    List all country, or create a new country.
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        queryset = models.PrimaryShareData.objects.all()
        serializer = serializers.ShareMarketSerializer(queryset, many=True)
        return Response(serializer.data) 

    def post(self, request, format=None):
        id_ = request.data["share_name"]
        share_name_instance = models.ShareName.objects.filter(id=id_)
        share_name = share_name_instance.first()

        if not share_name:
            return Response({"detail": "indices_name object not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        primary_share_obj = models.PrimaryShareData.objects.create(
                share_name = share_name,
                timestamp = request.data["timestamp"],
                open = request.data["open"],
                high = request.data["high"],
                low  = request.data["low"],
                close = request.data["close"],
                turnover = request.data["turnover"] 
            )
        serializer = serializers.ShareMarketSerializer(primary_share_obj)
        #serializer = serializers.ShareMarketSerializer(data=request.data)
        if serializer:
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShareMarketRetrieve(APIView):
    """
    Retrieve, update or delete a country instance.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return models.PrimaryShareData.objects.get(pk=pk)
        except models.PrimaryShareData.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        share_name = self.get_object(pk)
        serializer = serializers.ShareMarketSerializer(share_name)
        return Response(serializer.data) 

   
    def delete(self, request, pk, format=None):
        share_name = self.get_object(pk)
        share_name.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





















