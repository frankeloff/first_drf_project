# Generated by Django 4.1.5 on 2023-01-04 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "category_name",
                    models.CharField(max_length=80, verbose_name="Название категории"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CityArea",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "city_area_name",
                    models.CharField(
                        max_length=80, verbose_name="Название района города"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Enterprise",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "enterprise_name",
                    models.CharField(
                        max_length=80, verbose_name="Название предприятия"
                    ),
                ),
                ("description", models.TextField(verbose_name="Описание")),
            ],
        ),
        migrations.CreateModel(
            name="EnterpriseNetwork",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "enterprise_network_name",
                    models.CharField(
                        max_length=80, verbose_name="Название сети предприятий"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "service_name",
                    models.CharField(
                        max_length=80, verbose_name="Название услуги/товара"
                    ),
                ),
                (
                    "service_category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="comp.category",
                        verbose_name="Категория услуги/товара",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EnterpriseService",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.IntegerField()),
                (
                    "enterprise_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="comp.enterprise",
                        verbose_name="Предприятие",
                    ),
                ),
                (
                    "service_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="comp.service",
                        verbose_name="Услуга/товар",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="enterprise",
            name="enterprise_network_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="comp.enterprisenetwork",
                verbose_name="Сеть предприятий",
            ),
        ),
        migrations.CreateModel(
            name="CityAreaEnterprise",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "city_area_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="comp.cityarea",
                        verbose_name="Район города",
                    ),
                ),
                (
                    "enterprise_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="comp.enterprise",
                        verbose_name="Предприятие",
                    ),
                ),
            ],
        ),
    ]
