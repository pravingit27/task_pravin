from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class student(models.Model):
    name = models.CharField(default=True,max_length=100,db_index=True)
    #slug = models.SlugField(max_length=200,db_index=True,unique=True)
    rollno = models.CharField(default=0,max_length=100,primary_key=True)
    dob = models.DateField(null=True,blank=True)
    #marks = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(student, self).save(*args, **kwargs)

class Mark(models.Model):
    studentmarks = models.IntegerField(default=0, null=True, blank=True)
    #marks = models.OneToOneField(student,on_delete=models.CASCADE,null=True,blank=True)
    studentname = models.ForeignKey(student,related_name='students',on_delete=models.CASCADE,null=True,blank=True)
    grade = models.ForeignKey('Grade',related_name='marks',on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{}'.format(self.studentname)
    

class Grade(models.Model):
    grade = models.CharField(max_length=50,unique=True,primary_key=True)
    sm = models.ForeignKey(Mark,related_name='marks',on_delete=models.CASCADE,null=True,blank=True)

class User(AbstractUser):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=300,unique=True)
    password = models.CharField(max_length=250)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= []
    
