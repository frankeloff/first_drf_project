from django.urls import path, include, re_path
from .views import (
    ServiceAPICreate,
    EnterpriseAPIList,
    DetailEnterpriseServiceInformation,
    DetailServiceInformation,
    DetailEnterpriseInformation,
    DetailActiveServiceInformation,
)

urlpatterns = [
    path(
        "api/v1/service/add/",
        ServiceAPICreate.as_view(),
        name="add_service",
    ),  # Добавление товара/услуги
    path(
        "api/v1/organizations/<int:district_id>/",
        EnterpriseAPIList.as_view(),
        name="organizations_from_a_specific_area",
    ),  # Список заведений с условием заранее выбранного района
    path(
        "api/v1/organizations/all/details/",
        DetailEnterpriseInformation.as_view(),
        name="all_organizations_details",
    ),  # Детальная информация о заведениях
    path(
        "api/v1/organizations/all/details/<int:pk>/",
        DetailEnterpriseInformation.as_view(),
        name="current_organization_detail",
    ),  # Детальная информация о заведении
    path(
        "api/v1/organizations/active/details/",
        DetailEnterpriseServiceInformation.as_view(),
        name="all_active_organizations_details",
    ),  # Детальная информация о заведениях, которые есть на рынке
    path(
        "api/v1/organizations/active/details/<int:pk>/",
        DetailEnterpriseServiceInformation.as_view(),
        name="current_active_organization_detail",
    ),  # Детальная информация о заведении, которое есть на рынке
    path(
        "api/v1/services/all/details/",
        DetailServiceInformation.as_view(),
        name="all_services_details",
    ),  # Детальная информация о товарах/услугах
    path(
        "api/v1/services/all/details/<int:pk>/",
        DetailServiceInformation.as_view(),
        name="current_service_detail",
    ),  # Детальная информация о товаре/услуге
    path(
        "api/v1/services/active/details/",
        DetailActiveServiceInformation.as_view(),
        name="all_active_services_details",
    ),  # Детальная информация о товарах/услугах, которые есть в продаже
    path(
        "api/v1/services/active/details/<int:pk>/",
        DetailActiveServiceInformation.as_view(),
        name="current_active_service_detail",
    ),  # Детальная информация о товаре/услугe, который/которая есть в продаже
    path("api/v1/auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
]
