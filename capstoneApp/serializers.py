from rest_framework import serializers
from .models import userinfo, item_list


class UserinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = userinfo
        fields = ['username', 'userid', 'password']


class Item_ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = item_list
        fields = ['item_name']