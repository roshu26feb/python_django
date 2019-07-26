from django.contrib import admin
from .models import RundeckJobEntry, Server, ServiceGroup, Services, \
    ServiceInstance, MountTimeStamp, Mount, Facts

admin.site.register(RundeckJobEntry)
admin.site.register(Server)
admin.site.register(ServiceGroup)
admin.site.register(Services)
admin.site.register(ServiceInstance)
admin.site.register(MountTimeStamp)
admin.site.register(Mount)
admin.site.register(Facts)
