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


class BaseListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


class BaseCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


class BaseRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


# Вывод всех заведений или конкретного с возможностями поиска и фильтрами
class EnterpriseAPIList(BaseListAPIView):
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    serializer_class = EnterpriseSerializer
    filterset_class = CategoryAndPriceFilter
    search_fields = ("enterpriseservice__service__service_name",)

    def get_queryset(self):
        district_id = self.kwargs["district_id"]
        city_area_enterprise = CityAreaEnterprise.objects.all()
        particular_enterprises = city_area_enterprise.filter(city_area__pk=district_id)
        queryset = Enterprise.objects.filter(
            id__in=particular_enterprises.values("enterprise")
        )
        return queryset


# Добавление товара/услуги
class ServiceAPICreate(BaseCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


# Детальная информация обо всех заведениях (даже о тех, которых нет на рынке)
class DetailEnterpriseInformation(BaseListAPIView):
    queryset = Enterprise.objects.all()
    serializer_class = DetailedEnterpriseSerializer


# Детальная информация о конкретном заведении(даже о том, которого нет на рынке)
class DetailAboutParticularEnterpriseInformation(BaseRetrieveAPIView):
    serializer_class = DetailedEnterpriseSerializer

    def get_queryset(self):
        ent_id = self.kwargs["pk"]
        queryset = Enterprise.objects.filter(pk=ent_id)
        return queryset


# Детальная информация по заведениям, которые есть на рынке
class DetailEnterpriseServiceInformation(BaseListAPIView):
    queryset = EnterpriseService.objects.all()
    serializer_class = DetailEnterpriseAndServiceSerializer


# Детальная информация по заведению, которые есть на рынке
class DetailAboutParticularEnterpriseServiceInformation(BaseListAPIView):
    serializer_class = DetailEnterpriseAndServiceSerializer

    def get_queryset(self):
        ent_service_id = self.kwargs["pk"]
        queryset = EnterpriseService.objects.filter(enterprise__pk=ent_service_id)
        return queryset


# Детальная информация по товарам/услугах, которые есть в продаже
class DetailActiveServiceInformation(BaseListAPIView):
    queryset = EnterpriseService.objects.all()
    serializer_class = DetailedServiceWithPriceSerializer


# Детальная информация о товаре/услуге, которые есть в продаже
class DetailAboutParticularActiveServiceInformation(BaseListAPIView):
    serializer_class = DetailedServiceWithPriceSerializer

    def get_queryset(self):
        active_service_id = self.kwargs["pk"]
        queryset = EnterpriseService.objects.filter(service__pk=active_service_id)
        return queryset


# Детальная информация по всем товарам/услугах (даже по тем, которых нет в продаже/которого нет в продаже у заведений)
class DetailServiceInformation(BaseListAPIView):
    queryset = Service.objects.all()
    serializer_class = DetailedServiceSerializer


# Детальная информация о конкретном товаре/услуге (даже по тем, которых нет в продаже/которого нет в продаже у заведений)
class DetailAboutParticularServiceInformation(BaseRetrieveAPIView):
    serializer_class = DetailedServiceSerializer

    def get_queryset(self):
        service_id = self.kwargs["pk"]
        queryset = Service.objects.filter(pk=service_id)
        return queryset
