mkdir ./dataset
echo "DESCARGA 2015"
echo '--------x-------'
curl -v "http://10.0.0.3:8000/verificaciones/resumen?fecha_desde=2015-01-01&fecha_hasta=2015-12-31&_export=csv" >dataset/tables_2015.csv
echo "DESCARGA 2016"
echo '--------x-------'
curl -v "http://10.0.0.3:8000/verificaciones/resumen?fecha_desde=2016-01-01&fecha_hasta=2016-12-31&_export=csv" >dataset/tables_2016.csv
echo "DESCARGA 2017"
echo '--------x-------'
curl -v "http://10.0.0.3:8000/verificaciones/resumen?fecha_desde=2017-01-01&fecha_hasta=2017-12-31&_export=csv" >dataset/tables_2017.csv
echo "DESCARGA 2018"
echo '--------x-------'
curl -v "http://10.0.0.3:8000/verificaciones/resumen?fecha_desde=2018-01-01&fecha_hasta=2018-12-31&_export=csv" >dataset/tables_2018.csv
echo "DESCARGA 2019"
echo '--------x-------'
curl -v "http://10.0.0.3:8000/verificaciones/resumen?fecha_desde=2019-01-01&fecha_hasta=2019-12-31&_export=csv" >dataset/tables_2019.csv
echo "DESCARGA 2020"
echo '--------x-------'
curl -v "http://10.0.0.3:8000/verificaciones/resumen?fecha_desde=2020-01-01&fecha_hasta=2020-12-31&_export=csv" >dataset/tables_2020.csv
echo "DESCARGA 2021"
echo '--------x-------'
curl -v "http://10.0.0.3:8000/verificaciones/resumen?fecha_desde=2021-01-01&fecha_hasta=2021-12-31&_export=csv" >dataset/tables_2021.csv
echo "DESCARGA 2022"
echo '--------x-------'
curl -v "http://10.0.0.3:8000/verificaciones/resumen?fecha_desde=2022-01-01&fecha_hasta=2022-12-31&_export=csv" >dataset/tables_2022.csv
