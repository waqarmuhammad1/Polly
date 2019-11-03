# -*- coding: utf-8 -*-
from couchbase.cluster import Cluster, PasswordAuthenticator
from couchbase.exceptions import *




class CouchAPI():

    def __init__(self, username, password, ip):
        try:
            self.cluster = Cluster('couchbase://'+ip)
            self.cluster.authenticate(PasswordAuthenticator(username, password))

        except:
            raise Exception('Unable to verify user')

    def open_bucket(self):
        self.user_bucket = self.cluster.open_bucket('auth')
        self.email_bucket = self.cluster.open_bucket('auth_email')

    def authenticate(self, username, password):
        try:
            user_auth = self.user_bucket.get(username).value
            pwd = str(user_auth['pwd'])
            if pwd == password:
                return 'Login Successful'
            else:

                return 'Invalid username or password'
        except:
            try:
                user_auth = self.email_bucket.get(username).value
                pwd = str(user_auth['pwd'])
                if pwd == password:
                    return 'Login Successful'
                else:
                    return 'Invalid username or password'
            except CouchbaseError as e:
                return 'Invalid username or password'


    def store_user_auth(self, user, data):

        try:
            try:
                self.retrieve_data(user)
                return 'username or email already taken'
            except CouchbaseError as e:
                self.user_bucket.upsert(user, data)
                return 'Registration Successful'
        except:
            raise

    def store_email_auth(self, email, data):
        try:
            try:
                self.retrieve_data(email)
                return 'username or email already taken'
            except CouchbaseError as e:
                self.email_bucket.upsert(email, data)
                return 'Registration Successful'

        except:
            raise

    def replace_user_data(self, user, data):

        try:
            self.user_bucket.replace(user, data)
        except:
            raise

    def replace_email_data(self, user, data):

        try:
            self.email_bucket.replace(user, data)
        except:
            raise

    def retrieve_data(self, username):

        try:
            return self.user_bucket.get(username)
        except:
            try:
                return self.email_bucket.get(username)
            except:
                raise

couch = CouchAPI('Administrator', 'password', '0.0.0.0')
couch.open_bucket()

username = 'admin'
password = 'password'
email = 'waqar.muhammad@slu.edu'
first_name = 'Waqar'
last_name = 'Muhammad'
user_auth = {'first_name': first_name, 'last_name': last_name, 'email_id': email, 'pwd': password}
email_auth = {'first_name': first_name, 'last_name': last_name, 'user_name': username, 'pwd': password}

couch.store_user_auth('admin', user_auth)
couch.store_email_auth('waqar.muhammad@slu.edu', email_auth)
#
# print(couch.authenticate('waqar.muhammad@slu.edu', 'password'))