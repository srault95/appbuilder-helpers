# -*- coding: utf-8 -*-

import logging

from werkzeug.security import generate_password_hash

from mongoengine import fields

from flask_babelpkg import lazy_gettext

from flask_appbuilder.security.views import UserDBModelView as BaseUserDBModelView
from flask_appbuilder.security.views import ModelView
from flask_appbuilder.security.mongoengine.manager import SecurityManager as BaseSecurityManager
from flask_appbuilder.models.mongoengine.interface import MongoEngineInterface

from interfaces import MongoEngineInterfaceByGroup
import models 

log = logging.getLogger(__name__)

class UserDBModelView(BaseUserDBModelView):
    
    #list_columns = BaseUserDBModelView.list_columns + ['group']
    list_columns = ['group', 'first_name', 'last_name', 'username', 'email', 'active', 'roles']
    
    #add_columns = BaseUserDBModelView.add_columns + ['group']
    add_columns = ['group', 'first_name', 'last_name', 'username', 'active', 'email', 'roles', 'password']#, 'conf_password']

    edit_columns = ['group', 'first_name', 'last_name', 'username', 'active', 'email', 'roles', 'password']#, 'conf_password']

    
    #BaseUserDBModelView.label_columns.update({'group': lazy_gettext('Group')})
    
    #BaseUserDBModelView.description_columns.update({'group': lazy_gettext('Group')})
    show_fieldsets = [
        (lazy_gettext('User info'),
         {'fields': ['username', 'group', 'active', 'roles', 'login_count']}),
        (lazy_gettext('Personal Info'),
         {'fields': ['first_name', 'last_name', 'email'], 'expanded': True}),
        (lazy_gettext('Audit Info'),
         {'fields': ['last_login', 'fail_login_count', 'created_on',
                     'created_by', 'changed_on', 'changed_by'], 'expanded': False}),
    ]

    user_show_fieldsets = [
        (lazy_gettext('User info'),
         {'fields': ['username', 'group', 'active', 'roles', 'login_count']}),
        (lazy_gettext('Personal Info'),
         {'fields': ['first_name', 'last_name', 'email'], 'expanded': True}),
    ]
    """
    
    search_columns = BaseUserDBModelView.search_columns + ['group']
    """
    
class GroupModelView(ModelView):
    route_base = '/groups'
    
    related_views = [UserDBModelView]
    
    list_columns = ['name', 'active']

    list_title = lazy_gettext('List Groups')
    show_title = lazy_gettext('Show Groups')
    add_title = lazy_gettext('Add Groups')
    edit_title = lazy_gettext('Edit Groups')
    
    
class SecurityManager(BaseSecurityManager):

    user_model = models.User

    userdbmodelview = UserDBModelView
    
    groupmodelview = GroupModelView
    
    def __init__(self, appbuilder):
        """
            SecurityManager contructor
            param appbuilder:
                F.A.B AppBuilder main object
            """
            
        self.groupmodelview.datamodel = MongoEngineInterface(models.Group)
        self.userdbmodelview.datamodel = MongoEngineInterfaceByGroup(self.user_model)
        self.userldapmodelview.datamodel = MongoEngineInterfaceByGroup(self.user_model)
        self.useroidmodelview.datamodel = MongoEngineInterfaceByGroup(self.user_model)
        self.useroauthmodelview.datamodel = MongoEngineInterfaceByGroup(self.user_model)
        self.userremoteusermodelview.datamodel = MongoEngineInterfaceByGroup(self.user_model)
        self.userstatschartview.datamodel = MongoEngineInterfaceByGroup(self.user_model)
        self.rolemodelview.datamodel = MongoEngineInterface(self.role_model)
        self.permissionmodelview.datamodel=MongoEngineInterface(self.permission_model)
        self.viewmenumodelview.datamodel=MongoEngineInterface(self.viewmenu_model)
        self.permissionviewmodelview.datamodel=MongoEngineInterface(self.permissionview_model)
        super(SecurityManager, self).__init__(appbuilder)
        self.create_db()
    
    def add_user(self, username, first_name, last_name, email, role, password='', group=None):
        """
            Generic function to create user
        """
        try:
            _group = None
            if group:
                _group, created = models.Group.objects.get_or_create(name=group)
            
            user = self.user_model()
            user.group = _group
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.active = True
            user.roles.append(role)
            user.password = generate_password_hash(password)
            user.save()
            log.info("Added user %s to user list." % username)
            return user
        except Exception as e:
            log.error(
                "Error adding new user to database. {0}".format(
                    str(e)))
            return False
        
        return user
    
    def register_views(self):
        group_view = self.appbuilder.add_view(self.groupmodelview, "List Groups", icon="fa-group", label=lazy_gettext('List Groups'),
                                             category="Security", category_icon="fa-cogs")
        BaseSecurityManager.register_views(self)
        #group_view.related_views = [self.user_view.__class__]
        
    
    def get_all_users(self):
        return models.User.objects
    