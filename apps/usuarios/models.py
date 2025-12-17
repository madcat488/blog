# apps/usuarios/models.py - CORREGIDO
from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Usuario(AbstractUser):
    # Campos básicos
    nombre = models.CharField(_('Nombre'), max_length=30, blank=True)
    apellido = models.CharField(_('Apellido'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    
    # Campos adicionales
    fecha_nacimiento = models.DateField(_('Fecha de Nacimiento'), null=True, blank=True)
    telefono = models.CharField(_('Teléfono'), max_length=20, blank=True)
    colaborador = models.BooleanField(_('Colaborador'), default=False)
    
    # Imagen de perfil
    imagen = models.ImageField(
        _('Foto de perfil'),
        upload_to='usuarios/',
        null=True,
        blank=True,
        default='usuarios/default_user.png'
    )
    
    # Campos timestamp - CORREGIDOS
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)  # Usa este campo
    # Si realmente quieres fecha_creacion, haz:
    # fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Metadata
    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        ordering = ['-date_joined']  # Cambiado de fecha_creacion a date_joined
    
    def __str__(self):
        if self.nombre and self.apellido:
            return f"{self.nombre} {self.apellido}"
        return self.username
    
    @property
    def nombre_completo(self):
        if self.nombre and self.apellido:
            return f"{self.nombre} {self.apellido}"
        return self.username
    
    @property
    def iniciales(self):
        if self.nombre and self.apellido:
            return f"{self.nombre[0]}{self.apellido[0]}".upper()
        return self.username[0].upper() if self.username else "U"
    
    @property
    def edad(self):
        if not self.fecha_nacimiento:
            return None
        
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year
        
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1
        
        return edad