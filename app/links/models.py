# links/models.py
from django.db import models
from django.conf import settings # Para referenciar al User model correctamente

# --- Modelos de la Fase 1 y 2 ---

class URL(models.Model):
    """
    Modelo que representa una URL acortada.
    Corresponde a la tabla 'URLs'.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Si el usuario se borra, el enlace queda "anónimo"
        null=True,
        blank=True, # Permite enlaces anónimos
        related_name="urls"
    )
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=10, unique=True, db_index=True) # db_index es CRÍTICO para el rendimiento
    created_at = models.DateTimeField(auto_now_add=True) # Se establece automáticamente al crear
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # El campo 'total_clicks' se elimina. Se calculará dinámicamente desde ClickEvent.
    # Esto es más escalable y preciso.

    def __str__(self):
        return f"{self.short_code} -> {self.original_url[:50]}"

class ClickEvent(models.Model):
    """
    Modelo que registra cada clic en una URL.
    Corresponde a la tabla 'ClickEvents'.
    """
    url = models.ForeignKey(URL, on_delete=models.CASCADE, related_name="clicks") # Si se borra la URL, se borran sus clics
    clicked_at = models.DateTimeField(auto_now_add=True)
    ip_address_hash = models.CharField(max_length=64)
    user_agent = models.TextField(null=True, blank=True)
    referer_url = models.URLField(max_length=2048, null=True, blank=True)
    country_code = models.CharField(max_length=2, null=True, blank=True)
    city_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Click on {self.url.short_code} at {self.clicked_at}"

# --- Modelos de la Fase 3 ---

class Tag(models.Model):
    """
    Modelo para las etiquetas que los usuarios pueden asignar a sus URLs.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tags")
    name = models.CharField(max_length=50)

    class Meta:
        # Un usuario no puede tener dos etiquetas con el mismo nombre
        unique_together = [['user', 'name']]

    def __str__(self):
        return self.name

# ¡Magia de Django! La tabla de unión URL_Tags se gestiona a través de un ManyToManyField.
# Lo añadimos al modelo URL:

class URL(models.Model): # Versión final del modelo URL con el campo ManyToMany
    # ... todos los campos de antes ...
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="urls")
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=10, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    tags = models.ManyToManyField(Tag, blank=True, related_name="urls") # Relación Muchos a Muchos

    def __str__(self):
        return f"{self.short_code} -> {self.original_url[:50]}"


class CustomAlias(models.Model):
    """
    Modelo para alias personalizados. Usa una relación Uno a Uno.
    Corresponde a la tabla 'CustomAliases'.
    """
    alias = models.CharField(max_length=100, primary_key=True) # El alias es la clave primaria
    url = models.OneToOneField(URL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Alias '{self.alias}' for {self.url.short_code}"
