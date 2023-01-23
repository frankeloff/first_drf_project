from django_filters import rest_framework as filters
from .models import Enterprise


class CategoryAndPriceFilter(filters.FilterSet):
    price__lt = filters.NumberFilter(
        field_name="enterpriseservice__price", lookup_expr="lt"
    )
    price__gt = filters.NumberFilter(
        field_name="enterpriseservice__price", lookup_expr="gt"
    )

    class Meta:
        model = Enterprise
        fields = ("price__lt", "price__gt")
