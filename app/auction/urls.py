from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserLotAPIModelViewSet, LotReadOnlyModelViewSet, BetAPIModelViewSet, \
    TypeAnimalAPIModelViewSet, UserBetListAPIView, AnimalListAPIView

router = DefaultRouter()
router.register('user/lots', UserLotAPIModelViewSet, basename='user_lot')
router.register('lots', LotReadOnlyModelViewSet)
router.register('user/bets', BetAPIModelViewSet)
router.register(r'user/animals/(?P<type>[a-zA-Z]+)', TypeAnimalAPIModelViewSet, basename='animals_type')

app_name = 'auction'

urlpatterns = [
    path('', include(router.urls)),
    path('user/chose_bet/<int:lot>/', UserBetListAPIView.as_view(), name='chose_bet'),
    path('user/animals/', AnimalListAPIView.as_view(), name='animals')
]
