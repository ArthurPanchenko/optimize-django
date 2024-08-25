from django.db.models import Prefetch, F, Sum
from django.core.cache import cache

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

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        price_cache = cache.get('price_cache')

        if price_cache:
            total_price = price_cache
        else:
            total_price = qs.aggregate(
                total=Sum('price')
            ).get('total')
            cache.set('price_cache', total_price, 10)

        response_data = {'result': response.data}
        response_data['total_amount'] = total_price
        response.data = response_data

        return response