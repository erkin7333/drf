from django_filters import rest_framework as filters
from .models import Kino




def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class KinoFilter(filters.FilterSet):
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')
    year = filters.RangeFilter()

    class Meta:
        model = Kino
        fields = ['genres', 'year']





####
# reting_user=models.Case(
#                 models.When(retings__ip=get_client_ip(request), then=True),
#                     default=False,
#                     output_field=models.BooleanField()

####