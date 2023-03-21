from django.contrib import admin
import rto_consultas.models as models

class VerificacionesFilter(admin.ModelAdmin):
    # list_display = ('idtaller', 'idtipouso', 'idestado')
    list_filter = ('idtaller', 'idtipouso', 'idestado')
    search_fields = ('idtaller',)

    

admin.site.register(models.Verificaciones, VerificacionesFilter)
admin.site.register(models.Certificados)
admin.site.register(models.Certificadosasignadosportaller)
admin.site.register(models.Vehiculos)
