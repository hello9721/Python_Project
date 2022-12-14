class UserRouter(object):
    
    # db키 값(settings.py에서 설정한 키 값이라고 보면된다.)
    db_name = 'Weather'

    def __init__(self):
        self.model_list = ['default', self.db_name]

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.model_list:
            return model._meta.app_label

        return None

    def db_for_write(self, model, **hints):
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return None