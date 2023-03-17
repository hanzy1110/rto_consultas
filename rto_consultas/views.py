from django.views.generic import ListView
from .models import Verificaciones

class ListarVerificaciones(ListView):
	model = Verificaciones
	queryset = model.all().using('vehicularunc')

