
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, default="")
    completed = models.BooleanField(default=False) # Unificado con "d"
    deadline = models.DateField(null=True, blank=True) # Unificado a Date
    priority = models.CharField(max_length=10, null=True, blank=True)
    # Idealmente seria una tabla
    tags_raw = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    PRIORITY_CHOICES = [
        ('1', 'Baja'),
        ('2', 'Media'),
        ('3', 'Alta'),
    ]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, blank=True, null=True)

    # Función para convertir el string de etiquetas en una lista
    def get_tags_list(self):
        if self.tags_raw:
            return [tag.strip() for tag in self.tags_raw.split(',')]
        return []

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['completed','created']