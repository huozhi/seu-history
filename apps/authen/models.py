from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class StudentUserManager(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, username, password):
        user = self.create_user(
            username,
            password=password,
        )
        user.is_admin = False
        user.save(using=self._db)
        return user
 

class Student(AbstractBaseUser):
    objects = StudentUserManager()
    USERNAME_FIELD = 'username'

    username = models.CharField(max_length=30, blank=False, unique=True)
    start_time = models.DateTimeField(auto_now_add=True, blank=True)
    end_time = models.DateTimeField(auto_now_add=True, blank=True)
    score = models.IntegerField(default=0, blank=False)

    def __unicode__(self):
        return self.username

    class Meta:
        ordering = ['username']


