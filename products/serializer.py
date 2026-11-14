from rest_framework import serializers
from .models import products
from .models import Cetegory

class productsSerializer(serializers.ModelSerializer):
    class Meta:
        model = products
        fields = "__all__"

class CetegorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cetegory
        fields = "__all__"