import os
import sys
import json
import time
import tornado
import tornado.escape
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from tornado.web import RequestHandler
from tornado.httpclient import HTTPResponse
from models.user_models import Base, GoogleUser, FacebookUser

from google.oauth2 import id_token
from google.auth.transport import requests


if os.path.isfile('credentials.json') is False:
    sys.exit('credentials.json not found.')

credentials = json.loads(open('credentials.json', 'r').read())
ClientID = credentials['web']['client_id']


class MainApiHandler(RequestHandler):
    def prepare(self):
        super().prepare()
        self.gdb = None
        self.get_db_connection()

    def get_db_connection(self):
        try:
            engine = create_engine("mysql+mysqlconnector://root:1234@localhost:3308/users")
            if not database_exists(engine.url):
                create_database(engine.url)

            Base.metadata.create_all(engine)

            Session = sessionmaker(bind=engine)
            self.gdb = Session()
            print('Database Connection Established...')

        except Exception:
            traceback.print_exc()
            raise tornado.web.HTTPError(503)



class HomePageHandler(MainApiHandler):
    def get(self):
        self.render('templates/home.html', ClientID=ClientID)


class TokenHandler(MainApiHandler):
    def post(self, *args, **kwargs):
        token = tornado.escape.json_decode(self.request.body)
        token = token['id_token']

        print(token)


        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            id_info = id_token.verify_oauth2_token(token, requests.Request(), ClientID)

            json_object = json.dumps(id_info, indent=4)
            json_file = open('token.json', 'w')
            json_file.write(json_object)

            current_time = int(time.time()) + 18000
            issuer = ['accounts.google.com', 'https://accounts.google.com']

            if id_info['aud'] == ClientID and id_info['iss'] in issuer and id_info['exp'] < current_time:
                record = self.gdb.query(GoogleUser).filter(GoogleUser.google_user_id == id_info['sub']).one_or_none()
                if record is None:
                    user = GoogleUser()
                    user.google_user_id = int(id_info['sub'])
                    user.name = id_info['name']
                    user.email = id_info['email']
                    user.picture = id_info['picture']

                    self.gdb.add(user)
                    self.gdb.flush()
                    self.gdb.commit()

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            # userid = idinfo['sub']
        except Exception:
            traceback.print_exc()


class SuccessPageHandler(RequestHandler):
    def get(self):
        self.render('templates/success.html')


class FbHandler(MainApiHandler):
    def post(self, *args, **kwargs):
        data = tornado.escape.json_decode(self.request.body)
        data = data['response']

        if 'error' in data:
            print(data['error'])
        else:
            print('logged in')
            json_object = json.dumps(data, indent=4)
            json_file = open('token_facebook.json', 'w')
            json_file.write(json_object)

            record = self.gdb.query(FacebookUser).filter(FacebookUser.fb_user_id == data['id']).one_or_none()
            if record is None:
                user = FacebookUser()
                user.fb_user_id = int(data['id'])
                user.name = data['name']
                user.email = data['email'] if 'email' in data else None
                user.gender = data['gender'] if 'gender' in data else None
                user.birth_day = data['birth_day'] if 'birth_day' in data else None

                self.gdb.add(user)
                self.gdb.flush()
                self.gdb.commit()







