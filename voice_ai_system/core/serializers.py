from rest_framework import serializers
from .models import Customer, Loan, ConversationLog


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'


class ConversationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationLog
        fields = '__all__'