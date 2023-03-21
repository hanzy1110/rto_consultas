from django.views.generic import ListView
from .models import Verificaciones, Certificadosasignadosportaller

class ListVerificacionesView(ListView):
	model = Certificadosasignadosportaller
	# queryset = model.objects.all().using('vehicularunc')
	queryset = model.objects.all()

