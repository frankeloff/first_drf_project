from rest_framework import serializers
from .models import Service, Enterprise, EnterpriseNetwork, EnterpriseService, Category


class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = ("pk", "enterprise_name", "description", "enterprise_network")


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("pk", "service_name", "category")


class EnterpriseNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnterpriseNetwork
        fields = ("pk", "enterprise_network_name")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("pk", "category_name")


class DetailedEnterpriseSerializer(serializers.ModelSerializer):
    enterprise_network = EnterpriseNetworkSerializer()

    class Meta:
        model = Enterprise
        fields = ("pk", "enterprise_name", "description", "enterprise_network")


class DetailedServiceSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Service
        fields = ("pk", "service_name", "category")


class DetailedServiceWithPriceSerializer(serializers.ModelSerializer):
    service = DetailedServiceSerializer()

    class Meta:
        model = EnterpriseService
        fields = ("pk", "service", "price")


class DetailEnterpriseAndServiceSerializer(serializers.ModelSerializer):
    enterprise = DetailedEnterpriseSerializer()
    service = DetailedServiceSerializer()

    class Meta:
        model = EnterpriseService
        fields = ("pk", "enterprise", "service", "price")
