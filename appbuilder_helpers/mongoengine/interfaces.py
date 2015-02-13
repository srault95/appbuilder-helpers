# -*- coding: utf-8 -*-

from flask_login import current_user

from flask_appbuilder.models.mongoengine.interface import MongoEngineInterface

DEFAULT_GROUP_FIELD = 'group'
DEFAULT_GROUP_FIELD_IN_USER = 'group'

"""
TODO: if group is None ?
TODO: if role_admin ?
"""

class MongoEngineInterfaceByGroup(MongoEngineInterface):
    '''Add filter by Group model for all objects if have group field'''
    
    def __init__(self, obj, session=None, enable_filter_group=True, group_field=DEFAULT_GROUP_FIELD):
        
        MongoEngineInterface.__init__(self, obj, session=session)
        
        self.enable_filter_group = enable_filter_group
        
        self.group_field = group_field
        
        if not self.group_field in self.obj._fields.keys():
            self.enable_filter_group = False
    
    def query(self, filters=None, order_column='', order_direction='',
              page=None, page_size=None):

        if filters:
            objs = filters.apply_all(self.get_objects())
        else:
            objs = self.get_objects()
            
        count = len(objs)
        
        start, stop = 0, count
        if page:
            start = page * page_size
        if page_size:
            stop = start + page_size
        if order_column != '':
            if order_direction == 'asc':
                objs = objs.order_by('-{0}'.format(order_column))
            else:
                objs = objs.order_by('+{0}'.format(order_column))
        return count, objs[start:stop]

    def get(self, id):
        qs = self.get_objects()
        if qs:
            return qs.filter(pk=id).first()

    def filter_group(self, qs, group=None):
        
        '''Not group field in model'''        
        if not self.group_field in self.obj._fields.keys():
            return qs
        
        if group:
            f = {self.group_field:group}
            return qs.filter(**f)
        
        try:
            current_group = getattr(current_user, DEFAULT_GROUP_FIELD_IN_USER, None)
            
            if not current_group:
                return qs
            
            f = {self.group_field:current_group}
            return qs.filter(**f)
        except:
            pass
        
        return qs
    
    def get_objects(self):
        u'''Add method for filter objects
        
        ex: self.objects(group=current_user.group)
        '''
        """
        self.enable_filter_group: :  <class 'app.models.Tags'> False
        self.enable_filter_group: :  <class 'app.models.Gender'> False
        self.enable_filter_group: :  <class 'flask_appbuilder.security.mongoengine.models.Group'> False        
        """
        
        if self.enable_filter_group:
            return self.filter_group(self.obj.objects)
        
        return self.obj.objects

    def is_integer(self, col_name):
        try:
            return isinstance(self.obj._fields[col_name], (fields.IntField, fields.LongField))
        except:
            return False
    
