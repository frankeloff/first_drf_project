from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import (
    Enterprise,
    EnterpriseNetwork,
    Category,
    Service,
    EnterpriseService,
    CityArea,
    CityAreaEnterprise,
)
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .serializers import (
    EnterpriseSerializer,
    DetailedServiceWithPriceSerializer,
    DetailedServiceSerializer,
    DetailEnterpriseAndServiceSerializer,
    DetailedEnterpriseSerializer,
)


class AuthorizationTests(APITestCase):
    def setUp(self):
        # Создание юзеров
        user_test1 = User.objects.create_user(
            username="test1", email="test1@mail.ru", password="lq2w3e"
        )
        user_test1.save()

        # Создание токенов
        self.user_test1_token = Token.objects.create(user=user_test1)

        # Вспомогательные элементы
        self.category_test1 = Category.objects.create(category_name="Для ухода")
        self.category_test1.save()

        self.enterprice_network_test1 = EnterpriseNetwork.objects.create(
            enterprise_network_name="ProductsComp"
        )
        self.enterprice_network_test1.save()

        self.enterprise_test_1 = Enterprise.objects.create(
            enterprise_name="Пятерочка",
            description="Магазин продуктов",
            enterprise_network=EnterpriseNetwork.objects.get(
                enterprise_network_name="ProductsComp"
            ),
        )
        self.enterprise_test_1.save()

        self.service_test1 = Service.objects.create(
            service_name="Расческа", category=self.category_test1
        )
        self.service_test1.save()

        self.service_data = {"service_name": "Мыло", "category": self.category_test1.pk}

    # Тестирование на защищенность API токеном всех API
    # Тестирование всех предприятий
    def test_invalid_get_all_enterprises(self):
        response = self.client.get(reverse("all_organizations_details"), format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_enterprises(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(reverse("all_organizations_details"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_get_enterprise(self):
        response = self.client.get(
            reverse("current_organization_detail", kwargs={"pk": 1}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_enterprise(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse(
                "current_organization_detail", kwargs={"pk": self.enterprise_test_1.pk}
            ),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Тестирование активных предприятий
    def test_invalid_get_all_active_enterprises(self):
        response = self.client.get(
            reverse("all_active_organizations_details"), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_active_enterprises(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse("all_active_organizations_details"), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_get_active_enterprise(self):
        response = self.client.get(
            reverse("current_active_organization_detail", kwargs={"pk": 1}),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_active_enterprise(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse("current_active_organization_detail", kwargs={"pk": 1}),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Тестирование всех товаров/услуг
    def test_invalid_get_all_services(self):
        response = self.client.get(reverse("all_services_details"), format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_services(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(reverse("all_services_details"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_get_service(self):
        response = self.client.get(
            reverse("current_service_detail", kwargs={"pk": 1}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_service(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse("current_service_detail", kwargs={"pk": self.service_test1.pk}),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Тестирование активных товаров/услуг
    def test_invalid_get_all_active_services(self):
        response = self.client.get(
            reverse("all_active_services_details"), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_active_services(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse("all_active_services_details"), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_get_active_service(self):
        response = self.client.get(
            reverse("current_active_service_detail", kwargs={"pk": 1}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_active_service(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse("current_active_service_detail", kwargs={"pk": 1}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Тестирование добавления категории
    def test_invalid_add_category(self):
        response = self.client.post(
            reverse("add_service"), self.service_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_category(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.post(
            reverse("add_service"), self.service_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_organizations_from_a_specific_area(self):
        response = self.client.get(
            reverse("organizations_from_a_specific_area", kwargs={"district_id": 1})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_organizations_from_a_specific_area(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse("organizations_from_a_specific_area", kwargs={"district_id": 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Тестирование вывода списока заведений с условием заранее выбранного района
    def test_invalid_organizations_from_a_specific_area(self):
        response = self.client.get(
            reverse("organizations_from_a_specific_area", kwargs={"district_id": 1}),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_organizations_from_a_specific_area(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse("organizations_from_a_specific_area", kwargs={"district_id": 1}),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DataReturnTests(APITestCase):
    def setUp(self):
        # Создание юзеров
        user_test1 = User.objects.create_user(
            username="test1", email="test1@mail.ru", password="lq2w3e"
        )
        user_test1.save()

        # Создание токенов
        self.user_test1_token = Token.objects.create(user=user_test1)

        # Вспомогательные элементы

        # Категории
        self.category_test1 = Category.objects.create(category_name="Для ухода")
        self.category_test1.save()
        self.category_test2 = Category.objects.create(category_name="Продукты")
        self.category_test2.save()
        self.category_test3 = Category.objects.create(category_name="Мебель")
        self.category_test3.save()

        # Сервисы
        self.service_test1 = Service.objects.create(
            service_name="Расческа", category=self.category_test1
        )
        self.service_test1.save()
        self.service_test2 = Service.objects.create(
            service_name="Шампунь", category=self.category_test1
        )
        self.service_test2.save()
        self.service_test3 = Service.objects.create(
            service_name="Крем для лица", category=self.category_test1
        )
        self.service_test3.save()
        self.service_test4 = Service.objects.create(
            service_name="Бананы", category=self.category_test2
        )
        self.service_test4.save()
        self.service_test5 = Service.objects.create(
            service_name="Кресло", category=self.category_test3
        )
        self.service_test5.save()

        # Сети предприятий
        self.enterprice_network_test1 = EnterpriseNetwork.objects.create(
            enterprise_network_name="X5Group"
        )
        self.enterprice_network_test2 = EnterpriseNetwork.objects.create(
            enterprise_network_name="Alibaba"
        )
        self.enterprice_network_test1.save()
        self.enterprice_network_test2.save()

        # Предприятия
        self.enterprise_test_1 = Enterprise.objects.create(
            enterprise_name="Пятерочка",
            description="Магазин продуктов",
            enterprise_network=EnterpriseNetwork.objects.get(
                enterprise_network_name="X5Group"
            ),
        )

        self.enterprise_test_2 = Enterprise.objects.create(
            enterprise_name="Магнит",
            description="Магазин продуктов",
            enterprise_network=EnterpriseNetwork.objects.get(
                enterprise_network_name="X5Group"
            ),
        )

        self.enterprise_test_3 = Enterprise.objects.create(
            enterprise_name="Лента",
            description="Магазин продуктов",
            enterprise_network=EnterpriseNetwork.objects.get(
                enterprise_network_name="X5Group"
            ),
        )

        self.enterprise_test_4 = Enterprise.objects.create(
            enterprise_name="Aliexpress",
            description="Товары для всего",
            enterprise_network=EnterpriseNetwork.objects.get(
                enterprise_network_name="Alibaba"
            ),
        )
        self.enterprise_test_5 = Enterprise.objects.create(
            enterprise_name="Ашан",
            description="Магазин мебели",
            enterprise_network=EnterpriseNetwork.objects.get(
                enterprise_network_name="X5Group"
            ),
        )

        self.enterprise_test_1.save()
        self.enterprise_test_2.save()
        self.enterprise_test_3.save()
        self.enterprise_test_4.save()

        # Связывание предприятий с товарами/услугами
        self.enterprise_service_test1 = EnterpriseService.objects.create(
            enterprise=self.enterprise_test_1, service=self.service_test1, price=150
        )
        self.enterprise_service_test2 = EnterpriseService.objects.create(
            enterprise=self.enterprise_test_2, service=self.service_test1, price=250
        )
        self.enterprise_service_test3 = EnterpriseService.objects.create(
            enterprise=self.enterprise_test_3, service=self.service_test1, price=350
        )
        self.enterprise_service_test4 = EnterpriseService.objects.create(
            enterprise=self.enterprise_test_3, service=self.service_test4, price=120
        )
        self.enterprise_service_test5 = EnterpriseService.objects.create(
            enterprise=self.enterprise_test_5, service=self.service_test5, price=120
        )
        self.enterprise_service_test1.save()
        self.enterprise_service_test2.save()
        self.enterprise_service_test3.save()
        self.enterprise_service_test4.save()
        self.enterprise_service_test5.save()

        # Создание районов
        self.cityarea_test1 = CityArea.objects.create(city_area_name="Выхино")
        self.cityarea_test2 = CityArea.objects.create(city_area_name="Коптево")
        self.cityarea_test1.save()
        self.cityarea_test2.save()

        # Связывание организаций и районов
        self.enterprice_cityarea_test1 = CityAreaEnterprise.objects.create(
            enterprise=self.enterprise_test_1, city_area=self.cityarea_test1
        )
        self.enterprice_cityarea_test2 = CityAreaEnterprise.objects.create(
            enterprise=self.enterprise_test_2, city_area=self.cityarea_test1
        )
        self.enterprice_cityarea_test3 = CityAreaEnterprise.objects.create(
            enterprise=self.enterprise_test_5, city_area=self.cityarea_test1
        )
        self.enterprice_cityarea_test4 = CityAreaEnterprise.objects.create(
            enterprise=self.enterprise_test_3, city_area=self.cityarea_test2
        )
        self.enterprice_cityarea_test5 = CityAreaEnterprise.objects.create(
            enterprise=self.enterprise_test_4, city_area=self.cityarea_test2
        )
        self.enterprice_cityarea_test1.save()
        self.enterprice_cityarea_test2.save()
        self.enterprice_cityarea_test3.save()
        self.enterprice_cityarea_test4.save()
        self.enterprice_cityarea_test5.save()

        category_test4 = Category.objects.create(category_name="Для ухода")
        category_test4.save()
        self.service_data = {"service_name": "Мыло", "category": category_test4.pk}

    # Тестирование корректной работы API
    # Получение детальной информации обо всех организациях
    def test_get_all_enterprises_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(reverse("all_organizations_details"), format="json")
        serializer_data1 = DetailedEnterpriseSerializer(self.enterprise_test_1).data
        serializer_data2 = DetailedEnterpriseSerializer(self.enterprise_test_2).data
        serializer_data3 = DetailedEnterpriseSerializer(self.enterprise_test_3).data
        serializer_data4 = DetailedEnterpriseSerializer(self.enterprise_test_4).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data1, response.data)
        self.assertIn(serializer_data2, response.data)
        self.assertIn(serializer_data3, response.data)
        self.assertIn(serializer_data4, response.data)

    def test_get_current_enterprises_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse(
                "current_organization_detail", kwargs={"pk": self.enterprise_test_1.pk}
            )
        )
        serializer_data1 = DetailedEnterpriseSerializer(self.enterprise_test_1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data1, response.data)

    # Получение информации об активных организациях
    def test_get_all_active_enterprises_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse("all_active_organizations_details"), format="json"
        )
        serializer_data1 = DetailEnterpriseAndServiceSerializer(
            self.enterprise_service_test1
        ).data
        serializer_data2 = DetailEnterpriseAndServiceSerializer(
            self.enterprise_service_test2
        ).data
        serializer_data3 = DetailEnterpriseAndServiceSerializer(
            self.enterprise_service_test3
        ).data
        serializer_data4 = DetailEnterpriseAndServiceSerializer(
            self.enterprise_service_test4
        ).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data1, response.data)
        self.assertIn(serializer_data2, response.data)
        self.assertIn(serializer_data3, response.data)
        self.assertIn(serializer_data4, response.data)

    def test_get_current_active_enterprise_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse(
                "current_active_organization_detail",
                kwargs={"pk": self.enterprise_test_1.pk},
            ),
            format="json",
        )
        serializer_data1 = DetailEnterpriseAndServiceSerializer(
            self.enterprise_service_test1
        ).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data1, response.data)

    # Получение детальной информации обо всех товарах
    def test_get_all_services_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(reverse("all_services_details"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data1 = DetailedServiceSerializer(self.service_test1).data
        serializer_data2 = DetailedServiceSerializer(self.service_test2).data
        serializer_data3 = DetailedServiceSerializer(self.service_test3).data
        serializer_data4 = DetailedServiceSerializer(self.service_test4).data

        self.assertIn(serializer_data1, response.data)
        self.assertIn(serializer_data2, response.data)
        self.assertIn(serializer_data3, response.data)
        self.assertIn(serializer_data4, response.data)

    def test_get_current_services_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse("current_service_detail", kwargs={"pk": self.service_test1.pk}),
            format="json",
        )
        serializer_data1 = DetailedServiceSerializer(self.service_test1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data1, response.data)

    # Получение детальной информации о товарах/услугах, которые есть на рынке
    def test_get_all_acative_services_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse("all_active_services_details"), format="json"
        )
        serializer_data1 = DetailedServiceWithPriceSerializer(
            self.enterprise_service_test1
        ).data
        serializer_data2 = DetailedServiceWithPriceSerializer(
            self.enterprise_service_test2
        ).data
        serializer_data3 = DetailedServiceWithPriceSerializer(
            self.enterprise_service_test3
        ).data
        serializer_data4 = DetailedServiceWithPriceSerializer(
            self.enterprise_service_test4
        ).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data1, response.data)
        self.assertIn(serializer_data2, response.data)
        self.assertIn(serializer_data3, response.data)
        self.assertIn(serializer_data4, response.data)

    def test_get_current_active_services_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse(
                "current_active_service_detail", kwargs={"pk": self.service_test1.pk}
            ),
            format="json",
        )
        serializer_data1 = DetailedServiceWithPriceSerializer(
            self.enterprise_service_test1
        ).data
        serializer_data2 = DetailedServiceWithPriceSerializer(
            self.enterprise_service_test2
        ).data
        serializer_data3 = DetailedServiceWithPriceSerializer(
            self.enterprise_service_test3
        ).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data1, response.data)
        self.assertIn(serializer_data2, response.data)
        self.assertIn(serializer_data3, response.data)

    # Получение заведений с условием заранее выбранного района
    def test_organizations_from_a_specific_area_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse(
                "organizations_from_a_specific_area",
                kwargs={"district_id": self.cityarea_test1.pk},
            ),
            format="json",
        )
        serializer_data1 = EnterpriseSerializer(self.enterprise_test_1).data
        serializer_data2 = EnterpriseSerializer(self.enterprise_test_2).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data1, response.data)
        self.assertIn(serializer_data2, response.data)

    # Тестирование фильтров
    def test_search_filter_in_organizations_from_a_specific_area_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse(
                "organizations_from_a_specific_area",
                kwargs={"district_id": self.cityarea_test1.pk},
            )
            + "?category_name=Для%20ухода",
            format="json",
        )
        serializer_data1 = EnterpriseSerializer(self.enterprise_test_1).data
        serializer_data2 = EnterpriseSerializer(self.enterprise_test_2).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data1, response.data)
        self.assertIn(serializer_data2, response.data)

        response = self.client.get(
            reverse(
                "organizations_from_a_specific_area",
                kwargs={"district_id": self.cityarea_test1.pk},
            )
            + "?category_name=Мебель",
            format="json",
        )
        serializer_data5 = EnterpriseSerializer(self.enterprise_test_5).data
        self.assertIn(serializer_data5, response.data)

    def test_price_filter_in_organizations_from_a_specific_area_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse(
                "organizations_from_a_specific_area",
                kwargs={"district_id": self.cityarea_test1.pk},
            )
            + "?price__lt=200",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data1 = EnterpriseSerializer(self.enterprise_test_1).data
        self.assertIn(serializer_data1, response.data)
        serializer_data5 = EnterpriseSerializer(self.enterprise_test_5).data
        self.assertIn(serializer_data5, response.data)

        response = self.client.get(
            reverse(
                "organizations_from_a_specific_area",
                kwargs={"district_id": self.cityarea_test1.pk},
            )
            + "?price__gt=200",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data2 = EnterpriseSerializer(self.enterprise_test_2).data
        self.assertIn(serializer_data2, response.data)

    def test_search_and_price_filters_in_organizations_from_a_specific_area_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse(
                "organizations_from_a_specific_area",
                kwargs={"district_id": self.cityarea_test1.pk},
            )
            + "?price__lt=200&category_name=Для%20ухода",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data1 = EnterpriseSerializer(self.enterprise_test_1).data
        self.assertIn(serializer_data1, response.data)

        response = self.client.get(
            reverse(
                "organizations_from_a_specific_area",
                kwargs={"district_id": self.cityarea_test1.pk},
            )
            + "?price__lt=200&category_name=Мебель",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data5 = EnterpriseSerializer(self.enterprise_test_5).data
        self.assertIn(serializer_data5, response.data)

        response = self.client.get(
            reverse(
                "organizations_from_a_specific_area",
                kwargs={"district_id": self.cityarea_test1.pk},
            )
            + "?price__gt=200&category_name=Для%20ухода",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data2 = EnterpriseSerializer(self.enterprise_test_2).data
        self.assertIn(serializer_data2, response.data)

    # Добавление товара/услуги
    def test_add_category(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.post(
            reverse("add_service"), self.service_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Service.objects.get(service_name=self.service_data.get("service_name"))
        )
