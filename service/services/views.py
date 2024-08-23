from django.db.models import Prefetch, F, Sum

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

        response_data = {'result': response.data}
        response_data['total_amount'] = qs.aggregate(
            total=Sum('price')
        ).get('total')
        response.data = response_data

        return response