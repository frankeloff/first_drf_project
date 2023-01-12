from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from .models import Service, Enterprise, CityAreaEnterprise, EnterpriseService
from .serializers import (
    ServiceSerializer,
    EnterpriseSerializer,
    DetailEnterpriseAndServiceSerializer,
    DetailedServiceWithPriceSerializer,
    DetailedEnterpriseSerializer,
    DetailedServiceSerializer,
)
from rest_framework.permissions import (
    IsAuthenticated,
)
from .filters import CategoryAndPriceFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Вывод всех заведений или конкретного с возможностями поиска и фильтрами
class EnterpriseAPIList(generics.ListAPIView):
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    serializer_class = EnterpriseSerializer
    filterset_class = CategoryAndPriceFilter
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    search_fields = ("enterpriseservice__service__service_name",)

    def get_queryset(self):
        try:
            district_id = self.kwargs["district_id"]
            queryset = CityAreaEnterprise.objects.all()
            if district_id is not None:
                queryset = queryset.filter(city_area__pk=district_id)
                queryset = Enterprise.objects.filter(
                    id__in=queryset.values("enterprise")
                )
                return queryset
        except:
            return Enterprise.objects.all()


# Добавление товара/услуги
class ServiceAPICreate(generics.CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


# Детальная информация обо всех заведении/заведениях (даже о тех, которых нет на рынке)
class DetailEnterpriseInformation(generics.ListAPIView):
    serializer_class = DetailedEnterpriseSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        try:
            ent_id = self.kwargs["pk"]
            queryset = Enterprise.objects.filter(pk=ent_id)
            return queryset
        except:
            return Enterprise.objects.all()


# Детальная информация по заведению/заведениям, которые есть на рынке
class DetailEnterpriseServiceInformation(generics.ListAPIView):
    serializer_class = DetailEnterpriseAndServiceSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        try:
            ent_service_id = self.kwargs["pk"]
            queryset = EnterpriseService.objects.filter(enterprise__pk=ent_service_id)
            return queryset
        except:
            return EnterpriseService.objects.all()


# Детальная информация по товарам/услугах или товаре/услуге, которые есть в продаже
class DetailActiveServiceInformation(generics.ListAPIView):
    serializer_class = DetailedServiceWithPriceSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        try:
            active_service_id = self.kwargs["pk"]
            queryset = EnterpriseService.objects.filter(service__pk=active_service_id)
            return queryset
        except:
            return EnterpriseService.objects.all()


# Детальная информация по всем товарам/услугах или о конкретном товаре/услуге (даже по тем, которых нет в продаже/которого нет в продаже у заведений)
class DetailServiceInformation(generics.ListAPIView):
    serializer_class = DetailedServiceSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        try:
            service_id = self.kwargs["pk"]
            queryset = Service.objects.filter(pk=service_id)
            return queryset
        except:
            return Service.objects.all()
