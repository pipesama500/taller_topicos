from django.contrib import admin
from .models import Roles, Unidad, Torre, Piso, Apartamento, Usuario

admin.site.register(Roles)
admin.site.register(Unidad)
admin.site.register(Torre)
admin.site.register(Piso)
admin.site.register(Apartamento)
admin.site.register(Usuario)