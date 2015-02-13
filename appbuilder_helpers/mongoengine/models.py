# -*- coding: utf-8 -*-

import datetime

from mongoengine import fields
from mongoengine import NULLIFY, CASCADE, DENY, PULL
from mongoengine import OperationError, ValidationError, NotUniqueError

try:
    from flask_mongoengine import MongoEngine
    db = MongoEngine()
    Document = db.Document
    EmbeddedDocument = db.EmbeddedDocument
    DynamicDocument = db.DynamicDocument
    DynamicEmbeddedDocument = db.DynamicEmbeddedDocument
except:
    from mongoengine import Document, EmbeddedDocument, DynamicDocument, DynamicEmbeddedDocument

from flask_appbuilder._compat import as_unicode
from flask_appbuilder.security.mongoengine.models import Role, get_user_id

class Group(Document):
    
    name = fields.StringField(max_length=80, unique=True, required=True)
    
    active = fields.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name
    
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
    

    meta = {
        'collection': 'group',
        'indexes': ['name'],
    }


class User(Document):

    #TODO: required or config options
    #TODO: cascade
    group = fields.ReferenceField(Group)
    
    first_name = fields.StringField(max_length=64, required=True)

    last_name = fields.StringField(max_length=64, required=True)
    
    username = fields.StringField(max_length=32, required=True, unique=True)
    
    password = fields.StringField(max_length=256)
    
    active = fields.BooleanField()
    
    email = fields.StringField(max_length=64, required=True, unique=True)
    
    last_login = fields.DateTimeField()
    
    login_count = fields.IntField()
    
    fail_login_count = fields.IntField()
    
    roles = fields.ListField(fields.ReferenceField(Role))
    
    created_on = fields.DateTimeField(default=datetime.datetime.now)
    
    changed_on = fields.DateTimeField(default=datetime.datetime.now)

    created_by = fields.ReferenceField('self', default=get_user_id())
    
    changed_by = fields.ReferenceField('self', default=get_user_id())
    
    def get_group_name(self):
        return self.group.name if self.group else None
    group_name = property(fget=get_group_name)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return as_unicode(self.id)

    def get_full_name(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)

    def __unicode__(self):
        return self.get_full_name()
    
    meta = {
        'collection': 'user',
        'indexes': ['username', 'email', 'roles', 'group'],
    }
