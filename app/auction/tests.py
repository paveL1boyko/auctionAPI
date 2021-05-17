from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from auction.models import Lot, Animal, Bet
from auction.serializer import LotSerializer, BetSerializer, AnimalSerializer
from authenticate.models import CustomUser


class UserLotAPIModelViewSetTest(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = CustomUser.objects.create_user(password='test', username='admin')
        self.client.force_authenticate(user=self.user)
        cat = Animal.objects.create(user=self.user, type=Animal.AnimalType.CAT, alias='tom', breed='tabby')
        self.lot = Lot.objects.create(animal=cat, user=self.user, price=200)

    def test_get_all_lot(self):
        response = self.client.get(reverse('auction:user_lot-list'))
        lots = Lot.objects.filter(user=self.user)
        serializer = LotSerializer(lots, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lot_by_id(self):
        response = self.client.get(reverse('auction:user_lot-detail', kwargs={'pk': self.lot.pk}))
        lot = Lot.objects.get(user=self.user, pk=self.lot.pk)
        serializer = LotSerializer(lot, many=False)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_lot(self):
        response = self.client.post(reverse('auction:user_lot-list'),
                                    {'price': 200, 'animal': 1},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_lot(self):
        response = self.client.delete(reverse('auction:user_lot-detail', kwargs={'pk': self.lot.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LotReadOnlyModelViewSetTests(APITestCase):
    client = APIClient()

    def setUp(self):
        self.owner = CustomUser.objects.create_user(password='test', username='owner')
        self.user = CustomUser.objects.create_user(password='test', username='user1')
        self.client.force_authenticate(user=self.user)
        cat = Animal.objects.create(user=self.user, type=Animal.AnimalType.CAT, alias='tom', breed='tabby')
        hedgehog = Animal.objects.create(user=self.user, type=Animal.AnimalType.HEDGEHOG, alias='jon', breed='barbed')
        self.lot1 = Lot.objects.create(animal=cat, user=self.user, price=200)
        self.lot2 = Lot.objects.create(animal=hedgehog, user=self.user, price=100)

    def test_get_all_lot_for_user(self):
        response = self.client.get(reverse('auction:lot-list'))
        lots = Lot.objects.all()
        serializer = LotSerializer(lots, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lot_by_id(self):
        response = self.client.get(reverse('auction:lot-detail', kwargs={'pk': self.lot2.pk}))
        lot = Lot.objects.get(pk=self.lot2.pk)
        serializer = LotSerializer(lot, many=False)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BetAPIModelViewSetTest(APITestCase):
    client = APIClient()

    def setUp(self):
        owner = CustomUser.objects.create_user(password='test', username='admin')
        self.user = CustomUser.objects.create_user(password='test', username='user')
        self.client.force_authenticate(user=self.user)
        cat = Animal.objects.create(user=owner, type=Animal.AnimalType.CAT, alias='tom', breed='tabby')
        hedgehog = Animal.objects.create(user=owner, type=Animal.AnimalType.HEDGEHOG, alias='jon', breed='barbed')
        self.lot1 = Lot.objects.create(animal=cat, user=owner, price=200)
        self.lot2 = Lot.objects.create(animal=hedgehog, user=owner, price=100)
        self.bet1 = Bet.objects.create(lot=self.lot1, user=self.user, bet_value=300)
        self.bet2 = Bet.objects.create(lot=self.lot2, user=self.user, bet_value=150)

    def test_get_all_bet(self):
        response = self.client.get(reverse('auction:bet-list'))
        lots = Bet.objects.filter(user=self.user)
        serializer = BetSerializer(lots, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_bet_by_id(self):
        response = self.client.get(reverse('auction:bet-detail', kwargs={'pk': self.bet2.pk}))
        lot = Bet.objects.get(user=self.user, pk=self.bet2.pk)
        serializer = BetSerializer(lot)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_bet(self):
        response = self.client.post(reverse('auction:bet-list'),
                                    {'lot': self.lot2.pk, 'bet_value': 200},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_bet(self):
        response = self.client.delete(reverse('auction:bet-detail', kwargs={'pk': self.lot1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TypeAnimalAPIModelViewSetTest(APITestCase):
    client = APIClient()
    HEDGEHOGS = 'hedgehogs'
    CATS = 'cats'

    def setUp(self):
        self.user = CustomUser.objects.create_user(password='test', username='admin')
        self.client.force_authenticate(user=self.user)
        self.cat = Animal.objects.create(user=self.user, type=Animal.AnimalType.CAT,
                                         alias='tom', breed='tabby')
        self.hedgehog = Animal.objects.create(user=self.user, type=Animal.AnimalType.HEDGEHOG,
                                              alias='jon', breed='barbed')

    def test_get_all_user_cats(self):
        response = self.client.get(reverse('auction:animals_type-list', kwargs={'type': self.CATS}))
        cats = Animal.objects.filter(user=self.user, type=Animal.AnimalType.CAT)
        serializer = AnimalSerializer(cats, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_hedgehog_by_id(self):
        response = self.client.get(reverse('auction:animals_type-detail',
                                           kwargs={'type': self.HEDGEHOGS, 'pk': self.hedgehog.pk}))
        lot = Animal.objects.get(user=self.user, pk=self.hedgehog.pk)
        serializer = AnimalSerializer(lot)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_cat(self):
        response = self.client.post(reverse('auction:animals_type-list', kwargs={'type': self.CATS}),
                                    {'alias': 'johan', 'breed': 'clever'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_hedgehog(self):
        response = self.client.delete(reverse('auction:animals_type-detail',
                                              kwargs={'type': self.HEDGEHOGS, 'pk': self.hedgehog.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UserBetListAPIViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        self.owner = CustomUser.objects.create_user(password='test', username='admin')
        self.client.force_authenticate(user=self.owner)
        self.user1 = CustomUser.objects.create_user(password='test', username='user1')
        self.user2 = CustomUser.objects.create_user(password='test', username='user2')
        cat = Animal.objects.create(user=self.owner, type=Animal.AnimalType.CAT, alias='tom', breed='tabby')
        self.lot = Lot.objects.create(animal=cat, user=self.owner, price=200)
        self.bet1 = Bet.objects.create(lot=self.lot, user=self.user1, bet_value=300)
        self.bet2 = Bet.objects.create(lot=self.lot, user=self.user2, bet_value=450)

    def test_get_all_bets_for_id_lot(self):
        response = self.client.get(reverse('auction:chose_bet', kwargs={'lot': self.lot.pk}))
        lots = Bet.objects.filter(lot=self.lot.pk)
        serializer = BetSerializer(lots, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AnimalListAPIViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = CustomUser.objects.create_user(password='test', username='admin')
        self.client.force_authenticate(user=self.user)
        Animal.objects.create(user=self.user, type=Animal.AnimalType.CAT, alias='tom', breed='tabby')
        Animal.objects.create(user=self.user, type=Animal.AnimalType.HEDGEHOG, alias='jon', breed='barbed')

    def get_all_user_animal(self):
        request = self.client.get(reverse('auction:animals'))
        animals = Animal.objects.filter(user=self.user)
        serialize = AnimalSerializer(animals, many=True)
        self.assertEqual(serialize.data, request.data)
