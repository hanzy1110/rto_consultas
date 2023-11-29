# from rto_consultas.models import Talleres as TalleresNQN
# from rto_consultas_rn.models import Talleres as TalleresRN
# from rto_consultas.helpers import map_fields

VALS = {1: "Verdadero", 0: "Falso"}

VALS_ANULADO = {1: "anulado", 0: "vigente"}

DESCRIPTIONS = {
    1: "Particular",
    2: "Transporte de Carga",
    3: "Transporte Pasajeros",
    4: "Transporte Municipal",
}

ESTADO_CERTIFICADO = {
    1: "Aprobado",
    2: "Rechazado",
    3: "Condicional",
    4: "Reverificado",
    5: "Vencido",
}

SIGN_DICT = {
    "malanis": "/home/code/static/img/signs/malanis.jpg",
    "rpadua": "/home/code/static/img/signs/rpadua.png",
    "rtralamil": "/home/code/static/img/signs/rtralamil.jpg",
}

MONTHS_DICT = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}

TIPO_USO_VEHICULO = {
    1: "Particular",
    2: "Carga",
    3: "Pasajeros",
    4: "Municipal",
}

ESTADOS_CCCF = {1: "Vigente", 2: "Vencido", 3: "Anulado"}

DOCS = [(i, d) for i, d in enumerate(["", "DNI", "LC", "LE", "PAS", "CUIT"])]

MODIFICADOS = {0: "No", 1: "Si"}

USER_GROUPS = [
    "CCCFGroup",
    "DPTGroup",
    "SecTranspRNGroup",
    "SVGroup",
    "VialidadRNGroup",
]

# TALLERES_NQN_CHOICES = map_fields([], TalleresNQN)
# TALLERES_RN_CHOICES = map_fields([], TalleresRN)
