class CommentRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.db_table == 'todo_comment':
            return 'comment'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.db_table == 'todo_comment':
            return 'comment'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # if obj1._meta.app_label == 'comment' or \
        #         (obj2._meta.app_label == 'todo' or
        #          obj2._meta.app_label == 'sharetodo'):
        #     return True
        # return None
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name == 'comment':
            return db == 'comment'
        return None
