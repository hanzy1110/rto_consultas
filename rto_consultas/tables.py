import django_tables2 as tables
from .models import Verificaciones, Vehiculos, Certificados, Certificadosasignadosportaller

class VerificacionesTables(tables.Table):
	class Meta:
		model = Verificaciones
		fields = {
			"dominiovehiculo",
			"idestado",
			"idtipouso"
			}

class VehiculosTable(tables.Table):
	class Meta:
		model = Vehiculos
		fields = {
		"dominio",
		"idtipouso",
		"marca" 
		}

class CertificadosTable(tables.Table):
	class Meta:
		model = Certificados
		fields = {
		"nrocertificado",
		"idtaller",
		"fecha",
		"anulado"
		}

class CertificadosAssignTable(tables.Table):
	class Meta:
		model = Certificadosasignadosportaller
		query_fields = {
			"nrocertificado",
			"disponible",
			"replicado"
			}

