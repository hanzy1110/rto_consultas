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

USER_QUERIES_CERTS_ASIGNADOS = {
    "CCCFGroup": {},
    "DPTGroup": {"idtipouso__iexact": 3},
    "SecTranspRNGroup": {"idtipouso__iexact": 3},
    "SVGroup": {"idtipouso__iexact": 1},
    "VialidadRNGroup": {"idtipouso__iexact": 1},
}


USER_QUERIES_VERIFICACIONES = {
    "CCCFGroup": {},
    "DPTGroup": {"idtipouso__iexact": 3},
    "SecTranspRNGroup": {"idtipouso__iexact": 3},
    "SVGroup": {"idtipouso__iexact": 1},
    "VialidadRNGroup": {"idtipouso__iexact": 1},
}

USER_CERTS_BOUNDS = {
    "CCCFGroup": None,
    "DPTGroup": "123",
    "SecTranspRNGroup": None,
    "SVGroup": "152",
    "VialidadRNGroup": None,
}

TARIFARIO_DPT = {
    "A": "Vehiculos utilitarios para transporte de pasajeros, categorias M1 de mas de 8 y hasta 15 asientos y que no supere los 3.500 kg. ",
    "B": "Vehiculos utilitarios para transporte de pasajeros, categoria M1 y M2 de mas de 15 y hasta 29 asientos, de 2 ees y que no supere 5.000 kg ",
    "C": "Vehiculos utilitarios para transporte de pasajeros, categoria M3 superan los} 5.000 kg., con 2 ejes.",
    "D": "Vehiculos utilitarios para transporte de pasajeros, categoria M3 superan los 15.000 kg., con 3 ejes.",
    "E": "Vehiculos utilizados para el transporte de carga, categorias N y N1. La primera hace referencia los vehiculos de hasta 1.000 kg, y la segunda se refiere a vehiculos que no superen los 3.500 kg.",
    "F": "Vehiculos utilizados para el transporte de carga, categorias N2 que carguen mas de 3.500 kg., que no superen los 12.000 kg.",
    "G": "Vehiculos utilizados para el transporte de carga, categorias N3 que supere los 12,000 kg. De carga. ",
    "H": """Vehiculos acoplados y semiacoplados utilizados para el transporte de cargas
categorias O y O1. La primera corresponde a vehiculos acoplados incluyendo
semiacopados; y la segunda a vehiculos acoplados con un eje que no sea
semiacoplados y que su carga no exceda los 750 kg. Vehiculos acoplados
semiacoplados utilizados para el transporte de carga, categorias 02, 03 y 04,
La primera hace referencia a vehiculos acoplados que no excedan los 3.500 kg
que no correspondan a la categoria O1. La segunda corresponde a vehiculos
que superen los 3.500 kg y que no excedan los 10.000; y por ultimo vehiculos
que superen los 10.000 kg. """,
    "I": "Equipos Especiales",
    "Z": "Vehiculos Uso Particular",
    "Exentos": "",
}

# TALLERES_NQN_CHOICES = map_fields([], TalleresNQN)
# TALLERES_RN_CHOICES = map_fields([], TalleresRN)
