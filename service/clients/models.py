from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    company_name = models.CharField(max_length=100)
    full_address = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username