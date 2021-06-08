from django.apps import AppConfig
from siruco.db import Database
from os import getenv

class T1AuthConfig(AppConfig):
    name = 't1_auth'

    def ready(self):
        if getenv("DATABASE_URL") == None:
          print("Configuring Auth App")
        else:
            db = Database(schema="siruco")
            # create schema
            db.query(f'''
                     INSERT INTO AKUN_PENGGUNA(Username,Password,Peran) VALUES (
                          'admin@siruco.com',
                          '{getenv('ADMIN_PASS')}',
                          'admin_sistem'
                      ) ON CONFLICT DO NOTHING;
                      
                      INSERT INTO ADMIN(Username) VALUES (
                          'admin@siruco.com'
                      ) ON CONFLICT DO NOTHING;
                     ''')
