# Create your views here.
from rest_framework import status
from rest_framework.exceptions import NotFound, APIException
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .mixin import AddUserInModelMixin
from .models import Lot, Bet, Animal
from .serializer import BetSerializer, LotSerializer, AnimalSerializer, LotCreateSerializer


class LotReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Lot.objects.all()
    serializer_class = LotSerializer


class UserBetListAPIView(ListAPIView):
    serializer_class = BetSerializer

    def get_queryset(self):
        return Bet.objects.filter(lot=self.kwargs['lot'])


class UserLotAPIModelViewSet(AddUserInModelMixin, ModelViewSet):
    serializer_class = LotSerializer
    queryset = Lot.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = LotCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BetAPIModelViewSet(AddUserInModelMixin, ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer


class AnimalListAPIView(ListAPIView):
    serializer_class = AnimalSerializer

    def get_queryset(self):
        return Animal.objects.filter(user=self.request.user)


class TypeAnimalAPIModelViewSet(ModelViewSet):
    serializer_class = AnimalSerializer

    def get_queryset(self):
        try:
            animal_id = Animal.AnimalType[self.kwargs['type'][:-1].upper()]
        except:
            raise NotFound
        return Animal.objects.filter(type=animal_id, user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        type=Animal.AnimalType[self.kwargs['type'][:-1].upper()])
