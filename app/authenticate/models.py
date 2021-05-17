from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    balance = models.DecimalField(decimal_places=3, max_digits=10, default=0, verbose_name='Total balance')
    last_login = models.DateTimeField('last_login', auto_now=True)

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=7)

        return jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'), )
        }, settings.SECRET_KEY)
