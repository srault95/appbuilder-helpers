# -*- coding: utf-8 -*-

from flask_appbuilder import AppBuilder

from security import SecurityManager

def builder_factory(app=None,
                    session=None,
                    menu=None,
                    indexview=None,
                    base_template='appbuilder/baselayout.html',
                    static_folder='static/appbuilder',
                    static_url_path='/appbuilder',
                    security_manager_class=None):
    
    if not security_manager_class:
         security_manager_class = SecurityManager

    return AppBuilder(app=app, session=session, menu=menu, 
                      indexview=indexview, 
                      base_template=base_template, 
                      static_folder=static_folder, 
                      static_url_path=static_url_path, 
                      security_manager_class=security_manager_class)
    