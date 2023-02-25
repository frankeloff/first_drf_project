from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from .comp_service import (
    get_city_area_enterprises_by_city_area_id,
    get_enterprises_in_certain_city_area,
    get_all_services,
    get_all_enterprises,
    get_certain_enterprise_by_enterprise_id,
    get_all_enterprise_service,
    get_certain_enterprise_service_by_enterprise_id,
    get_certain_enterprise_service_by_service_id,
    get_all_services,
    get_certain_service_by_service_id,
)
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
        particular_enterprises = get_city_area_enterprises_by_city_area_id(
            city_area_id=district_id
        )
        queryset = get_enterprises_in_certain_city_area(
            city_area_enterprises=particular_enterprises
        )
        return queryset


# Добавление товара/услуги
class ServiceAPICreate(BaseCreateAPIView):
    queryset = get_all_services()
    serializer_class = ServiceSerializer


# Детальная информация обо всех заведениях (даже о тех, которых нет на рынке)
class DetailEnterpriseInformation(BaseListAPIView):
    queryset = get_all_enterprises()
    serializer_class = DetailedEnterpriseSerializer


# Детальная информация о конкретном заведении(даже о том, которого нет на рынке)
class DetailAboutParticularEnterpriseInformation(BaseRetrieveAPIView):
    serializer_class = DetailedEnterpriseSerializer

    def get_queryset(self):
        ent_id = self.kwargs["pk"]
        queryset = get_certain_enterprise_by_enterprise_id(ent_id=ent_id)
        return queryset


# Детальная информация по заведениям, которые есть на рынке
class DetailEnterpriseServiceInformation(BaseListAPIView):
    queryset = get_all_enterprise_service()
    serializer_class = DetailEnterpriseAndServiceSerializer


# Детальная информация по заведению, которые есть на рынке
class DetailAboutParticularEnterpriseServiceInformation(BaseListAPIView):
    serializer_class = DetailEnterpriseAndServiceSerializer

    def get_queryset(self):
        ent_id = self.kwargs["pk"]
        queryset = get_certain_enterprise_service_by_enterprise_id(ent_id=ent_id)
        return queryset


# Детальная информация по товарам/услугах, которые есть в продаже
class DetailActiveServiceInformation(BaseListAPIView):
    queryset = get_all_enterprise_service()
    serializer_class = DetailedServiceWithPriceSerializer


# Детальная информация о товаре/услуге, которые есть в продаже
class DetailAboutParticularActiveServiceInformation(BaseListAPIView):
    serializer_class = DetailedServiceWithPriceSerializer

    def get_queryset(self):
        active_service_id = self.kwargs["pk"]
        queryset = get_certain_enterprise_service_by_service_id(
            service_id=active_service_id
        )
        return queryset


# Детальная информация по всем товарам/услугах (даже по тем, которых нет в продаже/которого нет в продаже у заведений)
class DetailServiceInformation(BaseListAPIView):
    queryset = get_all_services()
    serializer_class = DetailedServiceSerializer


# Детальная информация о конкретном товаре/услуге (даже по тем, которых нет в продаже/которого нет в продаже у заведений)
class DetailAboutParticularServiceInformation(BaseRetrieveAPIView):
    serializer_class = DetailedServiceSerializer

    def get_queryset(self):
        service_id = self.kwargs["pk"]
        queryset = get_certain_service_by_service_id(service_id=service_id)
        return queryset
