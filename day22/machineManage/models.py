from django.db import models

# Create your models here.

from django.db import models

# Create your models here.


class Business(models.Model):
    caption = models.CharField(max_length=32)
    def db_name(self):
        return "Business"


class Host(models.Model):
    hostname = models.CharField(max_length=32, db_index=True)
    ip = models.GenericIPAddressField(protocol="ipv4", db_index=True)
    port = models.IntegerField()
    business = models.ForeignKey(to="Business", to_field='id', on_delete=True)
    def db_name(self):
        return "Host"


class Application(models.Model):
    name = models.CharField(max_length=32)
    r = models.ManyToManyField("Host")

    def db_name(self):
        return "Application"

class ACCOUNT(models.Model):
    username = models.CharField(max_length=32, db_index=True, primary_key=True)
    email = models.EmailField(max_length=32, db_index=True, primary_key=True)
    password = models.CharField(max_length=32)

    def db_name(self):
        return "ACCOUNT"