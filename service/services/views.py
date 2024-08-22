from django.db.models import Prefetch

from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Subscription, Client
from .serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        Prefetch('client',
            queryset=Client.objects.all().select_related('user').only(
                'company_name',
                'user__email',
                'user__username',
            )
        )
    )
    
    serializer_class = SubscriptionSerializer