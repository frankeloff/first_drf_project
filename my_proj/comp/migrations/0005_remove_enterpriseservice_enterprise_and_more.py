# Generated by Django 4.1.5 on 2023-01-07 20:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("comp", "0004_remove_cityarea_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="enterpriseservice",
            name="enterprise",
        ),
        migrations.RemoveField(
            model_name="enterpriseservice",
            name="service",
        ),
        migrations.AddField(
            model_name="enterpriseservice",
            name="enterprise",
            field=models.ManyToManyField(
                to="comp.enterprise", verbose_name="Предприятие"
            ),
        ),
        migrations.AddField(
            model_name="enterpriseservice",
            name="service",
            field=models.ManyToManyField(
                to="comp.service", verbose_name="Услуга/товар"
            ),
        ),
    ]
