from django.db import models

# Create your models here.


class Machine(models.Model):
    hostname = models.CharField(max_length=32, null=False)
    ip = models.CharField(max_length=32, null=False)
    port = models.IntegerField(null=False)
    power = models.CharField(max_length=32)

    machine_group = models.ForeignKey(to='MachineGroup', to_field='id', on_delete=True)


class MachineGroup(models.Model):
    name = models.CharField(max_length=32, null=False)
    create_time = models.DateTimeField(auto_now=True, null=True)