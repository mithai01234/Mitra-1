class CustomUserRouter:
    """
    A router to control all database operations on the `CustomUser` model.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'registration' and model._meta.model_name == 'User':
            return 'custom_user_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'registration' and model._meta.model_name == 'User':
            return 'custom_user_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label == obj2._meta.app_label == 'registration' and
            obj1._meta.model_name == obj2._meta.model_name == 'User'
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'registration':
            if model_name == 'User':
                return db == 'custom_user_db'
        return None
