# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django.db import models
import bcrypt

# Create your models here.
Name_regex = re.compile(r'^[a-zA-Z]\w+$')

class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = []
        if len(postData['name']) < 3 or len(postData['username']) < 3:
            errors.append('Name and Username cannot be fewer than 3 characters')
        if not re.match(Name_regex, postData['name']) or not re.match(Name_regex, postData['username']):
            errors.append('Name and Username can have only letters')
        username = self.filter(username=postData['username'])
        # if len(username):
        #     errors.append("Username already exist")
        if len(postData['password']) < 8:
            errors.append('Password is too small')
        if not (postData['password'] == postData['confirm_password']):
            errors.append('Passwords do not match')
        if not errors:
            hashing = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(10))
            user = User.objects.create(
                name=postData['name'],
                username=postData['username'],
                password=hashing,
        )
            return user
        return errors
    def validate_login(self, postData):
        errors = []
        user = self.filter(username=postData['username'])
        if len(user):
            if bcrypt.checkpw(postData['password'].encode(),user[0].password.encode()):
                return user[0]
            else:
                errors.append("Incorrect Password")
                return errors
        else:
            errors.append("Incorrect Email and Password")
            return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
 

