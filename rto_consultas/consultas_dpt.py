import os
import requests
from dataclasses import dataclass, asdict
import json
from .logging import configure_logger
LOG_FILE = os.environ["LOG_FILE"]
logger = configure_logger(LOG_FILE)

# client.headers.update({"Authorization": TOKEN_AUTH})

# COMO HAGO PARA LLAMAR A LA API?
@dataclass
class DPTResponse:
    dominio: str
    dominioprov:str
    tipo:str
    fechainsc:str
    anio:str
    interno:str
    capacidad:str
    marca:str
    numchasis:str
    modelochasis:str
    marcachasis:str
    motornum:str
    empresa:str
    domicilio:str
    codpostal:str
    localidad:str
    responsable:str
    dnirespon:str
    domicrespon:str
    telrespon:str

    dict = asdict

def query_dpt(dominio: dict) -> DPTResponse:
    logger.info(f"DOMINIO => {dominio}")
    client = requests.Session()

    endpoint = "http://10.0.0.17:60000/dpt_request"
    client.headers.update({"Content-Type": "application/json"})
    data = {"dominio":dominio['dominio'],"mode":"Vehiculos"}

    response = client.get(endpoint, data=data)
    logger.debug(f"DPT RESPONSE => {response}")

    dpt_response = json.loads(response.json()["Respuesta"])

    return DPTResponse(**dpt_response)
