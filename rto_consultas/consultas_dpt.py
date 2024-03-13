import os
from typing import Union
import requests
from dataclasses import dataclass, asdict
import json
from .logging import configure_logger

LOG_FILE = os.environ["LOG_FILE"]
logger = configure_logger(LOG_FILE)

# client.headers.update({"Authorization": TOKEN_AUTH})

@dataclass
class DPTResponse:
    Dominio: str
    DominioProv: str
    Tipo: str
    FechaInsc: str
    Anio: str
    Interno: str
    Capacidad: str
    Marca: str
    NumChasis: str
    ModeloChasis: str
    MarcaChasis: str
    MotorNum: str
    Empresa: str
    Domicilio: str
    CodPostal: str
    Localidad: str
    Responsable: str
    DNIRespon: str
    DomicRespon: str
    TelRespon: str

    dict = asdict


@dataclass
class HabsResponse:
    Hoy: str
    InicHabilit: str
    NumHabilit: str
    VehiAnio: str
    VehiCapac: str
    VehiInt: str
    VehiPat: str
    VtoHabilit: str
    VtoRevTec: str
    VtoSeguro: str

    dict = asdict


API_MODES = {"1": "Vehiculos", "2": "Habilitaciones"}


def query_dpt(form_data: dict) -> Union[DPTResponse, HabsResponse]:
    logger.info(f"DOMINIO => {form_data}")
    client = requests.Session()

    consulta = API_MODES[form_data["consulta"]]

    endpoint = "http://10.0.0.17:60000/dpt_request"
    client.headers.update({"Content-Type": "application/json"})
    data = {"dominio": form_data["dominio"], "mode": consulta}

    response = client.get(endpoint, data=data)
    logger.debug(f"DPT RESPONSE => {response}")

    dpt_response = json.loads(response.json()["Respuesta"])
    # dpt_response = json.loads(response.json())
    # dpt_response = response.json()
    logger.debug(f"INFO => {dpt_response}")

    match consulta:
        case "Vehiculos":
            return DPTResponse(**dpt_response)
        case "Habilitaciones":
            return HabsResponse(**dpt_response)
        # just to please the linter
        case _:
            return HabsResponse(**dpt_response)
