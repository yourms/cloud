from rest_framework import serializers

from android_rest.models import User, Product


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'email', 'phone', 'address', 'gno']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pno', 'id', 'main', 'sub1', 'sub2', 'specific', 'manufacture', 'name', 'quantitiy', 'nutrition',
                  'price', 'section', 'location', 'stock']
        
        
class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name']
