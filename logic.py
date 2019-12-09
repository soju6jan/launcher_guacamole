# -*- coding: utf-8 -*-
#########################################################
# python
import os
import sys
import traceback
import logging
import threading
import subprocess
import platform
import time
# third-party

# sjva 공용
from framework import app, path_app_root, db
from framework.logger import get_logger
from framework.util import Util

# 패키지
from .model import ModelSetting

package_name = __name__.split('.')[0].split('_sjva')[0]
logger = get_logger(package_name)
#########################################################
import requests
import urllib
import time
import threading
from datetime import datetime

class Logic(object):
    db_default = {
        'auto_start' : 'False',
        'url' : 'http://localhost:8080/guacamole',
    }

    mysql_process = None
    current_process = None

    @staticmethod
    def db_init():
        try:
            for key, value in Logic.db_default.items():
                if db.session.query(ModelSetting).filter_by(key=key).count() == 0:
                    db.session.add(ModelSetting(key, value))
            db.session.commit()
        except Exception as e: 
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())


    @staticmethod
    def plugin_load():
        try:
            if platform.system() != 'Windows':
                custom = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'guacamole')    
                os.system("chmod 777 -R %s" % custom)

            logger.debug('%s plugin_load', package_name)
            # DB 초기화 
            Logic.db_init()

            # 편의를 위해 json 파일 생성
            from plugin import plugin_info
            Util.save_from_dict_to_json(plugin_info, os.path.join(os.path.dirname(__file__), 'info.json'))

            # 자동시작 옵션이 있으면 보통 여기서 
            if ModelSetting.query.filter_by(key='auto_start').first().value == 'True':
                Logic.scheduler_start()
        except Exception as e: 
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())


    @staticmethod
    def plugin_unload():
        try:
            Logic.kill()
        except Exception as e: 
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())


    @staticmethod
    def scheduler_start():
        try:
            Logic.run()
        except Exception as e: 
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())


    @staticmethod
    def scheduler_stop():
        try:
            Logic.kill()
        except Exception as e: 
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())


    @staticmethod
    def setting_save(req):
        try:
            for key, value in req.form.items():
                logger.debug('Key:%s Value:%s', key, value)
                entity = db.session.query(ModelSetting).filter_by(key=key).with_for_update().first()
                entity.value = value
            db.session.commit()
            return True                  
        except Exception as e: 
            logger.error('Exception:%s %s', key)
            logger.error(traceback.format_exc())
            return False


    @staticmethod
    def get_setting_value(key):
        try:
            return db.session.query(ModelSetting).filter_by(key=key).first().value
        except Exception as e: 
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())


    @staticmethod
    def scheduler_function():
        try:
            pass
        except Exception as e: 
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())
    

    # 기본 구조 End
    ##################################################################

    @staticmethod
    def run():
        if Logic.current_process is None:
            cmd = ['/etc/guacamole/run.sh']
            Logic.mysql_process = subprocess.Popen(cmd)

            cmd = ['/var/lib/tomcat/bin/catalina.sh', 'start']
            Logic.current_process = subprocess.Popen(cmd)
    
    @staticmethod
    def kill():
        try:
            tmp = '/var/lib/tomcat/bin/catalina.sh'
            if os.path.exists(tmp):
                cmd = [tmp, 'stop']
                subprocess.Popen(cmd)
                time.sleep(1)

            if Logic.current_process is not None and Logic.current_process.poll() is None:
                import psutil
                process = psutil.Process(Logic.current_process.pid)
                for proc in process.children(recursive=True):
                    proc.kill()
                process.kill()
            Logic.current_process = None

            if Logic.mysql_process is not None and Logic.mysql_process.poll() is None:
                import psutil
                process = psutil.Process(Logic.mysql_process.pid)
                for proc in process.children(recursive=True):
                    proc.kill()
                process.kill()
            Logic.mysql_process = None
        except Exception as e: 
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())

    @staticmethod
    def install():
        try:
            def func():
                import system
                Logic.kill()
                commands = [
                    ['msg', u'잠시만 기다려주세요.'],
                    ['/app/data/custom/launcher_guacamole_sjva/guacamole/install.sh'],
                    ['msg', u'설치가 완료되었습니다.']
                ]
                system.SystemLogicCommand.start('설치', commands)
            t = threading.Thread(target=func, args=())
            t.setDaemon(True)
            t.start()
        except Exception as e: 
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())

    @staticmethod
    def is_installed():
        try:
            target = '/usr/bin/mysqld'
            if os.path.exists(target):
                return True
            else:
                return False
        except Exception as e: 
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())
