class HistoryDBRouter:
    """
    A router to control all database operations on models in the
    history application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read history models go to history_db.
        """
        if model._meta.app_label == 'history':
            return 'history_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write history models go to history_db.
        """
        if model._meta.app_label == 'history':
            return 'history_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the history app is involved.
        """
        if obj1._meta.app_label == 'history' or \
           obj2._meta.app_label == 'history':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the history app only appears in the 'history_db'
        database.
        """
        if app_label == 'history':
            return db == 'history_db'
        return None