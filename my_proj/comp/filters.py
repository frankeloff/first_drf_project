from django_filters import rest_framework as filters
from .models import Enterprise


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class CategoryAndPriceFilter(filters.FilterSet):
    category_name = CharFilterInFilter(
        field_name="enterpriseservice__service__category__category_name",
        lookup_expr="in",
    )
    price__lt = filters.NumberFilter(
        field_name="enterpriseservice__price", lookup_expr="lt"
    )
    price__gt = filters.NumberFilter(
        field_name="enterpriseservice__price", lookup_expr="gt"
    )

    class Meta:
        model = Enterprise
        fields = ("category_name", "price__lt", "price__gt")
