from rest_framework import serializers

from scooters.models import Scooter


class ScooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scooter
        fields = [
            'id',
            'brand',
            'scooter_model',
            'capacity',
            'year',
            'registration_number',
            'image',
            'available',
            'daily_price',
            'weekly_price',
            'monthly_price',
            'deposit_amount',
        ]
