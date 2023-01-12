from rest_framework import serializers
from .models import Service, Enterprise, EnterpriseNetwork, EnterpriseService, Category


class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class EnterpriseNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnterpriseNetwork
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class DetailedEnterpriseSerializer(serializers.ModelSerializer):
    enterprise_network = EnterpriseNetworkSerializer()

    class Meta:
        model = Enterprise
        fields = "__all__"


class DetailedServiceSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Service
        fields = "__all__"


class DetailedServiceWithPriceSerializer(serializers.ModelSerializer):
    service = DetailedServiceSerializer()

    class Meta:
        model = EnterpriseService
        fields = "__all__"


class DetailEnterpriseAndServiceSerializer(serializers.ModelSerializer):
    enterprise = DetailedEnterpriseSerializer()
    service = DetailedServiceSerializer()

    class Meta:
        model = EnterpriseService
        fields = "__all__"
