# Generated by Django 4.1.2 on 2023-06-30 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_equipamiento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=12)),
                ('primer_nombre', models.CharField(max_length=100)),
                ('primer_apellido', models.CharField(max_length=100)),
                ('segundo_apellido', models.CharField(max_length=100)),
                ('lugar_visita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.lugarvisita')),
            ],
        ),
    ]