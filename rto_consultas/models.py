# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

tipo_uso_dict = {
    1: "Particular",
    2: "Transporte Pasajeros",
    3: "Transporte Carga",
    4: "Municipal",
}


class Adjuntos(models.Model):
    idarchivo = models.IntegerField(
        db_column="idArchivo", primary_key=True
    )  # Field name made lowercase.
    nombre = models.CharField(
        db_column="Nombre", max_length=200
    )  # Field name made lowercase.
    idverificacion = models.IntegerField(
        db_column="idVerificacion"
    )  # Field name made lowercase.
    idtaller = models.IntegerField(db_column="idTaller")  # Field name made lowercase.
    fechacarga = models.DateField(db_column="FechaCarga")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "adjuntos"
        unique_together = (("idarchivo", "idtaller"),)


class Adjuntosauditoria(models.Model):
    idauditoria = models.ForeignKey(
        "Auditorias", on_delete=models.CASCADE, db_column="idAuditoria"
    )  # Field name made lowercase.
    idtaller = models.IntegerField(db_column="idTaller")  # Field name made lowercase.
    archivo = models.CharField(
        db_column="Archivo", max_length=200
    )  # Field name made lowercase.
    fechacarga = models.DateField(db_column="FechaCarga")  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "adjuntosauditoria"


class Adjuntosexcepcion(models.Model):
    idadjuntosexcepcion = models.IntegerField(
        db_column="idAdjuntosExcepcion", primary_key=True
    )  # Field name made lowercase.
    idexcepcion = models.ForeignKey(
        "Excepcion", on_delete=models.CASCADE, db_column="idExcepcion"
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        "Talleres", on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    archivo = models.CharField(max_length=255)
    fechacarga = models.DateField(db_column="fechaCarga")  # Field name made lowercase.
    replicado = models.IntegerField()
    activo = models.IntegerField()

    class Meta:
        app_label = "rto_consultas"

        db_table = "adjuntosexcepcion"


class Adjuntosmantenimientos(models.Model):
    idmantenimiento = models.IntegerField(
        db_column="idMantenimiento"
    )  # Field name made lowercase.
    idtaller = models.IntegerField(db_column="idTaller")  # Field name made lowercase.
    archivo = models.CharField(
        db_column="Archivo", max_length=200
    )  # Field name made lowercase.
    fechacarga = models.DateField(db_column="FechaCarga")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "adjuntosmantenimientos"


class Adjuntospendientes(models.Model):
    idarchivo = models.IntegerField(
        db_column="idArchivo", primary_key=True
    )  # Field name made lowercase.
    nombre = models.CharField(
        db_column="Nombre", max_length=200
    )  # Field name made lowercase.
    idpendiente = models.IntegerField(
        db_column="idPendiente"
    )  # Field name made lowercase.
    idtaller = models.IntegerField(db_column="idTaller")  # Field name made lowercase.
    fechacarga = models.DateField(db_column="FechaCarga")  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.
    activo = models.IntegerField(db_column="Activo")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "adjuntospendientes"
        unique_together = (("idarchivo", "idtaller"),)


class Adjuntosprorroga(models.Model):
    idadjuntosprorroga = models.IntegerField(
        db_column="idAdjuntosProrroga", primary_key=True
    )  # Field name made lowercase.
    idprorroga = models.ForeignKey(
        "Prorroga", on_delete=models.CASCADE, db_column="idProrroga"
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        "Talleres", on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    archivo = models.CharField(max_length=255)
    fechacarga = models.DateField(db_column="fechaCarga")  # Field name made lowercase.
    replicado = models.IntegerField()
    activo = models.IntegerField()

    class Meta:
        app_label = "rto_consultas"

        db_table = "adjuntosprorroga"


class Administrativos(models.Model):
    idadministrativo = models.IntegerField(
        db_column="idAdministrativo", primary_key=True
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        "Talleres", on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    apellido = models.CharField(
        db_column="Apellido", max_length=50
    )  # Field name made lowercase.
    nombre = models.CharField(
        db_column="Nombre", max_length=50
    )  # Field name made lowercase.
    fechadesde = models.DateField(db_column="FechaDesde")  # Field name made lowercase.
    fechahasta = models.DateField(
        db_column="FechaHasta", blank=True, null=True
    )  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.
    cuit = models.CharField(
        db_column="Cuit", max_length=15
    )  # Field name made lowercase.
    usuario = models.CharField(
        db_column="Usuario", max_length=50
    )  # Field name made lowercase.
    claveinicial = models.CharField(
        db_column="ClaveInicial", max_length=100
    )  # Field name made lowercase.
    activo = models.IntegerField(db_column="Activo")  # Field name made lowercase.
    replicado = models.IntegerField(db_column="Replicado")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "administrativos"
        unique_together = (("idadministrativo", "idtaller"),)


class Administrativosusuarios(models.Model):
    idtaller = models.IntegerField(
        db_column="idTaller", primary_key=True
    )  # Field name made lowercase.
    idusuario = models.IntegerField(db_column="idUsuario")  # Field name made lowercase.
    idadministrativo = models.IntegerField(
        db_column="idAdministrativo"
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "administrativosusuarios"
        unique_together = (("idtaller", "idusuario", "idadministrativo"),)


class Auditorias(models.Model):
    idauditoria = models.IntegerField(
        db_column="idAuditoria", primary_key=True
    )  # Field name made lowercase.
    idtaller = models.IntegerField(db_column="idTaller")  # Field name made lowercase.
    fecha = models.DateField(db_column="Fecha")  # Field name made lowercase.
    observaciones = models.TextField(
        db_column="Observaciones"
    )  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "auditorias"
        unique_together = (("idauditoria", "idtaller"),)


class Auditoriasequipos(models.Model):
    idauditoria = models.OneToOneField(
        Auditorias, on_delete=models.CASCADE, db_column="idAuditoria", primary_key=True
    )  # Field name made lowercase.
    idtaller = models.IntegerField(db_column="idTaller")  # Field name made lowercase.
    idequipo = models.ForeignKey(
        "Equipos", on_delete=models.CASCADE, db_column="idEquipo"
    )  # Field name made lowercase.
    funcionamientocorrecto = models.IntegerField(
        db_column="FuncionamientoCorrecto"
    )  # Field name made lowercase.
    observaciones = models.CharField(
        db_column="Observaciones", max_length=500
    )  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "auditoriasequipos"
        unique_together = (("idauditoria", "idtaller", "idequipo"),)


# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)

#     class Meta:
#         app_label = 'rto_consultas'

#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE)
#     permission = models.ForeignKey('AuthPermission', on_delete=models.CASCADE)

#     class Meta:
#         app_label = 'rto_consultas'

#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', on_delete=models.CASCADE)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         app_label = 'rto_consultas'

#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()

#     class Meta:
#         app_label = 'rto_consultas'

#         db_table = 'auth_user'


# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
#     group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE)

#     class Meta:
#         app_label = 'rto_consultas'

#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
#     permission = models.ForeignKey(AuthPermission, on_delete=models.CASCADE)

#     class Meta:
#         app_label = 'rto_consultas'

#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)


class Categorias(models.Model):
    idcategoria = models.AutoField(
        db_column="idCategoria", primary_key=True
    )  # Field name made lowercase.
    tipouso = models.CharField(
        db_column="tipoUso", max_length=11
    )  # Field name made lowercase.
    tipovehiculo = models.CharField(
        db_column="tipoVehiculo", max_length=100
    )  # Field name made lowercase.
    categoria = models.CharField(
        db_column="Categoria", max_length=100
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=100
    )  # Field name made lowercase.
    rangos = models.CharField(
        db_column="Rangos", max_length=200
    )  # Field name made lowercase.
    activa = models.IntegerField(db_column="Activa")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "categorias"


class Categoriastalleres(models.Model):
    idcategoria = models.OneToOneField(
        Categorias, on_delete=models.CASCADE, db_column="idCategoria", primary_key=True
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        "Talleres", on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    porcentaje = models.DecimalField(
        db_column="Porcentaje", max_digits=10, decimal_places=2
    )  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "categoriastalleres"
        unique_together = (("idcategoria", "idtaller"),)


class CccfAdjuntoscertificados(models.Model):
    idadjunto = models.AutoField(
        db_column="idAdjunto", primary_key=True
    )  # Field name made lowercase.
    idcertificado = models.IntegerField(
        db_column="idCertificado"
    )  # Field name made lowercase.
    nombrearchivo = models.CharField(
        db_column="NombreArchivo", max_length=200
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "cccf_adjuntoscertificados"


class CccfCertificadoexcesos(models.Model):
    idcertificadoexceso = models.AutoField(
        db_column="idCertificadoExceso", primary_key=True
    )  # Field name made lowercase.
    idcertificado = models.ForeignKey(
        "CccfCertificados", on_delete=models.CASCADE, db_column="idCertificado"
    )  # Field name made lowercase.
    numero = models.PositiveIntegerField(
        db_column="Numero"
    )  # Field name made lowercase.
    fecha = models.DateField(db_column="Fecha")  # Field name made lowercase.
    hora = models.TimeField(db_column="Hora")  # Field name made lowercase.
    velocidadsobrepaso = models.FloatField(
        db_column="VelocidadSobrepaso"
    )  # Field name made lowercase.
    tiempovelocidadexceso = models.CharField(
        db_column="TiempoVelocidadExceso", max_length=50
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "cccf_certificadoexcesos"


class CccfCertificados(models.Model):
    idcertificado = models.AutoField(
        db_column="idCertificado", primary_key=True
    )  # Field name made lowercase.
    nrocertificado = models.BigIntegerField(
        db_column="NroCertificado", unique=True
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        "CccfTalleres", on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    fechahoracarga = models.DateTimeField(
        db_column="FechaHoraCarga"
    )  # Field name made lowercase.
    fechacalibracion = models.DateField(
        db_column="FechaCalibracion"
    )  # Field name made lowercase.
    fechavencimiento = models.DateField(
        db_column="FechaVencimiento"
    )  # Field name made lowercase.
    idempresa = models.ForeignKey(
        "CccfEmpresas", on_delete=models.CASCADE, db_column="idEmpresa"
    )  # Field name made lowercase.
    propusuario = models.CharField(
        db_column="PropUsuario", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    dominio = models.CharField(
        db_column="Dominio", max_length=10
    )  # Field name made lowercase.
    nrointerno = models.CharField(
        db_column="NroInterno", max_length=50
    )  # Field name made lowercase.
    kilometraje = models.IntegerField(
        db_column="Kilometraje"
    )  # Field name made lowercase.
    tacmarca = models.CharField(
        db_column="TacMarca", max_length=50
    )  # Field name made lowercase.
    tactipo = models.CharField(
        db_column="TacTipo", max_length=50
    )  # Field name made lowercase.
    tacmodelo = models.CharField(
        db_column="TacModelo", max_length=50
    )  # Field name made lowercase.
    tacnroserie = models.CharField(
        db_column="TacNroSerie", max_length=50
    )  # Field name made lowercase.
    relw = models.CharField(
        db_column="RelW", max_length=50
    )  # Field name made lowercase.
    constantek = models.CharField(
        db_column="ConstanteK", max_length=50
    )  # Field name made lowercase.
    rodado_eje1 = models.CharField(
        db_column="Rodado_Eje1", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    rodado_eje2 = models.CharField(
        db_column="Rodado_Eje2", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    rodado_eje3 = models.CharField(
        db_column="Rodado_Eje3", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    rodado_eje4 = models.CharField(
        db_column="Rodado_Eje4", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    rodado_eje5 = models.CharField(
        db_column="Rodado_Eje5", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    precinto = models.CharField(
        db_column="Precinto", max_length=50
    )  # Field name made lowercase.
    impresora = models.CharField(
        db_column="Impresora", max_length=50
    )  # Field name made lowercase.
    nroinforme = models.CharField(
        db_column="NroInforme", max_length=50
    )  # Field name made lowercase.
    canthojas = models.CharField(
        db_column="CantHojas", max_length=50
    )  # Field name made lowercase.
    observaciones = models.TextField(
        db_column="Observaciones"
    )  # Field name made lowercase.
    usuario = models.CharField(max_length=50)
    idestado = models.IntegerField(db_column="idEstado")  # Field name made lowercase.
    fechaanulacion = models.DateField(
        db_column="FechaAnulacion", blank=True, null=True
    )  # Field name made lowercase.
    observacionesanulacion = models.TextField(
        db_column="ObservacionesAnulacion", blank=True, null=True
    )  # Field name made lowercase.
    patentemercosur = models.IntegerField(
        db_column="PatenteMercosur"
    )  # Field name made lowercase.
    cbverificador = models.CharField(
        db_column="CBVerificador", max_length=24, blank=True, null=True
    )  # Field name made lowercase.
    sinexcesos = models.IntegerField(
        db_column="SinExcesos", blank=True, null=True
    )  # Field name made lowercase.
    desconexioncantidad = models.IntegerField(
        db_column="DesconexionCantidad"
    )  # Field name made lowercase.
    desconexionhora = models.FloatField(
        db_column="DesconexionHora"
    )  # Field name made lowercase.
    aperturaequipo = models.IntegerField(
        db_column="AperturaEquipo"
    )  # Field name made lowercase.
    retiroelementograbacion = models.IntegerField(
        db_column="RetiroElementoGrabacion"
    )  # Field name made lowercase.
    fallasdispositivo = models.CharField(
        db_column="FallasDispositivo", max_length=500
    )  # Field name made lowercase.
    faltainformacion = models.CharField(
        db_column="FaltaInformacion", max_length=50
    )  # Field name made lowercase.
    cb = models.CharField(
        db_column="CB", max_length=50, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "cccf_certificados"


class CccfEmpresas(models.Model):
    idempresa = models.AutoField(
        db_column="idEmpresa", primary_key=True
    )  # Field name made lowercase.
    cuit = models.BigIntegerField(
        db_column="CUIT", unique=True
    )  # Field name made lowercase.
    razonsocial = models.CharField(
        db_column="RazonSocial", max_length=150
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "cccf_empresas"


class CccfEstados(models.Model):
    idestado = models.IntegerField(
        db_column="idEstado", primary_key=True
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=50
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "cccf_estados"


class CccfNroscertificadosasignados(models.Model):
    nrocertificado = models.BigIntegerField(
        db_column="NroCertificado", primary_key=True
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        "CccfTalleres", on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    fechacarga = models.DateField(db_column="FechaCarga")  # Field name made lowercase.
    disponible = models.IntegerField(
        db_column="Disponible"
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "cccf_nroscertificadosasignados"


class CccfTalleres(models.Model):
    idtaller = models.AutoField(
        db_column="idTaller", primary_key=True
    )  # Field name made lowercase.
    nrotaller = models.IntegerField(db_column="NroTaller")  # Field name made lowercase.
    nombre = models.CharField(
        db_column="Nombre", max_length=100
    )  # Field name made lowercase.
    cuit = models.CharField(
        db_column="CUIT", max_length=30, blank=True, null=True
    )  # Field name made lowercase.
    idlocalidad = models.IntegerField(
        db_column="idLocalidad", blank=True, null=True
    )  # Field name made lowercase.
    domicilio = models.CharField(
        db_column="Domicilio", max_length=250, blank=True, null=True
    )  # Field name made lowercase.
    activo = models.IntegerField(db_column="Activo")  # Field name made lowercase.
    fechabaja = models.DateField(
        db_column="FechaBaja", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "cccf_talleres"


class CccfUsuarios(models.Model):
    idusuario = models.AutoField(
        db_column="idUsuario", primary_key=True
    )  # Field name made lowercase.
    usuario = models.CharField(
        db_column="Usuario", unique=True, max_length=50
    )  # Field name made lowercase.
    clave = models.CharField(
        db_column="Clave", max_length=100
    )  # Field name made lowercase.
    idperfil = models.IntegerField(db_column="idPerfil")  # Field name made lowercase.
    apellido = models.CharField(
        db_column="Apellido", max_length=50
    )  # Field name made lowercase.
    nombre = models.CharField(
        db_column="Nombre", max_length=50
    )  # Field name made lowercase.
    email = models.CharField(
        db_column="Email", max_length=100
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        CccfTalleres,
        on_delete=models.CASCADE,
        db_column="idTaller",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    activo = models.IntegerField(db_column="Activo")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "cccf_usuarios"


class Certificados(models.Model):
    idcertificado = models.IntegerField(
        db_column="idCertificado", primary_key=True
    )  # Field name made lowercase.
    nrocertificado = models.BigIntegerField(
        db_column="NroCertificado"
    )  # Field name made lowercase.
    fecha = models.DateField(db_column="Fecha")  # Field name made lowercase.
    hora = models.TimeField(db_column="Hora")  # Field name made lowercase.
    idtaller = models.ForeignKey(
        "Talleres", on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    idestado = models.IntegerField(db_column="idEstado")  # Field name made lowercase.
    vigenciahasta = models.DateField(
        db_column="VigenciaHasta"
    )  # Field name made lowercase.
    idverificacion = models.ForeignKey(
        "rto_consultas.Verificaciones",
        on_delete=models.CASCADE,
        db_column="idVerificacion",
        related_name="certificados"
    )  # Field name made lowercase.
    idconvenio = models.ForeignKey(
        "Convenios",
        on_delete=models.CASCADE,
        db_column="idConvenio",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    anulado = models.IntegerField(db_column="Anulado")  # Field name made lowercase.
    fechaanulacion = models.DateField(
        db_column="FechaAnulacion", blank=True, null=True
    )  # Field name made lowercase.
    horaanulacion = models.TimeField(
        db_column="HoraAnulacion", blank=True, null=True
    )  # Field name made lowercase.
    observaciones = models.TextField(
        db_column="Observaciones", blank=True, null=True
    )  # Field name made lowercase.
    auditoria = models.TextField(
        db_column="Auditoria", blank=True, null=True
    )  # Field name made lowercase.
    serie = models.CharField(
        db_column="Serie", max_length=1
    )  # Field name made lowercase.
    idcategoria = models.IntegerField(
        db_column="idCategoria", blank=True, null=True
    )  # Field name made lowercase.
    porcentajecategoria = models.DecimalField(
        db_column="porcentajeCategoria",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.
    vencido = models.IntegerField(db_column="Vencido")  # Field name made lowercase.
    reverificado = models.IntegerField(
        db_column="Reverificado"
    )  # Field name made lowercase.
    idhabf1 = models.IntegerField(
        db_column="idHabF1", blank=True, null=True
    )  # Field name made lowercase.
    idhabf2 = models.IntegerField(
        db_column="idHabF2", blank=True, null=True
    )  # Field name made lowercase.
    intentosobtencionhab = models.IntegerField(
        db_column="IntentosObtencionHab", blank=True, null=True
    )  # Field name made lowercase.

    def __str__(self) -> str:
        return f"CERT {self.nrocertificado} - {self.idcertificado} -"

    class Meta:
        app_label = "rto_consultas"

        db_table = "certificados"
        unique_together = (("idcertificado", "idtaller"),)

        indexes = [
            models.Index(fields=("idcertificado", "idtaller")),
            models.Index(fields=("idverificacion",)),
            models.Index(fields=("idtaller",)),
        ]


class Certificadosasignadosportaller(models.Model):
    nrocertificado = models.BigIntegerField(
        db_column="NroCertificado", primary_key=True
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        "Talleres", on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    fechacarga = models.DateField(db_column="FechaCarga")  # Field name made lowercase.
    disponible = models.IntegerField(
        db_column="Disponible"
    )  # Field name made lowercase.
    replicado = models.IntegerField(db_column="Replicado")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "certificadosasignadosportaller"


class Clasesservicios(models.Model):
    idclaseservicio = models.AutoField(
        db_column="idClaseServicio", primary_key=True
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=200
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "clasesservicios"


class Convenios(models.Model):
    idconvenio = models.AutoField(
        db_column="idConvenio", primary_key=True
    )  # Field name made lowercase.
    nroconvenio = models.IntegerField(
        db_column="NroConvenio", unique=True
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=500
    )  # Field name made lowercase.
    idprovincia = models.ForeignKey(
        "Provincias", on_delete=models.CASCADE, db_column="idProvincia"
    )  # Field name made lowercase.
    formula = models.CharField(
        db_column="Formula", max_length=100
    )  # Field name made lowercase.
    vigente = models.IntegerField(db_column="Vigente")  # Field name made lowercase.
    leyaplica = models.CharField(
        db_column="LeyAplica", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    imagen = models.CharField(
        db_column="Imagen", max_length=100, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "convenios"


class Defectos(models.Model):
    iddefecto = models.AutoField(
        db_column="idDefecto", primary_key=True
    )  # Field name made lowercase.
    codigo = models.CharField(
        db_column="Codigo",
        unique=True,
        max_length=10,
        db_collation="utf8mb3_general_ci",
    )  # Field name made lowercase.
    idrubro = models.ForeignKey(
        "Rubrosdefectos", on_delete=models.CASCADE, db_column="idRubro"
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=250, db_collation="utf8mb3_general_ci"
    )  # Field name made lowercase.
    activo = models.IntegerField(db_column="Activo")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "defectos"


class Direcotrestecnicos(models.Model):
    iddirector = models.IntegerField(
        db_column="idDirector", primary_key=True
    )  # Field name made lowercase.
    apellido = models.CharField(
        db_column="Apellido", max_length=50
    )  # Field name made lowercase.
    nombre = models.CharField(
        db_column="Nombre", max_length=50
    )  # Field name made lowercase.
    matricula = models.CharField(
        db_column="Matricula", max_length=50
    )  # Field name made lowercase.
    curriculum = models.CharField(
        db_column="Curriculum", max_length=200
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        "Talleres", on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    fechadesde = models.DateField(db_column="FechaDesde")  # Field name made lowercase.
    fechahasta = models.DateField(
        db_column="FechaHasta", blank=True, null=True
    )  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.
    cuit = models.CharField(
        db_column="Cuit", max_length=15
    )  # Field name made lowercase.
    usuario = models.CharField(
        db_column="Usuario", max_length=50
    )  # Field name made lowercase.
    claveinicial = models.CharField(
        db_column="ClaveInicial", max_length=100
    )  # Field name made lowercase.
    activo = models.IntegerField(db_column="Activo")  # Field name made lowercase.
    replicado = models.IntegerField(db_column="Replicado")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "direcotrestecnicos"
        unique_together = (("iddirector", "idtaller"),)


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', on_delete=models.CASCADE, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)

#     class Meta:
#         app_label = 'rto_consultas'

#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         app_label = 'rto_consultas'

#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         app_label = 'rto_consultas'

#         db_table = 'django_migrations'


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()

#     class Meta:
#         app_label = 'rto_consultas'

#         db_table = 'django_session'


class Equipos(models.Model):
    idequipo = models.IntegerField(
        db_column="idEquipo", primary_key=True
    )  # Field name made lowercase.
    nroserie = models.CharField(
        db_column="NroSerie", max_length=50
    )  # Field name made lowercase.
    tipo = models.CharField(
        db_column="Tipo", max_length=50
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=100
    )  # Field name made lowercase.
    marca = models.CharField(
        db_column="Marca", max_length=50
    )  # Field name made lowercase.
    modelo = models.CharField(
        db_column="Modelo", max_length=50
    )  # Field name made lowercase.
    nrointerno = models.CharField(
        db_column="NroInterno", max_length=20
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        "Talleres", on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    nrolinea = models.IntegerField(
        db_column="NroLinea", blank=True, null=True
    )  # Field name made lowercase.
    periodicidadmantenimiento = models.IntegerField(
        db_column="PeriodicidadMantenimiento"
    )  # Field name made lowercase.
    activo = models.IntegerField(db_column="Activo")  # Field name made lowercase.
    fechabaja = models.DateField(
        db_column="FechaBaja", blank=True, null=True
    )  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "equipos"
        unique_together = (("idequipo", "idtaller"),)


class Estados(models.Model):
    idestado = models.AutoField(
        db_column="idEstado", primary_key=True,verbose_name="Estado Certificado"
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=100
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "estados"
        indexes = [
            models.Index(fields=("idestado",)),
        ]

    def __str__(self) -> str:
        return f"{self.descripcion}"


class Estadosequipo(models.Model):
    idestado = models.AutoField(
        db_column="idEstado", primary_key=True
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=50
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "estadosequipo"


class Excepcion(models.Model):
    idexcepcion = models.IntegerField(
        db_column="idExcepcion", primary_key=True
    )  # Field name made lowercase.
    replicado = models.IntegerField(blank=True, null=True)
    modificado = models.IntegerField()
    fechahoramodificacion = models.DateField(
        db_column="fechaHoraModificacion", blank=True, null=True
    )  # Field name made lowercase.
    historialmodificacion = models.TextField(
        db_column="historialModificacion", blank=True, null=True
    )  # Field name made lowercase.
    dominio = models.CharField(max_length=10)
    marcavehiculo = models.CharField(
        db_column="marcaVehiculo", max_length=255
    )  # Field name made lowercase.
    modelovehiculo = models.CharField(
        db_column="modeloVehiculo", max_length=255
    )  # Field name made lowercase.
    idlocalidadvehiculo = models.IntegerField(
        db_column="idLocalidadVehiculo"
    )  # Field name made lowercase.
    nombretitular = models.CharField(
        db_column="nombreTitular", max_length=255
    )  # Field name made lowercase.
    apellidotitular = models.CharField(
        db_column="apellidoTitular", max_length=255
    )  # Field name made lowercase.
    domiciliotitular = models.CharField(
        db_column="domicilioTitular", max_length=255
    )  # Field name made lowercase.
    idlocalidadtitular = models.IntegerField(
        db_column="idLocalidadTitular"
    )  # Field name made lowercase.
    nombreconductor = models.CharField(
        db_column="nombreConductor", max_length=255
    )  # Field name made lowercase.
    apellidoconductor = models.CharField(
        db_column="apellidoConductor", max_length=255
    )  # Field name made lowercase.
    domicilioconductor = models.CharField(
        db_column="domicilioConductor", max_length=255
    )  # Field name made lowercase.
    idlocalidadconductor = models.IntegerField(
        db_column="idLocalidadConductor"
    )  # Field name made lowercase.
    fecha = models.DateField()
    observacion = models.TextField()
    idtaller = models.IntegerField(db_column="idTaller")  # Field name made lowercase.
    activo = models.IntegerField()
    usuario = models.CharField(max_length=50)
    usuariodictamen = models.CharField(
        db_column="usuarioDictamen", max_length=50
    )  # Field name made lowercase.
    aprobado = models.IntegerField(blank=True, null=True)
    fechahoradictamen = models.DateTimeField(
        db_column="fechaHoraDictamen", blank=True, null=True
    )  # Field name made lowercase.
    observaciondictamen = models.TextField(
        db_column="observacionDictamen"
    )  # Field name made lowercase.
    idcategoria = models.IntegerField(
        db_column="idCategoria"
    )  # Field name made lowercase.
    chasisnro = models.CharField(
        db_column="chasisNro", max_length=50
    )  # Field name made lowercase.
    motoranio = models.IntegerField(db_column="motorAnio")  # Field name made lowercase.
    motormarca = models.CharField(
        db_column="motorMarca", max_length=50
    )  # Field name made lowercase.
    motornumero = models.CharField(
        db_column="motorNumero", max_length=50
    )  # Field name made lowercase.
    tipodocconductor = models.CharField(
        db_column="tipoDocConductor", max_length=10
    )  # Field name made lowercase.
    nrodocconductor = models.IntegerField(
        db_column="nroDocConductor"
    )  # Field name made lowercase.
    codigotitular = models.CharField(
        db_column="codigoTitular", max_length=12
    )  # Field name made lowercase.
    companiaseguro = models.CharField(
        db_column="companiaSeguro", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    nropoliza = models.CharField(
        db_column="nroPoliza", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    ultimorecpatente = models.CharField(
        db_column="ultimoRecPatente", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    idtipouso = models.IntegerField(db_column="idTipoUso")  # Field name made lowercase.
    idtipovehiculo = models.IntegerField(
        db_column="idTipoVehiculo", blank=True, null=True
    )  # Field name made lowercase.
    vanio = models.IntegerField(
        db_column="vAnio", blank=True, null=True
    )  # Field name made lowercase.
    chasismarca = models.CharField(
        db_column="chasisMarca", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    chasisanio = models.IntegerField(
        db_column="chasisAnio", blank=True, null=True
    )  # Field name made lowercase.
    tipocombustible = models.CharField(
        db_column="tipoCombustible", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    nroejes = models.IntegerField(
        db_column="nroEjes", blank=True, null=True
    )  # Field name made lowercase.
    tipodoctitular = models.CharField(
        db_column="tipoDocTitular", max_length=10
    )  # Field name made lowercase.
    nrodoctitular = models.IntegerField(
        db_column="nroDocTitular"
    )  # Field name made lowercase.
    telefonotitular = models.CharField(
        db_column="telefonoTitular", max_length=20
    )  # Field name made lowercase.
    tipopersona = models.CharField(
        db_column="tipoPersona", max_length=1
    )  # Field name made lowercase.
    razonsocialtitular = models.CharField(
        db_column="razonSocialTitular", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    cuittitular = models.CharField(
        db_column="cuitTitular", max_length=15, blank=True, null=True
    )  # Field name made lowercase.
    codigopjtitular = models.CharField(
        db_column="codigoPJTitular", max_length=30, blank=True, null=True
    )  # Field name made lowercase.
    emailtitular = models.CharField(
        db_column="emailTitular", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    notifyactive = models.IntegerField(
        db_column="notifyActive"
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "excepcion"
        unique_together = (("idexcepcion", "idtaller"),)


class Fotovalidacionpatente(models.Model):
    idfotovalidacion = models.IntegerField(
        db_column="idFotovalidacion", primary_key=True
    )  # Field name made lowercase.
    dominio = models.CharField(max_length=10)
    fechahora = models.DateTimeField(
        db_column="fechaHora"
    )  # Field name made lowercase.
    codigo = models.IntegerField(blank=True, null=True)
    resultado = models.CharField(max_length=200)
    path = models.CharField(max_length=100)
    idtaller = models.ForeignKey(
        "Talleres", on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    output = models.CharField(max_length=1024, blank=True, null=True)
    activo = models.IntegerField()
    fechahorarep = models.DateTimeField(
        db_column="fechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "fotovalidacionPatente"
        unique_together = (("idfotovalidacion", "idtaller"),)


class Habilitacion(models.Model):
    idhabilitacion = models.AutoField(
        db_column="idHabilitacion", primary_key=True
    )  # Field name made lowercase.
    nrocodigobarrashab = models.CharField(
        db_column="nroCodigoBarrasHab", max_length=255
    )  # Field name made lowercase.
    activo = models.IntegerField()
    fechahoracreacion = models.DateTimeField(
        db_column="fechaHoraCreacion"
    )  # Field name made lowercase.
    modificado = models.IntegerField()
    fechahoraultmodificacion = models.DateTimeField(
        db_column="fechaHoraUltModificacion"
    )  # Field name made lowercase.
    historialmodificacion = models.TextField(
        db_column="historialModificacion"
    )  # Field name made lowercase.
    dominio = models.CharField(max_length=10)
    marcavehiculo = models.CharField(
        db_column="marcaVehiculo", max_length=255
    )  # Field name made lowercase.
    modelovehiculo = models.CharField(
        db_column="modeloVehiculo", max_length=255
    )  # Field name made lowercase.
    idlocalidadvehiculo = models.IntegerField(
        db_column="idLocalidadVehiculo"
    )  # Field name made lowercase.
    nombretitular = models.CharField(
        db_column="nombreTitular", max_length=255
    )  # Field name made lowercase.
    apellidotitular = models.CharField(
        db_column="apellidoTitular", max_length=255
    )  # Field name made lowercase.
    domiciliotitular = models.CharField(
        db_column="domicilioTitular", max_length=255
    )  # Field name made lowercase.
    idlocalidadtitular = models.IntegerField(
        db_column="idLocalidadTitular"
    )  # Field name made lowercase.
    nombreconductor = models.CharField(
        db_column="nombreConductor", max_length=255
    )  # Field name made lowercase.
    apellidoconductor = models.CharField(
        db_column="apellidoConductor", max_length=255
    )  # Field name made lowercase.
    domicilioconductor = models.CharField(
        db_column="domicilioConductor", max_length=255
    )  # Field name made lowercase.
    idlocalidadconductor = models.IntegerField(
        db_column="idLocalidadConductor"
    )  # Field name made lowercase.
    usuariodictamen = models.CharField(
        db_column="usuarioDictamen", max_length=50
    )  # Field name made lowercase.
    fechahoradictamen = models.DateTimeField(
        db_column="fechaHoraDictamen"
    )  # Field name made lowercase.
    tipodoctitular = models.CharField(
        db_column="tipoDocTitular", max_length=10
    )  # Field name made lowercase.
    nrodoctitular = models.IntegerField(
        db_column="nroDocTitular"
    )  # Field name made lowercase.
    tipopersona = models.CharField(
        db_column="tipoPersona", max_length=1
    )  # Field name made lowercase.
    razonsocialtitular = models.CharField(
        db_column="razonSocialTitular", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    cuittitular = models.CharField(
        db_column="cuitTitular", max_length=15, blank=True, null=True
    )  # Field name made lowercase.
    idtiposervicio = models.IntegerField(
        db_column="idTipoServicio"
    )  # Field name made lowercase.
    nrocertificadocccf = models.CharField(
        db_column="NroCertificadoCCCF", max_length=50, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "habilitacion"


class Habsfinales(models.Model):
    idhabf = models.AutoField(
        db_column="idHabF", primary_key=True
    )  # Field name made lowercase.
    fh = models.DateTimeField(
        db_column="FH", blank=True, null=True
    )  # Field name made lowercase.
    dominiorto = models.CharField(
        db_column="DominioRTO", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    numpedido = models.CharField(
        db_column="NumPedido", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    dominio = models.CharField(max_length=50, blank=True, null=True)
    interno = models.CharField(max_length=50, blank=True, null=True)
    anio = models.CharField(max_length=50, blank=True, null=True)
    capacidad = models.CharField(max_length=50, blank=True, null=True)
    numhabil = models.CharField(max_length=50, blank=True, null=True)
    hab_fechaven = models.DateField(blank=True, null=True)
    seg_fechaven = models.DateField(blank=True, null=True)
    revfechaven = models.DateField(blank=True, null=True)
    hab_fechaini = models.DateField(blank=True, null=True)
    modalidad = models.CharField(max_length=256, blank=True, null=True)
    fechahoy = models.DateField(blank=True, null=True)

    class Meta:
        app_label = "rto_consultas"

        db_table = "habsfinales"


class Inspectores(models.Model):
    idinspector = models.IntegerField(
        db_column="idInspector", primary_key=True
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        "Talleres", on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    apellido = models.CharField(
        db_column="Apellido", max_length=50
    )  # Field name made lowercase.
    nombre = models.CharField(
        db_column="Nombre", max_length=50
    )  # Field name made lowercase.
    matricula = models.CharField(
        db_column="Matricula", max_length=50
    )  # Field name made lowercase.
    curriculum = models.CharField(
        db_column="Curriculum", max_length=200
    )  # Field name made lowercase.
    fechadesde = models.DateField(db_column="FechaDesde")  # Field name made lowercase.
    fechahasta = models.DateField(
        db_column="FechaHasta", blank=True, null=True
    )  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.
    cuit = models.CharField(
        db_column="Cuit", max_length=15
    )  # Field name made lowercase.
    usuario = models.CharField(
        db_column="Usuario", max_length=50
    )  # Field name made lowercase.
    claveinicial = models.CharField(
        db_column="ClaveInicial", max_length=100
    )  # Field name made lowercase.
    activo = models.IntegerField(db_column="Activo")  # Field name made lowercase.
    replicado = models.IntegerField(db_column="Replicado")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "inspectores"
        unique_together = (("idinspector", "idtaller"),)


class Inspectoresusuarios(models.Model):
    idtaller = models.IntegerField(
        db_column="idTaller", primary_key=True
    )  # Field name made lowercase.
    idusuario = models.IntegerField(db_column="idUsuario")  # Field name made lowercase.
    idinspector = models.IntegerField(
        db_column="idInspector"
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "inspectoresusuarios"
        unique_together = (("idtaller", "idusuario", "idinspector"),)


class Instalaciones(models.Model):
    idinstalacion = models.AutoField(
        db_column="idInstalacion", primary_key=True
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=200
    )  # Field name made lowercase.
    activo = models.IntegerField(db_column="Activo")  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        "Talleres", on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    replicado = models.IntegerField(db_column="Replicado")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "instalaciones"
        unique_together = (("idinstalacion", "idtaller"),)


class Lineasequipos(models.Model):
    idequipo = models.IntegerField(
        db_column="idEquipo", primary_key=True
    )  # Field name made lowercase.
    idtaller = models.IntegerField(db_column="idTaller")  # Field name made lowercase.
    nrolinea = models.IntegerField(db_column="NroLinea")  # Field name made lowercase.
    fechadesde = models.DateField(db_column="FechaDesde")  # Field name made lowercase.
    fechahasta = models.DateField(
        db_column="FechaHasta", blank=True, null=True
    )  # Field name made lowercase.
    observaciones = models.TextField(
        db_column="Observaciones", blank=True, null=True
    )  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "lineasequipos"
        unique_together = (("idequipo", "idtaller", "nrolinea", "fechadesde"),)


class Lineastaller(models.Model):
    nrolinea = models.IntegerField(
        db_column="NroLinea", primary_key=True
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        "Talleres", on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=100
    )  # Field name made lowercase.
    replicado = models.IntegerField(db_column="Replicado")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "lineastaller"
        unique_together = (("nrolinea", "idtaller"),)


class Localidades(models.Model):
    idlocalidad = models.AutoField(
        db_column="idLocalidad", primary_key=True
    )  # Field name made lowercase.
    idprovincia = models.ForeignKey(
        "Provincias", on_delete=models.CASCADE, db_column="idProvincia"
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=100
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "localidades"
        indexes = [
            models.Index(fields=("idlocalidad",)),
        ]


class Mantenimientos(models.Model):
    idmantenimiento = models.IntegerField(
        db_column="idMantenimiento", primary_key=True
    )  # Field name made lowercase.
    idequipo = models.ForeignKey(
        Equipos, on_delete=models.CASCADE, db_column="idEquipo"
    )  # Field name made lowercase.
    fecha = models.DateField(db_column="Fecha")  # Field name made lowercase.
    observaciones = models.TextField(
        db_column="Observaciones"
    )  # Field name made lowercase.
    idtaller = models.IntegerField(db_column="idTaller")  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "mantenimientos"
        unique_together = (("idmantenimiento", "idtaller"),)


class Marcasautos(models.Model):
    idmarca = models.AutoField(
        db_column="idMarca", primary_key=True
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=100
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "marcasautos"


class Nivelesdefectos(models.Model):
    idnivel = models.IntegerField(
        db_column="idNivel", primary_key=True
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=10
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "nivelesdefectos"


class Noconformidades(models.Model):
    idnc = models.IntegerField(
        db_column="idNC", primary_key=True
    )  # Field name made lowercase.
    dominio = models.CharField(max_length=10)
    descripcionnc = models.CharField(
        db_column="descripcionNC", max_length=200
    )  # Field name made lowercase.
    fechahora = models.DateTimeField(
        db_column="fechaHora"
    )  # Field name made lowercase.
    idtaller = models.IntegerField(db_column="idTaller")  # Field name made lowercase.
    activo = models.IntegerField()
    fechahorarep = models.DateTimeField(
        db_column="fechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "noConformidades"
        unique_together = (("idnc", "idtaller"),)


class Parametros(models.Model):
    idparametro = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=200, db_collation="utf8mb3_general_ci")
    valor = models.CharField(max_length=200, db_collation="utf8mb3_general_ci")
    observaciones = models.TextField(db_collation="utf8mb3_general_ci")

    class Meta:
        app_label = "rto_consultas"

        db_table = "parametros"


class Pendientes(models.Model):
    idpendiente = models.IntegerField(
        db_column="idPendiente", primary_key=True
    )  # Field name made lowercase.
    fecha = models.DateField(db_column="Fecha")  # Field name made lowercase.
    hora = models.TimeField(db_column="Hora")  # Field name made lowercase.
    horafinal = models.TimeField(db_column="HoraFinal")  # Field name made lowercase.
    idtaller = models.IntegerField(db_column="idTaller")  # Field name made lowercase.
    idfotovalidacion = models.IntegerField(
        db_column="idFotovalidacion", blank=True, null=True
    )  # Field name made lowercase.
    idverificacion = models.IntegerField(
        db_column="idVerificacion", blank=True, null=True
    )  # Field name made lowercase.
    dominiovehiculo = models.CharField(
        db_column="DominioVehiculo", max_length=10
    )  # Field name made lowercase.
    idhabilitacion = models.IntegerField(
        db_column="idHabilitacion", blank=True, null=True
    )  # Field name made lowercase.
    codigohabilitacion = models.CharField(
        db_column="codigoHabilitacion", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    chasisnro = models.CharField(
        db_column="ChasisNro", max_length=50
    )  # Field name made lowercase.
    motoranio = models.IntegerField(db_column="MotorAnio")  # Field name made lowercase.
    motormarca = models.CharField(
        db_column="MotorMarca", max_length=50
    )  # Field name made lowercase.
    motornumero = models.CharField(
        db_column="MotorNumero", max_length=50
    )  # Field name made lowercase.
    idlocalidadvehiculo = models.IntegerField(
        db_column="idLocalidadVehiculo"
    )  # Field name made lowercase.
    tipodocconductor = models.CharField(
        db_column="TipoDocConductor", max_length=10
    )  # Field name made lowercase.
    nrodocconductor = models.IntegerField(
        db_column="NroDocConductor"
    )  # Field name made lowercase.
    nombreconductor = models.CharField(
        db_column="NombreConductor", max_length=50
    )  # Field name made lowercase.
    apellidoconductor = models.CharField(
        db_column="ApellidoConductor", max_length=50
    )  # Field name made lowercase.
    reverificacion = models.IntegerField(
        db_column="Reverificacion", blank=True, null=True
    )  # Field name made lowercase.
    idverificacionoriginal = models.IntegerField(
        db_column="idVerificacionOriginal", blank=True, null=True
    )  # Field name made lowercase.
    inspector = models.CharField(
        db_column="Inspector", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    directortecnico = models.CharField(
        db_column="DirectorTecnico", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    idestado = models.IntegerField(db_column="idEstado")  # Field name made lowercase.
    eje1_tara = models.DecimalField(
        db_column="Eje1_Tara", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje2_tara = models.DecimalField(
        db_column="Eje2_Tara", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje3_tara = models.DecimalField(
        db_column="Eje3_Tara", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje4_tara = models.DecimalField(
        db_column="Eje4_Tara", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje1_fzaizq = models.DecimalField(
        db_column="Eje1_FzaIzq", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje2_fzaizq = models.DecimalField(
        db_column="Eje2_FzaIzq", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje3_fzaizq = models.DecimalField(
        db_column="Eje3_FzaIzq", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje4_fzaizq = models.DecimalField(
        db_column="Eje4_FzaIzq", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje1_fzader = models.DecimalField(
        db_column="Eje1_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje2_fzader = models.DecimalField(
        db_column="Eje2_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje3_fzader = models.DecimalField(
        db_column="Eje3_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje4_fzader = models.DecimalField(
        db_column="Eje4_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje1_dif = models.DecimalField(
        db_column="Eje1_Dif", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje2_dif = models.DecimalField(
        db_column="Eje2_Dif", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje3_dif = models.DecimalField(
        db_column="Eje3_Dif", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje4_dif = models.DecimalField(
        db_column="Eje4_Dif", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje1_eficiencia = models.DecimalField(
        db_column="Eje1_Eficiencia",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    eje2_eficiencia = models.DecimalField(
        db_column="Eje2_Eficiencia",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    eje3_eficiencia = models.DecimalField(
        db_column="Eje3_Eficiencia",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    eje4_eficiencia = models.DecimalField(
        db_column="Eje4_Eficiencia",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    eje5_tara = models.DecimalField(
        db_column="Eje5_Tara", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje5_fzaizq = models.DecimalField(
        db_column="Eje5_FzaIzq", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje5_fzader = models.DecimalField(
        db_column="Eje5_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje5_dif = models.DecimalField(
        db_column="Eje5_Dif", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje5_eficiencia = models.DecimalField(
        db_column="Eje5_Eficiencia",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    alineacion = models.CharField(
        db_column="Alineacion", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    nivelsonoro = models.CharField(
        db_column="NivelSonoro", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    interior = models.IntegerField(
        db_column="Interior", blank=True, null=True
    )  # Field name made lowercase.
    escape = models.IntegerField(
        db_column="Escape", blank=True, null=True
    )  # Field name made lowercase.
    bach = models.DecimalField(
        db_column="Bach", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    porcentajeco = models.DecimalField(
        db_column="PorcentajeCo", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    opac = models.DecimalField(
        db_column="Opac", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    ppmhc = models.DecimalField(
        db_column="ppmHC", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    freno_fzaisq = models.DecimalField(
        db_column="Freno_FzaIsq", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    freno_fzader = models.DecimalField(
        db_column="Freno_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    freno_dif = models.DecimalField(
        db_column="Freno_Dif", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    freno_eficiencia = models.DecimalField(
        db_column="Freno_Eficiencia",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    cccf = models.CharField(
        db_column="CCCF", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    marcatac = models.CharField(
        db_column="MarcaTac", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    nrotac = models.CharField(
        db_column="NroTac", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    rodadotac_eje1 = models.CharField(
        db_column="RodadoTac_Eje1", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    rodadotac_eje2 = models.CharField(
        db_column="RodadoTac_Eje2", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    rodadotac_eje3 = models.CharField(
        db_column="RodadoTac_Eje3", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    rodadotac_eje4 = models.CharField(
        db_column="RodadoTac_Eje4", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    rodadotac_eje5 = models.CharField(
        db_column="RodadoTac_Eje5", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    nrointerno = models.CharField(
        db_column="NroInterno", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    codigotitular = models.CharField(
        db_column="CodigoTitular", max_length=12
    )  # Field name made lowercase.
    descripciontitular = models.CharField(
        db_column="DescripcionTitular", max_length=150
    )  # Field name made lowercase.
    susp_fzaisq = models.DecimalField(
        db_column="Susp_FzaIsq", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    susp_fzader = models.DecimalField(
        db_column="Susp_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    susp_dif = models.DecimalField(
        db_column="Susp_Dif", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    susp_eficiencia = models.DecimalField(
        db_column="Susp_Eficiencia",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    observaciones = models.TextField(
        db_column="Observaciones"
    )  # Field name made lowercase.
    companiaseguro = models.CharField(
        db_column="CompaniaSeguro", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    nropoliza = models.CharField(
        db_column="NroPoliza", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    ultimorecpatente = models.CharField(
        db_column="UltimoRecPatente", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    idtipouso = models.IntegerField(db_column="idTipoUso")  # Field name made lowercase.
    usuariocarga = models.CharField(
        db_column="usuarioCarga", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    idtipovehiculo = models.IntegerField(
        db_column="idTipoVehiculo", blank=True, null=True
    )  # Field name made lowercase.
    vmarca = models.CharField(
        db_column="VMarca", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    vmodelo = models.CharField(
        db_column="VModelo", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    vanio = models.IntegerField(
        db_column="VAnio", blank=True, null=True
    )  # Field name made lowercase.
    chasismarca = models.CharField(
        db_column="ChasisMarca", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    chasisanio = models.IntegerField(
        db_column="ChasisAnio", blank=True, null=True
    )  # Field name made lowercase.
    tipocombustible = models.CharField(
        db_column="TipoCombustible", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    vpotencia = models.CharField(
        db_column="VPotencia", max_length=20, blank=True, null=True
    )  # Field name made lowercase.
    nroejes = models.IntegerField(
        db_column="NroEjes", blank=True, null=True
    )  # Field name made lowercase.
    vcaja = models.CharField(
        db_column="VCaja", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    pocisionmotor = models.CharField(
        db_column="PocisionMotor", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    aniofabricacion = models.IntegerField(
        db_column="AnioFabricacion"
    )  # Field name made lowercase.
    carroceria = models.CharField(
        db_column="Carroceria", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    expediente = models.CharField(
        db_column="Expediente", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    aireaco = models.IntegerField(
        db_column="AireAco", blank=True, null=True
    )  # Field name made lowercase.
    bar = models.IntegerField(
        db_column="Bar", blank=True, null=True
    )  # Field name made lowercase.
    banio = models.IntegerField(
        db_column="Banio", blank=True, null=True
    )  # Field name made lowercase.
    calefaccion = models.IntegerField(
        db_column="Calefaccion", blank=True, null=True
    )  # Field name made lowercase.
    suspension = models.CharField(
        db_column="Suspension", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    tara = models.DecimalField(
        db_column="Tara", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    pesomax = models.DecimalField(
        db_column="PesoMax", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    cargautil = models.DecimalField(
        db_column="CargaUtil", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    asientos = models.IntegerField(
        db_column="Asientos", blank=True, null=True
    )  # Field name made lowercase.
    idloctmserv = models.IntegerField(
        db_column="idLocTMServ", blank=True, null=True
    )  # Field name made lowercase.
    tiposervtm = models.CharField(
        db_column="TipoServTM", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    idtiposervicio = models.IntegerField(
        db_column="idTipoServicio", blank=True, null=True
    )  # Field name made lowercase.
    idclaseservicio = models.IntegerField(
        db_column="idClaseServicio", blank=True, null=True
    )  # Field name made lowercase.
    prestadorserv = models.CharField(
        db_column="prestadorServ", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    cuitprestserv = models.CharField(
        db_column="CuitPrestServ", max_length=15, blank=True, null=True
    )  # Field name made lowercase.
    ptipodoc = models.CharField(
        db_column="PTipoDoc", max_length=10, blank=True, null=True
    )  # Field name made lowercase.
    pnrodoc = models.IntegerField(
        db_column="PNroDoc", blank=True, null=True
    )  # Field name made lowercase.
    pcuit = models.CharField(
        db_column="PCuit", max_length=15, blank=True, null=True
    )  # Field name made lowercase.
    pdomicilio = models.CharField(
        db_column="PDomicilio", max_length=200, blank=True, null=True
    )  # Field name made lowercase.
    ptelefono = models.CharField(
        db_column="PTelefono", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    pemail = models.CharField(
        db_column="PEmail", max_length=200, blank=True, null=True
    )  # Field name made lowercase.
    pidlocalidad = models.IntegerField(
        db_column="PidLocalidad", blank=True, null=True
    )  # Field name made lowercase.
    ptipopersona = models.CharField(
        db_column="PTipoPersona", max_length=1, blank=True, null=True
    )  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.
    tipocarga = models.CharField(
        db_column="TipoCarga", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    pcodigopj = models.CharField(
        db_column="PCodigoPJ", max_length=30, blank=True, null=True
    )  # Field name made lowercase.
    certificadodiscapacidad = models.CharField(
        db_column="CertificadoDiscapacidad", max_length=250, blank=True, null=True
    )  # Field name made lowercase.
    nrofactura = models.CharField(
        db_column="nroFactura", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    activo = models.IntegerField(db_column="Activo")  # Field name made lowercase.
    status = models.CharField(
        db_column="Status", max_length=50, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "pendientes"
        unique_together = (("idpendiente", "idtaller"),)


class Pendientesdefectos(models.Model):
    idpendiente = models.OneToOneField(
        Pendientes, on_delete=models.CASCADE, db_column="idPendiente", primary_key=True
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        "Talleres", on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    iddefecto = models.IntegerField(db_column="idDefecto")  # Field name made lowercase.
    idnivel = models.IntegerField(db_column="idNivel")  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.
    descripcionrubro = models.CharField(
        db_column="DescripcionRubro", max_length=64
    )  # Field name made lowercase.
    descripciondefecto = models.CharField(
        db_column="DescripcionDefecto", max_length=200
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=160
    )  # Field name made lowercase.
    activo = models.IntegerField(db_column="Activo")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "pendientesdefectos"
        unique_together = (("idpendiente", "idtaller", "iddefecto"),)


class Pendientesservicios(models.Model):
    idpendienteservicios = models.IntegerField(
        db_column="idPendienteServicios", primary_key=True
    )  # Field name made lowercase.
    idpendiente = models.ForeignKey(
        Pendientes, on_delete=models.CASCADE, db_column="idPendiente"
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        "Talleres", on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    idservicio = models.ForeignKey(
        "Serviciostransporte", on_delete=models.CASCADE, db_column="idServicio"
    )  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="fechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.
    activo = models.IntegerField()

    class Meta:
        app_label = "rto_consultas"

        db_table = "pendientesservicios"
        unique_together = (("idpendienteservicios", "idtaller", "idservicio"),)


class Perfiles(models.Model):
    idperfil = models.AutoField(
        db_column="idPerfil", primary_key=True
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=50
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "perfiles"


class Personas(models.Model):
    tipodoc = models.CharField(
        db_column="TipoDoc", max_length=10, blank=True, null=True
    )  # Field name made lowercase.
    nrodoc = models.IntegerField(
        db_column="NroDoc", blank=True, null=True
    )  # Field name made lowercase.
    cuit = models.CharField(
        db_column="Cuit", max_length=15, blank=True, null=True
    )  # Field name made lowercase.
    apellido = models.CharField(
        db_column="Apellido", max_length=70, blank=True, null=True
    )  # Field name made lowercase.
    nombre = models.CharField(
        db_column="Nombre", max_length=70, blank=True, null=True
    )  # Field name made lowercase.
    domicilio = models.CharField(
        db_column="Domicilio", max_length=200, blank=True, null=True
    )  # Field name made lowercase.
    telefono = models.CharField(
        db_column="Telefono", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    razonsocial = models.CharField(
        db_column="RazonSocial", max_length=200, blank=True, null=True
    )  # Field name made lowercase.
    tipopersona = models.CharField(
        db_column="TipoPersona", max_length=1
    )  # Field name made lowercase.
    email = models.CharField(
        db_column="Email", max_length=200, blank=True, null=True
    )  # Field name made lowercase.
    idlocalidad = models.IntegerField(
        db_column="idLocalidad", blank=True, null=True
    )  # Field name made lowercase.
    codigotitular = models.CharField(
        db_column="CodigoTitular", primary_key=True, max_length=12
    )  # Field name made lowercase.
    fechahoraserv = models.DateTimeField(
        db_column="FechaHoraServ", blank=True, null=True
    )  # Field name made lowercase.
    codigopj = models.CharField(
        db_column="CodigoPJ", max_length=30, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "personas"
        unique_together = (("tipodoc", "nrodoc"),)


class Prorroga(models.Model):
    idprorroga = models.IntegerField(
        db_column="idProrroga", primary_key=True
    )  # Field name made lowercase.
    idtaller = models.IntegerField(db_column="idTaller")  # Field name made lowercase.
    numerocertificado = models.CharField(
        db_column="numeroCertificado", max_length=255
    )  # Field name made lowercase.
    replicado = models.IntegerField(blank=True, null=True)
    modificado = models.IntegerField()
    fechahoramodificacion = models.DateTimeField(
        db_column="fechaHoraModificacion", blank=True, null=True
    )  # Field name made lowercase.
    historialmodificacion = models.TextField(
        db_column="historialModificacion", blank=True, null=True
    )  # Field name made lowercase.
    dominio = models.CharField(max_length=10)
    fechahoracreacion = models.DateTimeField(
        db_column="fechaHoraCreacion"
    )  # Field name made lowercase.
    fundamentacionpeticion = models.TextField(
        db_column="fundamentacionPeticion"
    )  # Field name made lowercase.
    fundamentaciondictamen = models.TextField(
        db_column="fundamentacionDictamen", blank=True, null=True
    )  # Field name made lowercase.
    activo = models.IntegerField()
    usuariopeticion = models.CharField(
        db_column="usuarioPeticion", max_length=50
    )  # Field name made lowercase.
    usuariodictamen = models.CharField(
        db_column="usuarioDictamen", max_length=50
    )  # Field name made lowercase.
    aprobado = models.IntegerField(blank=True, null=True)
    fechahoradictamen = models.DateTimeField(
        db_column="fechaHoraDictamen", blank=True, null=True
    )  # Field name made lowercase.
    notifyactive = models.IntegerField(
        db_column="notifyActive"
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "prorroga"


class Provincias(models.Model):
    idprovincia = models.AutoField(
        db_column="idProvincia", primary_key=True
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=100
    )  # Field name made lowercase.
    abreviatura = models.CharField(
        db_column="Abreviatura", max_length=15, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "provincias"


class RepTablasparametricas(models.Model):
    idreplicacion = models.AutoField(
        db_column="idReplicacion", primary_key=True
    )  # Field name made lowercase.
    texto = models.TextField(db_column="Texto")  # Field name made lowercase.
    fechacarga = models.DateTimeField(
        db_column="FechaCarga"
    )  # Field name made lowercase.
    usuario = models.CharField(
        db_column="Usuario", max_length=50
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "rep_tablasparametricas"


class Replicacionlogs(models.Model):
    idreplicacion = models.AutoField(
        db_column="idReplicacion", primary_key=True
    )  # Field name made lowercase.
    idtaller = models.IntegerField(db_column="idTaller")  # Field name made lowercase.
    usuario = models.CharField(
        db_column="Usuario", max_length=50
    )  # Field name made lowercase.
    fechahora = models.DateTimeField(
        db_column="FechaHora"
    )  # Field name made lowercase.
    observaciones = models.TextField(
        db_column="Observaciones"
    )  # Field name made lowercase.
    exito = models.IntegerField(db_column="Exito")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "replicacionlogs"


class Rubrosdefectos(models.Model):
    idrubro = models.AutoField(
        db_column="idRubro", primary_key=True
    )  # Field name made lowercase.
    codigo = models.CharField(
        db_column="Codigo",
        unique=True,
        max_length=10,
        db_collation="utf8mb3_general_ci",
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=200, db_collation="utf8mb3_general_ci"
    )  # Field name made lowercase.
    activo = models.IntegerField(db_column="Activo")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "rubrosdefectos"


class Serviciohab(models.Model):
    idserviciohab = models.AutoField(
        db_column="idServicioHab", primary_key=True
    )  # Field name made lowercase.
    idhabilitacion = models.ForeignKey(
        Habilitacion, on_delete=models.CASCADE, db_column="idHabilitacion"
    )  # Field name made lowercase.
    idserviciostransportehab = models.ForeignKey(
        "Serviciostransportehab",
        on_delete=models.CASCADE,
        db_column="idServiciosTransporteHab",
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "serviciohab"


class Serviciostransporte(models.Model):
    idtiposervicio = models.AutoField(
        db_column="idTipoServicio", primary_key=True
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=200
    )  # Field name made lowercase.
    descripcionnqn = models.CharField(
        db_column="descripcionNqn", max_length=200, blank=True, null=True
    )  # Field name made lowercase.
    habilitado = models.IntegerField(
        db_column="Habilitado"
    )  # Field name made lowercase.
    municipal = models.IntegerField(db_column="Municipal")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "serviciostransporte"


class Serviciostransportehab(models.Model):
    idserviciostransportehab = models.IntegerField(
        db_column="idServiciosTransporteHab", primary_key=True
    )  # Field name made lowercase.
    descripcion = models.CharField(max_length=200)

    class Meta:
        app_label = "rto_consultas"

        db_table = "serviciostransportehab"


class Talleres(models.Model):
    idtaller = models.AutoField(
        db_column="idTaller", primary_key=True,verbose_name="Taller"
    )  # Field name made lowercase.
    idlocalidad = models.ForeignKey(
        Localidades, on_delete=models.CASCADE, db_column="idLocalidad"
    )  # Field name made lowercase.
    nombre = models.CharField(
        db_column="Nombre", max_length=100, db_collation="utf8mb3_general_ci"
    )  # Field name made lowercase.
    nrotaller = models.IntegerField(db_column="Nrotaller")  # Field name made lowercase.
    direccion = models.CharField(
        db_column="Direccion",
        max_length=200,
        db_collation="utf8mb3_general_ci",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    telefono = models.CharField(
        db_column="Telefono",
        max_length=50,
        db_collation="utf8mb3_general_ci",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    activo = models.IntegerField(db_column="Activo")  # Field name made lowercase.
    cuit = models.CharField(
        db_column="Cuit", max_length=11
    )  # Field name made lowercase.
    licenciacomercial = models.CharField(
        db_column="LicenciaComercial", max_length=20
    )  # Field name made lowercase.
    apellidoad = models.CharField(
        db_column="ApellidoAd", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    dniresponsablead = models.CharField(
        db_column="DNIResponsableAd", max_length=8, blank=True, null=True
    )  # Field name made lowercase.
    nombread = models.CharField(
        db_column="NombreAd", max_length=50
    )  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.
    codigorechazado = models.IntegerField(
        db_column="CodigoRechazado"
    )  # Field name made lowercase.
    adjobligatorio = models.IntegerField(
        db_column="AdjObligatorio"
    )  # Field name made lowercase.

    def __str__(self) -> str:
        return f"{self.nombre}"

    class Meta:
        app_label = "rto_consultas"

        db_table = "talleres"

        indexes = [
            models.Index(fields=("idtaller",)),
        ]


class Tipousovehiculo(models.Model):
    idtipouso = models.AutoField(
        db_column="idTipoUso", primary_key=True,verbose_name="Tipo Uso"
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=50
    )  # Field name made lowercase.
    mesesvigencia = models.IntegerField(
        db_column="MesesVigencia", blank=True, null=True
    )  # Field name made lowercase.
    codigooblea = models.IntegerField(
        db_column="CodigoOblea"
    )  # Field name made lowercase.

    def __str__(self) -> str:
        return f"{self.idtipouso}: {tipo_uso_dict[self.idtipouso]}"

    class Meta:
        app_label = "rto_consultas"

        db_table = "tipousovehiculo"
        indexes = [
            models.Index(fields=("idtipouso",)),
        ]


class Tipovehiculo(models.Model):
    idtipovehiculo = models.AutoField(
        db_column="idTipoVehiculo", primary_key=True
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=100
    )  # Field name made lowercase.
    fiscalizable = models.IntegerField(
        db_column="Fiscalizable"
    )  # Field name made lowercase.
    tipovehiculo = models.CharField(
        db_column="tipoVehiculo", max_length=11
    )  # Field name made lowercase.
    activo = models.IntegerField()

    class Meta:
        app_label = "rto_consultas"

        db_table = "tipovehiculo"
        indexes = [
            models.Index(fields=("idtipovehiculo",)),
        ]


class Usuarios(models.Model):
    idusuario = models.AutoField(
        db_column="idUsuario", primary_key=True
    )  # Field name made lowercase.
    usuario = models.CharField(
        db_column="Usuario", unique=True, max_length=50
    )  # Field name made lowercase.
    idperfil = models.ForeignKey(
        Perfiles, on_delete=models.CASCADE, db_column="idPerfil"
    )  # Field name made lowercase.
    password = models.CharField(
        db_column="Password", max_length=150
    )  # Field name made lowercase.
    activo = models.IntegerField(db_column="Activo")  # Field name made lowercase.
    apellido = models.CharField(
        db_column="Apellido", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    nombre = models.CharField(
        db_column="Nombre", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    email = models.CharField(
        db_column="Email", max_length=100, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "usuarios"


class Usuariostaller(models.Model):
    idusuario = models.OneToOneField(
        Usuarios, on_delete=models.CASCADE, db_column="idUsuario", primary_key=True
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        Talleres, on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "usuariostaller"
        unique_together = (("idusuario", "idtaller"),)


class Valoresadm(models.Model):
    idvaladm = models.AutoField(
        db_column="idValAdm", primary_key=True
    )  # Field name made lowercase.
    descripcion = models.CharField(max_length=100)
    valor = models.FloatField()

    class Meta:
        app_label = "rto_consultas"

        db_table = "valoresAdm"


class Vehiculos(models.Model):
    dominio = models.CharField(
        db_column="Dominio", primary_key=True, max_length=10,verbose_name="Dominio"
    )  # Field name made lowercase.
    idtipovehiculo = models.IntegerField(
        db_column="idTipoVehiculo"
    )  # Field name made lowercase.
    marca = models.CharField(
        db_column="Marca", max_length=100
    )  # Field name made lowercase.
    modelo = models.CharField(
        db_column="Modelo", max_length=100
    )  # Field name made lowercase.
    anio = models.IntegerField(db_column="Anio")  # Field name made lowercase.
    idlocalidad = models.IntegerField(
        db_column="idLocalidad"
    )  # Field name made lowercase.
    motormarca = models.CharField(
        db_column="MotorMarca", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    motornro = models.CharField(
        db_column="MotorNro", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    motoranio = models.IntegerField(
        db_column="MotorAnio", blank=True, null=True
    )  # Field name made lowercase.
    chasismarca = models.CharField(
        db_column="ChasisMarca", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    chasisnro = models.CharField(
        db_column="ChasisNro", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    chasisanio = models.IntegerField(
        db_column="ChasisAnio", blank=True, null=True
    )  # Field name made lowercase.
    tacografomarca = models.CharField(
        db_column="TacografoMarca", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    tacografonro = models.CharField(
        db_column="TacografoNro", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    tacograforodado_eje1 = models.CharField(
        db_column="TacografoRodado_Eje1", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    tacograforodado_eje2 = models.CharField(
        db_column="TacografoRodado_Eje2", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    tacograforodado_eje3 = models.CharField(
        db_column="TacografoRodado_Eje3", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    tacograforodado_eje4 = models.CharField(
        db_column="TacografoRodado_Eje4", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    tacograforodado_eje5 = models.CharField(
        db_column="TacografoRodado_Eje5", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    cccf = models.CharField(
        db_column="CCCF", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    tipocombustible = models.CharField(
        db_column="TipoCombustible", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    pot = models.CharField(
        db_column="Pot", max_length=20, blank=True, null=True
    )  # Field name made lowercase.
    nroejes = models.IntegerField(
        db_column="NroEjes", blank=True, null=True
    )  # Field name made lowercase.
    idtipouso = models.ForeignKey(
        Tipousovehiculo, on_delete=models.CASCADE, db_column="idTipoUso"
    )  # Field name made lowercase.
    caja = models.CharField(
        db_column="Caja", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    pocisionmotor = models.CharField(
        db_column="PocisionMotor", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    aniofabricacion = models.IntegerField(
        db_column="AnioFabricacion"
    )  # Field name made lowercase.
    carroceria = models.CharField(
        db_column="Carroceria", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    expediente = models.CharField(
        db_column="Expediente", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    aireaco = models.IntegerField(
        db_column="AireAco", blank=True, null=True
    )  # Field name made lowercase.
    bar = models.IntegerField(
        db_column="Bar", blank=True, null=True
    )  # Field name made lowercase.
    banio = models.IntegerField(
        db_column="Banio", blank=True, null=True
    )  # Field name made lowercase.
    calefaccion = models.IntegerField(
        db_column="Calefaccion", blank=True, null=True
    )  # Field name made lowercase.
    suspencion = models.CharField(
        db_column="Suspencion", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    tara = models.DecimalField(
        db_column="Tara", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    pesomax = models.DecimalField(
        db_column="PesoMax", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    cargautil = models.DecimalField(
        db_column="CargaUtil", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    asientos = models.IntegerField(
        db_column="Asientos", blank=True, null=True
    )  # Field name made lowercase.
    codigotitular = models.CharField(
        db_column="CodigoTitular", max_length=12
    )  # Field name made lowercase.
    idloctmserv = models.ForeignKey(
        Localidades,
        on_delete=models.CASCADE,
        db_column="idLocTMServ",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    tiposervtm = models.CharField(
        db_column="TipoServTM", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    idtiposervicio = models.ForeignKey(
        Serviciostransporte,
        on_delete=models.CASCADE,
        db_column="idTipoServicio",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    tiposservicios = models.CharField(
        db_column="tiposServicios", max_length=400, blank=True, null=True
    )  # Field name made lowercase.
    idhabilitacion = models.IntegerField(
        db_column="idHabilitacion", blank=True, null=True
    )  # Field name made lowercase.
    codigohabilitacion = models.CharField(
        db_column="codigoHabilitacion", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    idclaseservicio = models.IntegerField(
        db_column="idClaseServicio", blank=True, null=True
    )  # Field name made lowercase.
    prestadorserv = models.CharField(
        db_column="prestadorServ", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    cuitprestserv = models.CharField(
        db_column="CuitPrestServ", max_length=15, blank=True, null=True
    )  # Field name made lowercase.
    nrointerno = models.CharField(
        db_column="NroInterno", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    companiaseguro = models.CharField(
        db_column="CompaniaSeguro", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    nropoliza = models.CharField(
        db_column="NroPoliza", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    ultimorecpatente = models.CharField(
        db_column="UltimoRecPatente", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    idcategoria = models.IntegerField(
        db_column="idCategoria"
    )  # Field name made lowercase.
    fechahoraserv = models.DateTimeField(
        db_column="FechaHoraServ", blank=True, null=True
    )  # Field name made lowercase.
    tipocarga = models.CharField(
        db_column="TipoCarga", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    certificadodiscapacidad = models.CharField(
        db_column="CertificadoDiscapacidad", max_length=250, blank=True, null=True
    )  # Field name made lowercase.
    patentemercosur = models.IntegerField(
        db_column="PatenteMercosur"
    )  # Field name made lowercase.
    tipodocconductor = models.CharField(
        db_column="TipoDocConductor", max_length=10, blank=True, null=True
    )  # Field name made lowercase.
    nrodocconductor = models.IntegerField(
        db_column="NroDocConductor", blank=True, null=True
    )  # Field name made lowercase.
    nombreconductor = models.CharField(
        db_column="NombreConductor", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    apellidoconductor = models.CharField(
        db_column="ApellidoConductor", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    domicilioconductor = models.CharField(
        db_column="DomicilioConductor", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    localidadconductor = models.IntegerField(
        db_column="LocalidadConductor", blank=True, null=True
    )  # Field name made lowercase.
    fechaactualizacion = models.DateField(
        db_column="FechaActualizacion", blank=True, null=True
    )  # Field name made lowercase.
    artarjetaverde = models.CharField(
        db_column="arTarjetaVerde", max_length=150, blank=True, null=True
    )  # Field name made lowercase.
    esreverificacion = models.IntegerField(
        db_column="esReverificacion"
    )  # Field name made lowercase.
    idverificacionoriginal = models.IntegerField(
        db_column="idVerificacionOriginal", blank=True, null=True
    )  # Field name made lowercase.
    status = models.CharField(
        db_column="Status", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    idtallerverif = models.IntegerField(
        db_column="idTallerVerif", blank=True, null=True
    )  # Field name made lowercase.
    nrofactura = models.CharField(
        db_column="nroFactura", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    activo = models.IntegerField(db_column="Activo")  # Field name made lowercase.

    def __str__(self) -> str:
        return f"Vehiculo: {self.dominio}"

    class Meta:
        app_label = "rto_consultas"

        db_table = "vehiculos"


class Verificaciones(models.Model):
    idverificacion = models.IntegerField(
        db_column="idVerificacion", primary_key=True
    )  # Field name made lowercase.
    fecha = models.DateField(db_column="Fecha", verbose_name="Fecha")  # Field name made lowercase.
    hora = models.TimeField(db_column="Hora")  # Field name made lowercase.
    horafinal = models.TimeField(
        db_column="HoraFinal", blank=True, null=True
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        Talleres, on_delete=models.CASCADE, db_column="idTaller",
    )  # Field name made lowercase.
    idfotovalidacion = models.IntegerField(
        db_column="idFotovalidacion", blank=True, null=True
    )  # Field name made lowercase.
    dominiovehiculo = models.ForeignKey(
        Vehiculos, on_delete=models.CASCADE, db_column="DominioVehiculo",
    )  # Field name made lowercase.
    idhabilitacion = models.IntegerField(
        db_column="idHabilitacion", blank=True, null=True
    )  # Field name made lowercase.
    codigohabilitacion = models.CharField(
        db_column="codigoHabilitacion", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    chasisnro = models.CharField(
        db_column="ChasisNro", max_length=50
    )  # Field name made lowercase.
    motoranio = models.IntegerField(db_column="MotorAnio")  # Field name made lowercase.
    motormarca = models.CharField(
        db_column="MotorMarca", max_length=50
    )  # Field name made lowercase.
    motornumero = models.CharField(
        db_column="MotorNumero", max_length=50
    )  # Field name made lowercase.
    idlocalidadvehiculo = models.IntegerField(
        db_column="idLocalidadVehiculo"
    )  # Field name made lowercase.
    tipodocconductor = models.CharField(
        db_column="TipoDocConductor", max_length=10
    )  # Field name made lowercase.
    nrodocconductor = models.IntegerField(
        db_column="NroDocConductor"
    )  # Field name made lowercase.
    nombreconductor = models.CharField(
        db_column="NombreConductor", max_length=50
    )  # Field name made lowercase.
    apellidoconductor = models.CharField(
        db_column="ApellidoConductor", max_length=50
    )  # Field name made lowercase.
    reverificacion = models.IntegerField(
        db_column="Reverificacion", blank=True, null=True
    )  # Field name made lowercase.
    idverificacionoriginal = models.IntegerField(
        db_column="idVerificacionOriginal", blank=True, null=True
    )  # Field name made lowercase.
    inspector = models.CharField(
        db_column="Inspector", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    directortecnico = models.CharField(
        db_column="DirectorTecnico", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    idestado = models.ForeignKey(
        Estados, on_delete=models.CASCADE, db_column="idEstado",
    )  # Field name made lowercase.
    eje1_tara = models.DecimalField(
        db_column="Eje1_Tara", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje2_tara = models.DecimalField(
        db_column="Eje2_Tara", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje3_tara = models.DecimalField(
        db_column="Eje3_Tara", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje4_tara = models.DecimalField(
        db_column="Eje4_Tara", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje1_fzaizq = models.DecimalField(
        db_column="Eje1_FzaIzq", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje2_fzaizq = models.DecimalField(
        db_column="Eje2_FzaIzq", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje3_fzaizq = models.DecimalField(
        db_column="Eje3_FzaIzq", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje4_fzaizq = models.DecimalField(
        db_column="Eje4_FzaIzq", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje1_fzader = models.DecimalField(
        db_column="Eje1_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje2_fzader = models.DecimalField(
        db_column="Eje2_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje3_fzader = models.DecimalField(
        db_column="Eje3_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje4_fzader = models.DecimalField(
        db_column="Eje4_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje1_dif = models.DecimalField(
        db_column="Eje1_Dif", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje2_dif = models.DecimalField(
        db_column="Eje2_Dif", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje3_dif = models.DecimalField(
        db_column="Eje3_Dif", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje4_dif = models.DecimalField(
        db_column="Eje4_Dif", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje1_eficiencia = models.DecimalField(
        db_column="Eje1_Eficiencia",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    eje2_eficiencia = models.DecimalField(
        db_column="Eje2_Eficiencia",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    eje3_eficiencia = models.DecimalField(
        db_column="Eje3_Eficiencia",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    eje4_eficiencia = models.DecimalField(
        db_column="Eje4_Eficiencia",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    eje5_tara = models.DecimalField(
        db_column="Eje5_Tara", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje5_fzaizq = models.DecimalField(
        db_column="Eje5_FzaIzq", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje5_fzader = models.DecimalField(
        db_column="Eje5_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje5_dif = models.DecimalField(
        db_column="Eje5_Dif", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    eje5_eficiencia = models.DecimalField(
        db_column="Eje5_Eficiencia",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    alineacion = models.CharField(
        db_column="Alineacion", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    nivelsonoro = models.CharField(
        db_column="NivelSonoro", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    interior = models.IntegerField(
        db_column="Interior", blank=True, null=True
    )  # Field name made lowercase.
    escape = models.IntegerField(
        db_column="Escape", blank=True, null=True
    )  # Field name made lowercase.
    bach = models.DecimalField(
        db_column="Bach", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    porcentajeco = models.DecimalField(
        db_column="PorcentajeCo", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    opac = models.DecimalField(
        db_column="Opac", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    ppmhc = models.DecimalField(
        db_column="ppmHC", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    freno_fzaisq = models.DecimalField(
        db_column="Freno_FzaIsq", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    freno_fzader = models.DecimalField(
        db_column="Freno_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    freno_dif = models.DecimalField(
        db_column="Freno_Dif", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    freno_eficiencia = models.DecimalField(
        db_column="Freno_Eficiencia",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    cccf = models.CharField(
        db_column="CCCF", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    marcatac = models.CharField(
        db_column="MarcaTac", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    nrotac = models.CharField(
        db_column="NroTac", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    rodadotac_eje1 = models.CharField(
        db_column="RodadoTac_Eje1", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    rodadotac_eje2 = models.CharField(
        db_column="RodadoTac_Eje2", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    rodadotac_eje3 = models.CharField(
        db_column="RodadoTac_Eje3", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    rodadotac_eje4 = models.CharField(
        db_column="RodadoTac_Eje4", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    rodadotac_eje5 = models.CharField(
        db_column="RodadoTac_Eje5", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    nrointerno = models.CharField(
        db_column="NroInterno", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    codigotitular = models.ForeignKey(
        Personas, on_delete=models.CASCADE, db_column="CodigoTitular"
    )  # Field name made lowercase.
    descripciontitular = models.CharField(
        db_column="DescripcionTitular", max_length=150
    )  # Field name made lowercase.
    susp_fzaisq = models.DecimalField(
        db_column="Susp_FzaIsq", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    susp_fzader = models.DecimalField(
        db_column="Susp_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    susp_dif = models.DecimalField(
        db_column="Susp_Dif", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    susp_eficiencia = models.DecimalField(
        db_column="Susp_Eficiencia",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    observaciones = models.TextField(
        db_column="Observaciones"
    )  # Field name made lowercase.
    companiaseguro = models.CharField(
        db_column="CompaniaSeguro", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    nropoliza = models.CharField(
        db_column="NroPoliza", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    ultimorecpatente = models.CharField(
        db_column="UltimoRecPatente", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    idtipouso = models.IntegerField(db_column="idTipoUso", )  # Field name made lowercase.
    usuariocarga = models.CharField(
        db_column="usuarioCarga", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    idtipovehiculo = models.IntegerField(
        db_column="idTipoVehiculo", blank=True, null=True
    )  # Field name made lowercase.
    vmarca = models.CharField(
        db_column="VMarca", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    vmodelo = models.CharField(
        db_column="VModelo", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    vanio = models.IntegerField(
        db_column="VAnio", blank=True, null=True
    )  # Field name made lowercase.
    chasismarca = models.CharField(
        db_column="ChasisMarca", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    chasisanio = models.IntegerField(
        db_column="ChasisAnio", blank=True, null=True
    )  # Field name made lowercase.
    tipocombustible = models.CharField(
        db_column="TipoCombustible", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    vpotencia = models.CharField(
        db_column="VPotencia", max_length=20, blank=True, null=True
    )  # Field name made lowercase.
    nroejes = models.IntegerField(
        db_column="NroEjes", blank=True, null=True
    )  # Field name made lowercase.
    vcaja = models.CharField(
        db_column="VCaja", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    pocisionmotor = models.CharField(
        db_column="PocisionMotor", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    aniofabricacion = models.IntegerField(
        db_column="AnioFabricacion"
    )  # Field name made lowercase.
    carroceria = models.CharField(
        db_column="Carroceria", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    expediente = models.CharField(
        db_column="Expediente", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    aireaco = models.IntegerField(
        db_column="AireAco", blank=True, null=True
    )  # Field name made lowercase.
    bar = models.IntegerField(
        db_column="Bar", blank=True, null=True
    )  # Field name made lowercase.
    banio = models.IntegerField(
        db_column="Banio", blank=True, null=True
    )  # Field name made lowercase.
    calefaccion = models.IntegerField(
        db_column="Calefaccion", blank=True, null=True
    )  # Field name made lowercase.
    suspencion = models.CharField(
        db_column="Suspencion", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    tara = models.DecimalField(
        db_column="Tara", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    pesomax = models.DecimalField(
        db_column="PesoMax", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    cargautil = models.DecimalField(
        db_column="CargaUtil", max_digits=10, decimal_places=2, blank=True, null=True
    )  # Field name made lowercase.
    asientos = models.IntegerField(
        db_column="Asientos", blank=True, null=True
    )  # Field name made lowercase.
    idloctmserv = models.IntegerField(
        db_column="idLocTMServ", blank=True, null=True
    )  # Field name made lowercase.
    tiposervtm = models.CharField(
        db_column="TipoServTM", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    idtiposervicio = models.IntegerField(
        db_column="idTipoServicio", blank=True, null=True
    )  # Field name made lowercase.
    idclaseservicio = models.IntegerField(
        db_column="idClaseServicio", blank=True, null=True
    )  # Field name made lowercase.
    prestadorserv = models.CharField(
        db_column="prestadorServ", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    cuitprestserv = models.CharField(
        db_column="CuitPrestServ", max_length=15, blank=True, null=True
    )  # Field name made lowercase.
    ptipodoc = models.CharField(
        db_column="PTipoDoc", max_length=10, blank=True, null=True
    )  # Field name made lowercase.
    pnrodoc = models.IntegerField(
        db_column="PNroDoc", blank=True, null=True
    )  # Field name made lowercase.
    pcuit = models.CharField(
        db_column="PCuit", max_length=15, blank=True, null=True
    )  # Field name made lowercase.
    pdomicilio = models.CharField(
        db_column="PDomicilio", max_length=200, blank=True, null=True
    )  # Field name made lowercase.
    ptelefono = models.CharField(
        db_column="PTelefono", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    pemail = models.CharField(
        db_column="PEmail", max_length=200, blank=True, null=True
    )  # Field name made lowercase.
    pidlocalidad = models.IntegerField(
        db_column="PidLocalidad", blank=True, null=True
    )  # Field name made lowercase.
    ptipopersona = models.CharField(
        db_column="PTipoPersona", max_length=1, blank=True, null=True
    )  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.
    tipocarga = models.CharField(
        db_column="TipoCarga", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    pcodigopj = models.CharField(
        db_column="PCodigoPJ", max_length=30, blank=True, null=True
    )  # Field name made lowercase.
    certificadodiscapacidad = models.CharField(
        db_column="CertificadoDiscapacidad", max_length=250, blank=True, null=True
    )  # Field name made lowercase.
    firma = models.CharField(
        db_column="Firma", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    nrofactura = models.CharField(
        db_column="nroFactura", max_length=100, blank=True, null=True
    )  # Field name made lowercase.

    def __str__(self) -> str:
        return f"Verif: {self.idverificacion}:{self.dominiovehiculo} - {self.idtaller}"

    @staticmethod
    def get_nro_certificado(record):
        cert = (Certificados
                        .objects
                        .prefetch_related("idverificacion")
                        .get(idverificacion__exact=record.idverificacion,
                                idtaller__exact=record.idtaller)
                    )

        return cert.nrocertificado
        # return (record.certificados
        #                # .all()
        #                .get(
        #                    idverificacion=record.idverificacion,
        #                    idtaller=record.idtaller
        #                     )
        #                )

    class Meta:
        app_label = "rto_consultas"

        db_table = "verificaciones"
        unique_together = (("idverificacion", "idtaller"),)
        indexes = [
            models.Index(fields=("idverificacion", "idtaller")),
            models.Index(fields=("idtipouso",)),
            models.Index(fields=("idhabilitacion",)),
        ]


class Verificacionespdf(models.Model):
    idpdf = models.IntegerField(
        db_column="idPDF", primary_key=True
    )  # Field name made lowercase.
    nombrea4 = models.CharField(
        db_column="NombreA4", max_length=200
    )  # Field name made lowercase.
    nombretc = models.CharField(
        db_column="NombreTC", max_length=200
    )  # Field name made lowercase.
    hasha4 = models.CharField(
        db_column="HashA4", max_length=200
    )  # Field name made lowercase.
    idverificacion = models.ForeignKey(
        Verificaciones, on_delete=models.CASCADE, db_column="idVerificacion"
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        Talleres, on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    fechacarga = models.DateField(db_column="FechaCarga")  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.
    enviado = models.IntegerField(db_column="Enviado")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "verificacionesPDF"
        unique_together = (("idpdf", "idtaller"),)


class Verificacionesauditorias(models.Model):
    idauditoria = models.AutoField(
        db_column="idAuditoria", primary_key=True
    )  # Field name made lowercase.
    fechacarga = models.DateTimeField(
        db_column="FechaCarga"
    )  # Field name made lowercase.
    idverificacion = models.IntegerField(
        db_column="idVerificacion"
    )  # Field name made lowercase.
    idtaller = models.IntegerField(db_column="idTaller")  # Field name made lowercase.
    observaciones = models.TextField(
        db_column="Observaciones"
    )  # Field name made lowercase.
    conforme = models.IntegerField(db_column="Conforme")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "verificacionesauditorias"


class Verificacionesdefectos(models.Model):
    idverificacion = models.OneToOneField(
        Verificaciones,
        on_delete=models.CASCADE,
        db_column="idVerificacion",
        primary_key=True,
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        Talleres, on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    iddefecto = models.IntegerField(db_column="idDefecto")  # Field name made lowercase.
    idnivel = models.ForeignKey(
        Nivelesdefectos, on_delete=models.CASCADE, db_column="idNivel"
    )  # Field name made lowercase.
    replicado = models.IntegerField(db_column="Replicado")  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="FechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.
    descripcionrubro = models.CharField(
        db_column="DescripcionRubro", max_length=200
    )  # Field name made lowercase.
    descripciondefecto = models.CharField(
        db_column="DescripcionDefecto", max_length=200
    )  # Field name made lowercase.
    descripcion = models.CharField(
        db_column="Descripcion", max_length=160
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "verificacionesdefectos"
        unique_together = (("idverificacion", "idtaller", "iddefecto"),)


class Verificacionesservicios(models.Model):
    idverificacionesservicios = models.AutoField(
        db_column="idVerificacionesServicios", primary_key=True
    )  # Field name made lowercase.
    idverificacion = models.ForeignKey(
        Verificaciones, on_delete=models.CASCADE, db_column="idVerificacion"
    )  # Field name made lowercase.
    idtaller = models.ForeignKey(
        Talleres, on_delete=models.CASCADE, db_column="idTaller"
    )  # Field name made lowercase.
    idservicio = models.IntegerField(
        db_column="idServicio"
    )  # Field name made lowercase.
    fechahorarep = models.DateTimeField(
        db_column="fechaHoraRep", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "verificacionesservicios"
        unique_together = (("idverificacionesservicios", "idtaller", "idservicio"),)


class Vin(models.Model):
    idvin = models.AutoField(
        db_column="idVin", primary_key=True
    )  # Field name made lowercase.
    letra = models.TextField()
    aniovin = models.IntegerField(db_column="anioVin")  # Field name made lowercase.

    class Meta:
        app_label = "rto_consultas"

        db_table = "vin"


# class VWVerificaciones(models.Model):
#     idverificacion = models.IntegerField(db_column="idVerificacion", primary_key=True)
#     fecha = models.DateField(db_column="Fecha")
#     hora = models.TimeField(db_column="Hora")
#     horafinal = models.TimeField(db_column="HoraFinal", blank=True, null=True)
#     idtaller = models.ForeignKey(
#         Talleres, on_delete=models.CASCADE, db_column="idTaller"
#     )
#     idfotovalidacion = models.IntegerField(
#         db_column="idFotovalidacion", blank=True, null=True
#     )
#     dominiovehiculo = models.ForeignKey(
#         Vehiculos, on_delete=models.CASCADE, db_column="DominioVehiculo"
#     )
#     idhabilitacion = models.IntegerField(
#         db_column="idHabilitacion", blank=True, null=True
#     )
#     codigohabilitacion = models.CharField(
#         db_column="codigoHabilitacion", max_length=255, blank=True, null=True
#     )
#     chasisnro = models.CharField(db_column="ChasisNro", max_length=50)
#     motoranio = models.IntegerField(db_column="MotorAnio")
#     motormarca = models.CharField(db_column="MotorMarca", max_length=50)
#     motornumero = models.CharField(db_column="MotorNumero", max_length=50)
#     idlocalidadvehiculo = models.IntegerField(db_column="idLocalidadVehiculo")
#     tipodocconductor = models.CharField(db_column="TipoDocConductor", max_length=10)
#     nrodocconductor = models.IntegerField(db_column="NroDocConductor")
#     nombreconductor = models.CharField(db_column="NombreConductor", max_length=50)
#     apellidoconductor = models.CharField(db_column="ApellidoConductor", max_length=50)
#     reverificacion = models.IntegerField(
#         db_column="Reverificacion", blank=True, null=True
#     )
#     idverificacionoriginal = models.IntegerField(
#         db_column="idVerificacionOriginal", blank=True, null=True
#     )
#     inspector = models.CharField(
#         db_column="Inspector", max_length=100, blank=True, null=True
#     )
#     directortecnico = models.CharField(
#         db_column="DirectorTecnico", max_length=100, blank=True, null=True
#     )
#     idestado = models.ForeignKey(
#         Estados, on_delete=models.CASCADE, db_column="idEstado"
#     )
#     eje1_tara = models.DecimalField(
#         db_column="Eje1_Tara", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje2_tara = models.DecimalField(
#         db_column="Eje2_Tara", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje3_tara = models.DecimalField(
#         db_column="Eje3_Tara", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje4_tara = models.DecimalField(
#         db_column="Eje4_Tara", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje1_fzaizq = models.DecimalField(
#         db_column="Eje1_FzaIzq", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje2_fzaizq = models.DecimalField(
#         db_column="Eje2_FzaIzq", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje3_fzaizq = models.DecimalField(
#         db_column="Eje3_FzaIzq", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje4_fzaizq = models.DecimalField(
#         db_column="Eje4_FzaIzq", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje1_fzader = models.DecimalField(
#         db_column="Eje1_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje2_fzader = models.DecimalField(
#         db_column="Eje2_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje3_fzader = models.DecimalField(
#         db_column="Eje3_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje4_fzader = models.DecimalField(
#         db_column="Eje4_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje1_dif = models.DecimalField(
#         db_column="Eje1_Dif", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje2_dif = models.DecimalField(
#         db_column="Eje2_Dif", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje3_dif = models.DecimalField(
#         db_column="Eje3_Dif", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje4_dif = models.DecimalField(
#         db_column="Eje4_Dif", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje1_eficiencia = models.DecimalField(
#         db_column="Eje1_Eficiencia",
#         max_digits=10,
#         decimal_places=2,
#         blank=True,
#         null=True,
#     )
#     eje2_eficiencia = models.DecimalField(
#         db_column="Eje2_Eficiencia",
#         max_digits=10,
#         decimal_places=2,
#         blank=True,
#         null=True,
#     )
#     eje3_eficiencia = models.DecimalField(
#         db_column="Eje3_Eficiencia",
#         max_digits=10,
#         decimal_places=2,
#         blank=True,
#         null=True,
#     )
#     eje4_eficiencia = models.DecimalField(
#         db_column="Eje4_Eficiencia",
#         max_digits=10,
#         decimal_places=2,
#         blank=True,
#         null=True,
#     )
#     eje5_tara = models.DecimalField(
#         db_column="Eje5_Tara", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje5_fzaizq = models.DecimalField(
#         db_column="Eje5_FzaIzq", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje5_fzader = models.DecimalField(
#         db_column="Eje5_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje5_dif = models.DecimalField(
#         db_column="Eje5_Dif", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     eje5_eficiencia = models.DecimalField(
#         db_column="Eje5_Eficiencia",
#         max_digits=10,
#         decimal_places=2,
#         blank=True,
#         null=True,
#     )
#     alineacion = models.CharField(
#         db_column="Alineacion", max_length=50, blank=True, null=True
#     )
#     nivelsonoro = models.CharField(
#         db_column="NivelSonoro", max_length=50, blank=True, null=True
#     )
#     interior = models.IntegerField(db_column="Interior", blank=True, null=True)
#     escape = models.IntegerField(db_column="Escape", blank=True, null=True)
#     bach = models.DecimalField(
#         db_column="Bach", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     porcentajeco = models.DecimalField(
#         db_column="PorcentajeCo", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     opac = models.DecimalField(
#         db_column="Opac", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     ppmhc = models.DecimalField(
#         db_column="ppmHC", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     freno_fzaisq = models.DecimalField(
#         db_column="Freno_FzaIsq", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     freno_fzader = models.DecimalField(
#         db_column="Freno_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     freno_dif = models.DecimalField(
#         db_column="Freno_Dif", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     freno_eficiencia = models.DecimalField(
#         db_column="Freno_Eficiencia",
#         max_digits=10,
#         decimal_places=2,
#         blank=True,
#         null=True,
#     )
#     cccf = models.CharField(db_column="CCCF", max_length=50, blank=True, null=True)
#     marcatac = models.CharField(
#         db_column="MarcaTac", max_length=50, blank=True, null=True
#     )
#     nrotac = models.CharField(db_column="NroTac", max_length=50, blank=True, null=True)
#     rodadotac_eje1 = models.CharField(
#         db_column="RodadoTac_Eje1", max_length=50, blank=True, null=True
#     )
#     rodadotac_eje2 = models.CharField(
#         db_column="RodadoTac_Eje2", max_length=50, blank=True, null=True
#     )
#     rodadotac_eje3 = models.CharField(
#         db_column="RodadoTac_Eje3", max_length=50, blank=True, null=True
#     )
#     rodadotac_eje4 = models.CharField(
#         db_column="RodadoTac_Eje4", max_length=50, blank=True, null=True
#     )
#     rodadotac_eje5 = models.CharField(
#         db_column="RodadoTac_Eje5", max_length=50, blank=True, null=True
#     )
#     nrointerno = models.CharField(
#         db_column="NroInterno", max_length=50, blank=True, null=True
#     )
#     codigotitular = models.ForeignKey(
#         Personas, on_delete=models.CASCADE, db_column="CodigoTitular"
#     )
#     descripciontitular = models.CharField(
#         db_column="DescripcionTitular", max_length=150
#     )
#     susp_fzaisq = models.DecimalField(
#         db_column="Susp_FzaIsq", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     susp_fzader = models.DecimalField(
#         db_column="Susp_FzaDer", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     susp_dif = models.DecimalField(
#         db_column="Susp_Dif", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     susp_eficiencia = models.DecimalField(
#         db_column="Susp_Eficiencia",
#         max_digits=10,
#         decimal_places=2,
#         blank=True,
#         null=True,
#     )
#     observaciones = models.TextField(db_column="Observaciones")
#     companiaseguro = models.CharField(
#         db_column="CompaniaSeguro", max_length=50, blank=True, null=True
#     )
#     nropoliza = models.CharField(
#         db_column="NroPoliza", max_length=50, blank=True, null=True
#     )
#     ultimorecpatente = models.CharField(
#         db_column="UltimoRecPatente", max_length=50, blank=True, null=True
#     )
#     idtipouso = models.IntegerField(db_column="idTipoUso")
#     usuariocarga = models.CharField(
#         db_column="usuarioCarga", max_length=50, blank=True, null=True
#     )
#     idtipovehiculo = models.IntegerField(
#         db_column="idTipoVehiculo", blank=True, null=True
#     )
#     vmarca = models.CharField(db_column="VMarca", max_length=100, blank=True, null=True)
#     vmodelo = models.CharField(
#         db_column="VModelo", max_length=100, blank=True, null=True
#     )
#     vanio = models.IntegerField(db_column="VAnio", blank=True, null=True)
#     chasismarca = models.CharField(
#         db_column="ChasisMarca", max_length=100, blank=True, null=True
#     )
#     chasisanio = models.IntegerField(db_column="ChasisAnio", blank=True, null=True)
#     tipocombustible = models.CharField(
#         db_column="TipoCombustible", max_length=50, blank=True, null=True
#     )
#     vpotencia = models.CharField(
#         db_column="VPotencia", max_length=20, blank=True, null=True
#     )
#     nroejes = models.IntegerField(db_column="NroEjes", blank=True, null=True)
#     vcaja = models.CharField(db_column="VCaja", max_length=50, blank=True, null=True)
#     pocisionmotor = models.CharField(
#         db_column="PocisionMotor", max_length=50, blank=True, null=True
#     )
#     aniofabricacion = models.IntegerField(db_column="AnioFabricacion")
#     carroceria = models.CharField(
#         db_column="Carroceria", max_length=50, blank=True, null=True
#     )
#     expediente = models.CharField(
#         db_column="Expediente", max_length=50, blank=True, null=True
#     )
#     aireaco = models.IntegerField(db_column="AireAco", blank=True, null=True)
#     bar = models.IntegerField(db_column="Bar", blank=True, null=True)
#     banio = models.IntegerField(db_column="Banio", blank=True, null=True)
#     calefaccion = models.IntegerField(db_column="Calefaccion", blank=True, null=True)
#     suspencion = models.CharField(
#         db_column="Suspencion", max_length=50, blank=True, null=True
#     )
#     tara = models.DecimalField(
#         db_column="Tara", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     pesomax = models.DecimalField(
#         db_column="PesoMax", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     cargautil = models.DecimalField(
#         db_column="CargaUtil", max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     asientos = models.IntegerField(db_column="Asientos", blank=True, null=True)
#     idloctmserv = models.IntegerField(db_column="idLocTMServ", blank=True, null=True)
#     tiposervtm = models.CharField(
#         db_column="TipoServTM", max_length=100, blank=True, null=True
#     )
#     idtiposervicio = models.IntegerField(
#         db_column="idTipoServicio", blank=True, null=True
#     )
#     idclaseservicio = models.IntegerField(
#         db_column="idClaseServicio", blank=True, null=True
#     )
#     prestadorserv = models.CharField(
#         db_column="prestadorServ", max_length=100, blank=True, null=True
#     )
#     cuitprestserv = models.CharField(
#         db_column="CuitPrestServ", max_length=15, blank=True, null=True
#     )
#     ptipodoc = models.CharField(
#         db_column="PTipoDoc", max_length=10, blank=True, null=True
#     )
#     pnrodoc = models.IntegerField(db_column="PNroDoc", blank=True, null=True)
#     pcuit = models.CharField(db_column="PCuit", max_length=15, blank=True, null=True)
#     pdomicilio = models.CharField(
#         db_column="PDomicilio", max_length=200, blank=True, null=True
#     )
#     ptelefono = models.CharField(
#         db_column="PTelefono", max_length=50, blank=True, null=True
#     )
#     pemail = models.CharField(db_column="PEmail", max_length=200, blank=True, null=True)
#     pidlocalidad = models.IntegerField(db_column="PidLocalidad", blank=True, null=True)
#     ptipopersona = models.CharField(
#         db_column="PTipoPersona", max_length=1, blank=True, null=True
#     )
#     # fechahorarep = models.DateTimeField(db_column="FechaHoraRep", blank=True, null=True)
#     tipocarga = models.CharField(
#         db_column="TipoCarga", max_length=50, blank=True, null=True
#     )
#     pcodigopj = models.CharField(
#         db_column="PCodigoPJ", max_length=30, blank=True, null=True
#     )
#     certificadodiscapacidad = models.CharField(
#         db_column="CertificadoDiscapacidad", max_length=250, blank=True, null=True
#     )
#     firma = models.CharField(db_column="Firma", max_length=100, blank=True, null=True)
#     nrofactura = models.CharField(
#         db_column="nroFactura", max_length=100, blank=True, null=True
#     )

#     idcertificado = models.IntegerField(
#         db_column="idCertificado",
#     )
#     nrocertificado = models.BigIntegerField(db_column="NroCertificado", unique=True)
#     vigenciahasta = models.DateField(db_column="VigenciaHasta")
#     serie = models.CharField(db_column="Serie", max_length=1)
#     certanulado = models.IntegerField(db_column="certAnulado")
#     observaciones = models.TextField(
#         db_column="ObservacionesCert", blank=True, null=True
#     )
#     idcategoria = models.IntegerField(db_column="idCategoria", blank=True, null=True)
#     porcentajecategoria = models.DecimalField(
#         db_column="porcentajeCategoria",
#         max_digits=10,
#         decimal_places=2,
#         blank=True,
#         null=True,
#     )
#     vencido = models.IntegerField(db_column="certVencido")
#     reverificado = models.IntegerField(db_column="certReverificado")
#     categoria = models.CharField(db_column="Categoria", max_length=100)
#     nombre = models.CharField(
#         db_column="Taller", max_length=100, db_collation="utf8mb3_general_ci"
#     )
#     nrotaller = models.IntegerField(db_column="Nrotaller")
#     estado = models.CharField(db_column="Estado", max_length=100)
#     tipoUso = models.CharField(db_column="tipoUso", max_length=50)
#     tipoVehiculo = models.CharField(db_column="tipoVehiculo", max_length=100)
#     vidprovincia = models.IntegerField(db_column="VidProvincia")
#     localidadvehiculo = models.CharField(db_column="LocalidadVehiculo", max_length=100)
#     pidprovincia = models.IntegerField(db_column="PidProvincia")
#     localidadtitular = models.CharField(db_column="LocalidadTitular", max_length=100)
#     locta = models.IntegerField(db_column="LocTa")
#     tidprovincia = models.CharField(db_column="TidProvincia", max_length=100)
#     localidadtaller = models.CharField(db_column="LocalidadTaller", max_length=100)
#     tmidprovincia = models.CharField(db_column="TMidProvincia", max_length=100)
#     localidadtranspmuni = models.CharField(
#         db_column="LocalidadTranspMuni", max_length=100
#     )
#     tiposervpas = models.CharField(db_column="tipoServPas", max_length=200)
#     claseservpas = models.CharField(db_column="claseServPas", max_length=200)

#     class Meta:
#         app_label = "rto_consultas"
#         db_table = "vw_verificaciones"
#         managed = False

#         unique_together = (("idverificacion", "idtaller"),)
#         indexes = [
#             models.Index(fields=("idverificacion", "idtaller")),
#             models.Index(fields=("idtipouso",)),
#             models.Index(fields=("idhabilitacion",)),
#         ]
