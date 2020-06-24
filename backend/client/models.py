from django.db import models
from django.contrib.auth.models import User


#possibly change all null possibilities to blank too


class client(models.Model):
    name = models.CharField(max_length=100, null=False)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=5, null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=100, null=False)
    #ead = models.ForeignKey(leadContact, null=True, on_delete=models.SET_NULL)



class leadContact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    company = models.ForeignKey(client, on_delete=models.CASCADE)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now=True)


#project may need to be seperated and added on to
class project(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)


class projectWorker(models.Model):
    pName = models.ForeignKey(project, on_delete=models.CASCADE)
    wName = models.ForeignKey(User, on_delete=models.CASCADE)

