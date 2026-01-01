# apps/properties/filters.py
import django_filters
from .models import Property

class PropertyFilter(django_filters.FilterSet):
    advert_type = django_filters.CharFilter(field_name="advert_type", lookup_expr="iexact")
    property_type = django_filters.CharFilter(field_name="property_type", lookup_expr="iexact")
    city = django_filters.CharFilter(field_name="city", lookup_expr="icontains")
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    bedrooms_min = django_filters.NumberFilter(field_name="bedrooms", lookup_expr="gte")

    class Meta:
        model = Property
        fields = ["advert_type", "property_type", "city", "price_min", "price_max", "bedrooms_min"]