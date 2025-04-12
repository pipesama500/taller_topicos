from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode
from io import BytesIO
from django.core.files import File


class Unidad(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Torre(models.Model):
    id_unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Piso(models.Model):
    id_torre = models.ForeignKey(Torre, on_delete=models.CASCADE)
    numero = models.IntegerField()

    def __str__(self):
        return f"Piso {self.numero} - {self.id_torre.nombre}"

class Apartamento(models.Model):
    id_piso = models.ForeignKey(Piso, on_delete=models.CASCADE)
    numero = models.IntegerField()

    def __str__(self):
        return f"Apartamento {self.numero} - {self.id_piso}"

class Roles(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('id_rol', Roles.objects.get(nombre='Administrador'))
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    id_rol = models.ForeignKey(Roles, on_delete=models.CASCADE)
    id_apartamento = models.ForeignKey(Apartamento, null=True, blank=True, on_delete=models.SET_NULL)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.email}"

class Anuncio(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-fecha_publicacion']

class Proveedor(models.Model):
    TIPO_CHOICES = [
        ('domicilio', 'Domicilio'),
        ('paquete', 'Paquete'),
    ]
    
    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_display()}"

class Visita(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('rechazada', 'Rechazada'),
    ]

    nombre_visitante = models.CharField(max_length=100)
    apellido_visitante = models.CharField(max_length=100)
    fecha_visita = models.DateTimeField()
    es_frecuente = models.BooleanField(default=False)
    fecha_expiracion_frecuente = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    notificacion = models.BooleanField(default=False)
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    mensaje_qr = models.CharField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.es_frecuente and not self.mensaje_qr:
            self.mensaje_qr = f"visita-{self.apartamento.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            
            qr_image = qrcode.make(self.mensaje_qr)
            buffer = BytesIO()
            qr_image.save(buffer, format='PNG')
            file_name = f'{self.nombre_visitante}_{self.apellido_visitante}_qr.png'
            self.qr_code.save(file_name, File(buffer), save=False)
            
        super().save(*args, **kwargs)

class Domicilio(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('rechazado', 'Rechazado'),
    ]

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, limit_choices_to={'tipo': 'domicilio'})
    proveedor_personalizado = models.CharField(max_length=100, blank=True, null=True)
    nombre_producto = models.CharField(max_length=100, blank=True, null=True)
    fecha_anuncio = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    notificacion = models.BooleanField(default=False)
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)

    def __str__(self):
        return f"Domicilio de {self.proveedor} para el apartamento {self.apartamento}"

class Paquete(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('recogido', 'Recogido'),
    ]

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, limit_choices_to={'tipo': 'paquete'})
    proveedor_personalizado = models.CharField(max_length=100, blank=True, null=True)
    nombre_producto = models.CharField(max_length=100, blank=True, null=True)
    fecha_anuncio = models.DateTimeField(default=timezone.now)
    fecha_estimacion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    notificacion = models.BooleanField(default=False)
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)

    def __str__(self):
        return f"Paquete de {self.proveedor} para el apartamento {self.apartamento}"
