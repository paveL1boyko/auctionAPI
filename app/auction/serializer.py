from rest_framework import serializers

from .models import Lot, Bet, Animal


class BetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        exclude = ['user']


class AnimalSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_name', read_only=True)

    class Meta:
        model = Animal
        fields = ['id', 'breed', 'alias', 'type']


class LotSerializer(serializers.ModelSerializer):
    animal_info = AnimalSerializer(source='animal', read_only=True)

    class Meta:
        model = Lot
        fields = ['id', 'price', 'animal_info']


class LotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = ['id', 'price', 'animal']


class BetSerializer(serializers.ModelSerializer):
    lot_info = LotSerializer(source='lot', read_only=True)

    class Meta:
        model = Bet
        fields = ['id', 'lot', 'bet_value', 'lot_info']
