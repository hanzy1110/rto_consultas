from django.views.generic import ListView
from .models import Verificaciones

class ListVerificacionesView(ListView):
	model = Verificaciones
	# queryset = model.objects.all().using('vehicularunc')
	queryset = model.objects.all()

