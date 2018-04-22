from django.db import models

# Create your models here.


class Business(models.Model):
    caption = models.CharField(max_length=32)


class Host(models.Model):
    hostname = models.CharField(max_length=32, db_index=True)
    ip = models.GenericIPAddressField(protocol="ipv4", db_index=True)
    port = models.IntegerField()
    business = models.ForeignKey(to="Business", to_field='id', on_delete=True)


class Application(models.Model):
    name = models.CharField(max_length=32)
    r = models.ManyToManyField("Host")