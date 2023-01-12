from django.contrib import admin

from .models import (
    CityArea,
    Category,
    EnterpriseNetwork,
    Enterprise,
    Service,
    CityAreaEnterprise,
    EnterpriseService,
)


admin.site.register(CityArea)
admin.site.register(Category)
admin.site.register(EnterpriseNetwork)
admin.site.register(Enterprise)
admin.site.register(Service)
admin.site.register(CityAreaEnterprise)
admin.site.register(EnterpriseService)
