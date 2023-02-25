from .models import Service, Enterprise, CityAreaEnterprise, EnterpriseService
from typing import List


def get_city_area_enterprises_by_city_area_id(city_area_id: int) -> List[Enterprise]:
    result = CityAreaEnterprise.objects.filter(city_area__pk=city_area_id)
    return result


def get_enterprises_in_certain_city_area(
    city_area_enterprises: List[CityAreaEnterprise],
) -> List[Enterprise]:
    result = Enterprise.objects.filter(
        id__in=city_area_enterprises.values("enterprise")
    )
    return result


def get_all_services():
    result = Service.objects.all()
    return result


def get_all_enterprises():
    result = Enterprise.objects.all()
    return result


def get_certain_enterprise_by_enterprise_id(ent_id: int) -> Enterprise:
    result = Enterprise.objects.filter(pk=ent_id)
    return result


def get_all_enterprise_service():
    result = EnterpriseService.objects.all()
    return result


def get_certain_enterprise_service_by_enterprise_id(ent_id: int) -> EnterpriseService:
    result = EnterpriseService.objects.filter(enterprise__pk=ent_id)
    return result


def get_certain_enterprise_service_by_service_id(service_id: int) -> EnterpriseService:
    result = EnterpriseService.objects.filter(service__pk=service_id)
    return result


def get_all_services():
    result = Service.objects.all()
    return result


def get_certain_service_by_service_id(service_id: int) -> Service:
    result = Service.objects.filter(pk=service_id)
    return result
