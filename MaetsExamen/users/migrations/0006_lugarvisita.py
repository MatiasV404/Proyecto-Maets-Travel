# Generated by Django 4.1.2 on 2023-06-30 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_genero'),
    ]

    operations = [
        migrations.CreateModel(
            name='LugarVisita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('valor_temporada_alta', models.IntegerField()),
                ('valor_temporada_baja', models.IntegerField()),
            ],
        ),
    ]
