from django.db.models import F
from celery import shared_task



@shared_task
def set_price(subscription_id):
    from .models import Subscription    
    
    sub = Subscription.objects.filter(id=subscription_id).annotate(
        annotated_price=F('service__full_price') - 
              F('service__full_price') * 
              F('plan__discount_percent') / 100
    ).first()

    sub.price = sub.annotated_price
    sub.save()