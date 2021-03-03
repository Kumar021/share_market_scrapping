from rest_framework import serializers

from .models import ShareName, PrimaryShareData



class ShareNameSerializer(serializers.ModelSerializer): 
    class Meta:
        model = ShareName
        fields = ('id', 'name',)  


class ShareMarketSerializer(serializers.HyperlinkedModelSerializer):
    timestamp = serializers.DateField(format="%Y-%m-%d")
    #share_name = serializers.RelatedField(many=True, read_only=True)
    share_name = ShareNameSerializer(read_only=True)
    class Meta:
        model = PrimaryShareData
        fields = ('id', 'share_name', 'timestamp', 'open', 'high', 'low', 'close', 'turnover') 




















