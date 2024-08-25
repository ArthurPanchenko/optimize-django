import time

from django.db.models import F
from django.core.cache import cache

from celery import shared_task
from celery_singleton import Singleton


@shared_task(base=Singleton)
def set_price(subscription_id):
    from .models import Subscription    
    
    time.sleep(10)

    sub = Subscription.objects.filter(id=subscription_id).annotate(
        annotated_price=F('service__full_price') - 
              F('service__full_price') * 
              F('plan__discount_percent') / 100
    ).first()

    sub.price = sub.annotated_price
    sub.save()
    cache.delete('price_cache')
