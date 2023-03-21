from django.views.generic import ListView
from .models import Verificaciones, Certificadosasignadosportaller

class ListVerificacionesView(ListView):
	model = Verificaciones
	paginate_by = 10

	def get_queryset(self):
		# return self.model.objects.prefectch_related().all()[:5]
		return self.model.objects.all()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# context['Certificados'] = 
		return context
