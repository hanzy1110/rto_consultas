from django.views.generic import ListView
from rto_consultas.models import Verificaciones

class ListarVerificaciones(ListView):
	model = Verificaciones

