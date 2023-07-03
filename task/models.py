from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('Pendiente', 'Pendiente'),
    ('Atrasada', 'Atrasada'),
    ('En Proceso', 'En Proceso'),
    ('En Revisión', 'En Revisión'),
    ('Aprobada', 'Aprobada'),
    ('Rechazada', 'Rechazada')
]

class Task(models.Model):
    description = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_of")
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="supervisor_of")
    status = models.CharField(max_length=20,choices=STATUS_CHOICES, default='Pendiente')
    deadline = models.DateField()

    def __str__(self):
        return self.description
