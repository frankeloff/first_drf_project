from django.db import models


class CityArea(models.Model):
    city_area_name = models.CharField(
        max_length=80, verbose_name="Название района города"
    )

    class Meta:
        verbose_name = "Район города"
        verbose_name_plural = "Районы города"


class Category(models.Model):
    category_name = models.CharField(max_length=80, verbose_name="Название категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class EnterpriseNetwork(models.Model):
    enterprise_network_name = models.CharField(
        max_length=80, verbose_name="Название сети предприятий"
    )

    class Meta:
        verbose_name = "Сеть предприятий"
        verbose_name_plural = "Сети предприятий"


class Enterprise(models.Model):
    enterprise_name = models.CharField(
        max_length=80, verbose_name="Название предприятия"
    )
    description = models.TextField(blank=False, verbose_name="Описание")
    enterprise_network = models.ForeignKey(
        "EnterpriseNetwork", on_delete=models.PROTECT, verbose_name="Сеть предприятий"
    )

    class Meta:
        verbose_name = "Предприятие"
        verbose_name_plural = "Предприятия"


class Service(models.Model):
    service_name = models.CharField(
        max_length=80, verbose_name="Название услуги/товара"
    )
    category = models.ForeignKey(
        "Category", on_delete=models.PROTECT, verbose_name="Категория услуги/товара"
    )

    class Meta:
        verbose_name = "Сервис"
        verbose_name_plural = "Сервисы"


class CityAreaEnterprise(models.Model):
    enterprise = models.ForeignKey(
        "Enterprise", on_delete=models.PROTECT, verbose_name="Предприятие"
    )
    city_area = models.ForeignKey(
        "CityArea", on_delete=models.PROTECT, verbose_name="Район города"
    )

    class Meta:
        verbose_name = "Район города и предприятие"
        verbose_name_plural = "Районы города и предприятия"


class EnterpriseService(models.Model):
    enterprise = models.ForeignKey(
        "Enterprise", on_delete=models.PROTECT, verbose_name="Предприятие"
    )
    service = models.ForeignKey(
        "Service", on_delete=models.PROTECT, verbose_name="Услуга/товар"
    )
    price = models.IntegerField()

    class Meta:
        verbose_name = "Предприятие и сервис"
        verbose_name_plural = "Предприятия и сервисы"
