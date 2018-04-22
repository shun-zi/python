# Generated by Django 2.0.3 on 2018-04-03 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=32)),
                ('ip', models.CharField(max_length=32)),
                ('port', models.IntegerField()),
                ('power', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='MachineGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('create_time', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='machine',
            name='machine_group',
            field=models.ForeignKey(on_delete=True, to='machine.MachineGroup'),
        ),
    ]
