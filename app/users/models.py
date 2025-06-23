# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Plan(models.Model):
    """
    Modelo para los niveles de suscripción (ej: Gratuito, Pro).
    Corresponde a la Tabla 'Plans' de la Fase 3.
    """
    PLAN_FREE = 1
    PLAN_PRO = 2
    PLAN_ENTERPRISE = 3
    PLAN_CHOICES = [
        (PLAN_FREE, 'Gratuito'),
        (PLAN_PRO, 'Pro'),
        (PLAN_ENTERPRISE, 'Empresa'),
    ]

    id = models.PositiveSmallIntegerField(choices=PLAN_CHOICES, primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    url_limit = models.PositiveIntegerField(null=True, blank=True, help_text="Límite de URLs por mes. NULL para ilimitado.")
    custom_alias_allowed = models.BooleanField(default=False)
    analytics_retention_days = models.PositiveIntegerField(default=30, help_text="Días de retención de datos de clics.")

    def __str__(self):
        return self.name

class User(AbstractUser):
    """
    Modelo de Usuario personalizado.
    Hereda de AbstractUser para obtener username, email, password, etc.
    """
    # No necesitamos definir username, email, password, last_login, is_active.
    # Vienen incluidos en AbstractUser.

    plan = models.ForeignKey(
        Plan,
        on_delete=models.SET_NULL, # Si se borra un plan, los usuarios no se borran, su plan queda nulo.
        null=True,
        blank=True,
        related_name="users",
        help_text="Plan de suscripción del usuario."
    )

    def __str__(self):
        return self.username
