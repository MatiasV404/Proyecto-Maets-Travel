from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class Genero(models.Model):
    id_genero = models.AutoField(primary_key=True)
    genero = models.CharField(max_length=30)
    
    def __str__(self):
        return self.genero
    
class LugarVisita(models.Model):
    nombre = models.CharField(max_length=100)
    valor_temporada_alta = models.IntegerField()
    valor_temporada_baja = models.IntegerField()

    def __str__(self):
        return self.nombre

class Equipamiento(models.Model):
    equipamiento = models.CharField(max_length=150)
    precio = models.IntegerField()
    cantidad = models.IntegerField()

    def __str__(self):
        return self.title


class Persona(models.Model):
    rut = models.CharField(max_length=12)
    primer_nombre = models.CharField(max_length=100)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100)
    lugar_visita = models.ForeignKey(LugarVisita, on_delete=models.CASCADE)  # Asegúrate de tener definido el modelo Lugar

    def __str__(self):
        return self.rut

class Donacion(models.Model):
    nombre = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Donation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)