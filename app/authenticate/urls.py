from django.urls import path

from .views import RegistrationAPIView, LoginAPIView, UserRetrieveAPIView

app_name = 'authenticate'

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('token/', LoginAPIView.as_view(), name='token'),
    path('user/', UserRetrieveAPIView.as_view(), name='user_data')

]
