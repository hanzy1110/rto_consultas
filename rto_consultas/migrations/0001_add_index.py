from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('rto_consultas', '0001_add_idx_verificaciones.py'),
    ]

    operations = [
        migrations.RunSQL(
            sql='ALTER TABLE verificaciones ADD INDEX taller_idx (idTaller);',
            reverse_sql='ALTER TABLE my_table DROP INDEX taller_idx;'
        ),
        migrations.RunSQL(
            sql='ALTER TABLE verificaciones ADD INDEX tipo_uso_idx (idTipoUso);',
            reverse_sql='ALTER TABLE my_table DROP INDEX tipo_uso_idx;'
        ),
        migrations.RunSQL(
            sql='ALTER TABLE verificaciones ADD INDEX id_hab_idx (idHabilitacion);',
            reverse_sql='ALTER TABLE my_table DROP INDEX id_hab_idx;'
        ),
        migrations.RunSQL(
            sql='ALTER TABLE verificaciones ADD INDEX id_verif_idx (idVerificacion);',
            reverse_sql='ALTER TABLE my_table DROP INDEX id_verif_idx ;'
        ),
    ]

