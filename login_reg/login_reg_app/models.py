from django.db import models
from datetime import date,datetime
import re


class UserManager(models.Manager):

    def reg_validator(self,postData):
        today = datetime.now()
        birth_date = datetime.strptime(postData['birthday'], '%Y-%m-%d')
        age = (today - birth_date).days/365
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 3:
            errors['first_name'] = 'First Name must be at least 3 characters!'
        if len(postData['last_name']) < 3:
            errors['last_name'] = 'Last Name must be at least 3 characters!'
        if birth_date > today:
            errors['birthday'] = "Birthday must be in the past!"
        if age < 13:
            errors['birthday'] = "You must be at least 13 years old to register!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid Email'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters!'
        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = 'Passwords do not match!'
        return errors
    
    def login_validator(self,postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['login_email']):
            errors['login_email'] = 'Invalid Email/Password'
        if len(postData['login_password']) <8:
            errors['login_password'] = 'Invalid Email/Password'
        return errors


class User(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    birthday=models.DateField(null=True, blank=True, default=None)
    email=models.CharField(max_length=45)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    message_content=models.TextField()
    message_user=models.ForeignKey(User, related_name='messages', on_delete = models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment_content=models.TextField()
    comment_user=models.ForeignKey(User, related_name='comments', on_delete = models.CASCADE)
    message=models.ForeignKey(Message, related_name='comments_messages', on_delete = models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


