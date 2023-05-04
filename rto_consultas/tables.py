import django_tables2 as tables
from django.core.paginator import Paginator
from .models import Verificaciones, Vehiculos, Certificados, Certificadosasignadosportaller

class VerificacionesTables(tables.Table):
	class Meta:
		model = Verificaciones
		fields = {
			"dominiovehiculo",
			"idestado",
			"idtipouso"
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

class VehiculosTable(tables.Table):
	class Meta:
		model = Vehiculos
		fields = {
		"dominio",
		"idtipouso",
		"marca" 
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


class CertificadosTable(tables.Table):
	class Meta:
		model = Certificados
		fields = {
		"nrocertificado",
		"idtaller",
		"fecha",
		"anulado"
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
