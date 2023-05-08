import django_tables2 as tables
from django.core.paginator import Paginator
from .models import Verificaciones, Vehiculos, Certificados, Certificadosasignadosportaller
from .models import Estados, Tipousovehiculo, Talleres


def map_fields(form_fields, description_fields, model):
    values = {}
    for field, (dfield, dmodel) in zip(form_fields, description_fields):
        val = model.objects.values_list(field, flat=True).distinct() 
        descriptions = dmodel.objects.values_list(dfield, flat=True).distinct() 
        values[field] = {v:d for v,d in zip(val, descriptions)}

    return values


class VerificacionesTables(tables.Table):

	form_fields = {
					"idestado",
					"idtipouso"
					}
	description_fields = {
			("descripcion", Estados),
			("descripcion", Tipousovehiculo)
						}

	class Meta:
		model = Verificaciones
		fields = {
			"dominiovehiculo",
			"idestado",
			"idtipouso"
			}

	def render_idestado(self, value):

		# try:
			descriptions = map_fields(self.form_fields, self.description_fields, self.Meta.model)
			return descriptions["idestado"][value]
		# except Exception as e:
		# 	print(e)
		# 	return "Unknown!"

	def render_idtipouso(self, value):

		# try:
			descriptions = map_fields(self.form_fields, self.description_fields, self.Meta.model)
			return descriptions["idtipouso"][value]
		# except Exception as e:
		# 	print(e)
		# 	return "Unknown!"

	def paginate(self, paginator_class=Paginator, per_page=None, page=1, *args, **kwargs):

		per_page = per_page or self._meta.per_page
		self.paginator = paginator_class(self.rows, per_page, *args, **kwargs)
		self.page = self.paginator.page(page)

		return self


class VehiculosTable(tables.Table):

	form_fields = {
					"idtipouso",
					}

	description_fields = {
						("descripcion", Tipousovehiculo)
						}

	class Meta:
		model = Vehiculos
		fields = {
					"dominio",
					"idtipouso",
					"marca" 
				}

	def render_idtipouso(self, value):
		try:
			descriptions = map_fields(self.form_fields, self.description_fields, self.Meta.model)
			return descriptions["idtipouso"][value]
		except Exception as e:
			print(e)
			return "Unknown!"

	def paginate(self, paginator_class=Paginator, per_page=None, page=1, *args, **kwargs):

		per_page = per_page or self._meta.per_page
		self.paginator = paginator_class(self.rows, per_page, *args, **kwargs)
		self.page = self.paginator.page(page)

		return self


class CertificadosTable(tables.Table):

	form_fields = {
					"idtaller",
					}

	description_fields = {
						("nombre", Talleres)
						}

	class Meta:
		model = Certificados
		fields = {
		"nrocertificado",
		"idtaller",
		"fecha",
		"anulado"
		}

	def render_idtaller(self, value):
		try:
			descriptions = map_fields(self.form_fields, self.description_fields, self.Meta.model)
			return descriptions["idtaller"][value]
		except Exception as e:
			print(e)
			return "Unknown!"

	def paginate(self, paginator_class=Paginator, per_page=None, page=1, *args, **kwargs):
		"""
			Paginates the table using a paginator and creates a ``page`` property
			containing information for the current page.

			Arguments:
			paginator_class (`~django.core.paginator.Paginator`): A paginator class to
			    paginate the results.

			per_page (int): Number of records to display on each page.
			page (int): Page to display.

			Extra arguments are passed to the paginator.

			Pagination exceptions (`~django.core.paginator.EmptyPage` and
			`~django.core.paginator.PageNotAnInteger`) may be raised from this
			method and should be handled by the caller.
		"""

		per_page = per_page or self._meta.per_page
		self.paginator = paginator_class(self.rows, per_page, *args, **kwargs)
		self.page = self.paginator.page(page)

		return self


class CertificadosAssignTable(tables.Table):
	class Meta:
		model = Certificadosasignadosportaller
		query_fields = {
			"nrocertificado",
			"disponible",
			"replicado"
			}

	def paginate(self, paginator_class=Paginator, per_page=None, page=1, *args, **kwargs):
		"""
			Paginates the table using a paginator and creates a ``page`` property
			containing information for the current page.

			Arguments:
			paginator_class (`~django.core.paginator.Paginator`): A paginator class to
			    paginate the results.

			per_page (int): Number of records to display on each page.
			page (int): Page to display.

			Extra arguments are passed to the paginator.

			Pagination exceptions (`~django.core.paginator.EmptyPage` and
			`~django.core.paginator.PageNotAnInteger`) may be raised from this
			method and should be handled by the caller.
		"""

		per_page = per_page or self._meta.per_page
		self.paginator = paginator_class(self.rows, per_page, *args, **kwargs)
		self.page = self.paginator.page(page)

		return self
