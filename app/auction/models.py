from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models

from authenticate.models import CustomUser


class Animal(models.Model):
    class AnimalType(models.IntegerChoices):
        CAT = 1,
        HEDGEHOG = 2
    type = models.SmallIntegerField(choices=AnimalType.choices)
    alias = models.CharField(max_length=50)
    breed = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='owner')

    def get_type_name(self):
        return ''.join([item[1] for item in self.AnimalType.choices if self.type == item[0]])

    def __str__(self):
        return f'{self.alias}, breed {self.breed}'


class Lot(models.Model):
    price = models.DecimalField(decimal_places=3, max_digits=10)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owner')
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)

    def __str__(self):
        return f'Owner {self.user}, {self.animal}'


class Bet(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bet_value = models.DecimalField(decimal_places=3, max_digits=10)

    def __str__(self):
        return f'{self.user} {self.lot}'
