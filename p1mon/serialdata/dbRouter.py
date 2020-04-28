class SerialdataDBRouter:
    """
    A router to control all database operations on models in the
    serialdata application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read serialdata models go to serialdata_db.
        """
        if model._meta.app_label == 'serialdata':
            return 'serialdata_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write serialdata models go to serialdata_db.
        """
        if model._meta.app_label == 'serialdata':
            return 'serialdata_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the serialdata app is involved.
        """
        if obj1._meta.app_label == 'serialdata' or \
           obj2._meta.app_label == 'serialdata':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the serialdata app only appears in the 'serialdata_db'
        database.
        """
        if app_label == 'serialdata':
            return db == 'serialdata_db'
        return None