from hashlib import sha256
from passlib.hash import bcrypt
from db import DB
from mdict import *

"""
Users collections
    username
    email
    password_hash
    api_key_id
    api_key_secret_hash
    services
        - vanguard
            username
            password
            security_questions
                - <question>: <answer>
                - <question>: <answer>
                - <question>: <answer>
"""

PASSWORD_HASH_ROUNDS = 8

class Users(object):
    users = DB.users

    allowed_services = [
        "vanguard"
    ]

    @staticmethod
    def hash_password(password):
        return bcrypt.encrypt(password, rounds=PASSWORD_HASH_ROUNDS)

    @staticmethod
    def verify_password(password, p_hash):
        return bcrypt.verify(password, p_hash)

    @staticmethod
    def gen_api_key():
        return sha256().hexdigest()

    @staticmethod
    def register_user(username, email, password):
        # Make sure user doesn't already exist
        user = Users.find_user(username)
        if user is not None:
            raise RuntimeError("User {} already exists".format(username))

        user = Users.find_user_by_email(email)
        if user is not None:
            raise RuntimeError("User with email {} already exists".format(email))

        user = dict(user=username,
                    email=email,
                    password=Users.hash_password(password))

        # Generate an API key for the user
        user["api_key"] = Users.gen_api_key()

        # Save the user
        Users.users.insert(user)

    @staticmethod
    def delete_user(username):
        user = Users.find_user(username)
        if user is None:
            # user doesn't exist
            return

        # delete user
        Users.users.delete_one({'_id': user['_id']})

    @staticmethod
    def find_user(username):
        return Users.users.find_one(dict(user=username))

    @staticmethod
    def clean_user(user):
        # Remove the _id and password
        del user['_id']
        del user['password']
        return user

    @staticmethod
    def find_user_by_email(email):
        return Users.users.find_one(dict(email=email))

    @staticmethod
    def enroll_in_service(username, service_info):
        # Check user exists
        user = Users.find_user(username)
        if user is None:
            raise RuntimeError("User not found")

        service_name = service_info.get("service_name")
        if service_name not in Users.allowed_services:
            raise RuntimeError("This service is not supported")

        # Make sure user is not already enrolled
        if user.get("services", {}).get(service_name) is not None:
            raise RuntimeError("User is already enrolled in this service")

        mset(user, "services:{}".format(service_name), service_info)
        Users.users.update_one({'_id': user['_id']}, {'$set': {'services': user.get('services')}})

    @staticmethod
    def unenroll_from_service(username, service_name):
        user = Users.find_user(username)
        if user is None:
            raise RuntimeError("User not found")

        if mget(user, "services:{}".format(service_name)) is None:
            return

        del_filter = {'$unset': {}}
        del_filter['$unset']['services.{}'.format(service_name)] = 1
        Users.users.update_one({'_id': user['_id']}, del_filter)

    @staticmethod
    def register_security_answer(username, service_name, question, answer):
        user = Users.find_user(username)
        if user is None:
            raise RuntimeError("User not found")

        if mget(user, "services:{}".format(service_name)) is None:
            raise RuntimeError("User is not enrolled in service {}".format(service_name))

        set_filter = {'$set': {}}
        set_filter['$set']['services.{}.security_questions.{}'.format(service_name, question)] = answer
        Users.users.update_one({'_id': user['_id']}, set_filter)

    @staticmethod
    def auth_user(username, password):
        user = Users.find_user(username)
        p_hash = user.get("password")
        return Users.verify_password(password, p_hash)
