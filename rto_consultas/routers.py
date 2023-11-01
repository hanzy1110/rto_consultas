DJANGO_TABLES = ["auth", "admin", "contenttypes", "sessions"]

class UserRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label in DJANGO_TABLES:
            return 'users'
        elif model._meta.app_label == "rto_consultas_rn":
            return "rio_negro"
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in DJANGO_TABLES:
            return 'users'
        elif model._meta.app_label == "rto_consultas_rn":
            return "rio_negro"
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in DJANGO_TABLES:
            return db == 'users'
        elif app_label == "rto_consultas_rn":
            return db == "rio_negro"

        return db == 'default'
