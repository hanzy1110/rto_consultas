date_from="2023-01-01"
date_to="2023-07-01"
URL_TRANSPORTE="http://10.0.0.3:8000/resumen/transporte?idtipouso=3&fecha_desde=${date_from}&fecha_hasta=${date_to}&_export=csv"
URL_CARGA="http://10.0.0.3:8000/resumen/transporte?idtipouso=2&fecha_desde=${date_from}&fecha_hasta=${date_to}&_export=csv"

curl -X GET "$URL_TRANSPORTE" >transporte.csv
curl -X GET "$URL_CARGA" >carga.csv
