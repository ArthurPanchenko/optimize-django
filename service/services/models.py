from typing import Iterable
from django.db import models
from django.core.validators import MaxValueValidator

from clients.models import Client
from .tasks import set_price


class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.__full_price = self.full_price

    def save(self, *args, **kwargs):
        
        if self.full_price != self.__full_price:
            for service in self.subscription.all():
                set_price.delay(service.id)
        
        return super().save(*args, **kwargs)

class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount')
    )

    plan_type = models.CharField(choices=PLAN_TYPES, max_length=10)
    discount_percent = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(100)]
    )

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.__discount_percent = self.discount_percent

    def __str__(self):
        return f'{self.plan_type}: {self.discount_percent}%'
    
    def save(self, *args, **kwargs):
        
        if self.discount_percent != self.__discount_percent:
            for sub in self.subscription.all():
                set_price.delay(sub.id)
        
        return super().save(*args, **kwargs)


class Subscription(models.Model):
    client = models.ForeignKey(
        Client,
        related_name='subscription',
        on_delete=models.PROTECT   
    )
    service = models.ForeignKey(
        Service,
        related_name='subscription',
        on_delete=models.PROTECT   
    )
    plan = models.ForeignKey(
        Plan,
        related_name='subscription',
        on_delete=models.PROTECT
    )

    price = models.PositiveIntegerField()
    comment = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.client}, {self.service}, {self.plan}'
    
    def save(self, *args, **kwargs):
        created = bool(self.id)
        result = super().save(*args, *kwargs)
        if created:
            set_price.delay(self.id)
        return result