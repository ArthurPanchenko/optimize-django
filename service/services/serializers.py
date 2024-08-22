from rest_framework import serializers

from .models import Subscription, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = (
            '__all__'
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')
    plan = PlanSerializer()
    price = serializers.SerializerMethodField()

    def get_price(self, instance):
        return instance.price

    class Meta:
        model = Subscription
        fields = (
            'id',
            'client',
            'client_name',
            'email',
            'plan',
            'plan_id',
            'service',
            'price'
        )