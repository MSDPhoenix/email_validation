from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



class User:
    def __init__(self,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def get_one(cls,data):
        query = '''
                SELECT * FROM users WHERE id = %(id)s;
                '''
        results = connectToMySQL('users').query_db(query,data)
        user = cls(results[0])
        return user

    @classmethod
    def get_all(cls):
        query = '''
                SELECT * FROM users;
                '''
        results = connectToMySQL('users').query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def save(cls,data):
        query = '''
                INSERT INTO users (first_name,last_name,email)
                VALUES (%(first_name)s,%(last_name)s,%(email)s)
                '''
        return connectToMySQL('users').query_db(query,data)

    @classmethod
    def update(cls,data):
        query = '''
                UPDATE users
                SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s
                WHERE id=%(id)s; 
                '''
        return connectToMySQL('users').query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = '''
                DELETE FROM users WHERE id=%(id)s;
                '''
        return connectToMySQL('users').query_db(query,data)

    @staticmethod
    def validate(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash('First name must be at least 2 characters.')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name must be at least 2 characters.')
            is_valid = False
        if len(user['email']) < 2:
            flash('Email must be at least 2 characters.')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address")
            is_valid = False
        all_email_addresses = []
        users = User.get_all()
        for registered_user in users:
            if user['email'] == registered_user.email:
                flash('There is already an account registered with this email.')
                is_valid = False
        # if len(user['first_name']) < 2:
        #     flash('Name must be at least 2 characters.')
        #     is_valid = False
        return is_valid