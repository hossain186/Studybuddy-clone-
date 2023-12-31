from django.db import models

# Create your models here.
from django.contrib.auth.models import User


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)

    Topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null= True)

    name = models.CharField(max_length=200)

    discriptions = models.TextField(null= True, blank= True)
    participents = models.ManyToManyField(User,related_name="participents" , blank=True )
    created = models.DateTimeField(auto_now_add= True)
    update = models.DateTimeField(auto_created=True)
    class Meta:
        ordering = ['-created' , '-update']
    
    def __str__(self):
        return self.name
    
class Message(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    body = models.TextField()
    created = models.DateTimeField(auto_now=True)
    update = models.DateTimeField(auto_now_add= True)

    class Meta:
        ordering = ['-created' , '-update']
    

    def __str__(self) :
        return self.body

