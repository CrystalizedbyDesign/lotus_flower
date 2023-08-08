from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Sign_up:
    db = 'lotus_flower'
    def __init__(self, user):
        self.id = user['id']
        self.first_name = user['first_name']
        self.last_name = user['last_name']
        self.username = user['username']
        self.age = user['age']
        self.email = user['email']
        self.password = user['password']
        self.created_at = user['created_at']
        self.updated_at = user['updated_at']
        
    
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO sign_up (first_name, last_name, username, age, email, password) 
                VALUES (%(first_name)s, %(last_name)s, %(username)s, %(age)s, %(email)s, %(password)s);"""
        return connectToMySQL(cls.db).query_db(query, data)

    

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sign_up;"
        results = connectToMySQL(cls.db).query_db(query)
        user = []
        for row in results:
            user.append(cls(row))
        print(results)
        return user
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM sign_up WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_login_id(cls, data):
        query = "SELECT * FROM sign_up WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        if results:  # Check if the results list is not empty
            return cls(results[0])
        else:
            return None  # Return

    @staticmethod
    def validate_sign_up(user):
        is_valid = True
        query = "SELECT * FROM sign_up WHERE email = %(email)s;"
        results = connectToMySQL(Sign_up.db).query_db(query, user)
    
        if len(results) >= 1:
            flash("Email taken", "sign_up") 
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "sign_up")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("first_name must be at least 3 characters", "sign_up")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("last_name must be at least 3 characters", "sign_up")
            is_valid = False
        if  len(user['email']) < 3:
            flash("email must be at least 3 characters", "sign_up")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "sign_up")
            is_valid = False# test whether a field matches the pattern
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match", "sign_up")
            is_valid = False

        return is_valid