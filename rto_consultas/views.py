from django.views.generic import ListView
from .models import Verificaciones, Certificadosasignadosportaller

class ListVerificacionesView(ListView):
	model = Verificaciones

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['Certificados'] = self.model.objects.all()[:5]
		return context
