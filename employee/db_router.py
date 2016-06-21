from utils import constants


class DbRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "eboa":
            return constants.DATABASE_BPM_EBOA
        else:
            return constants.DATABASE_EB

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'eboa':
            return 'auth_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'eboa' and \
           obj2._meta.app_label == 'eboa':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label == 'eboa':
            return db == constants.DATABASE_BPM_EBOA
        return None