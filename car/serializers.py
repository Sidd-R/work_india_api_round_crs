from rest_framework import serializers
from .models import Car, Transaction


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
        

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'