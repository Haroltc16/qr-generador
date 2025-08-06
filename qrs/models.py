from django.db import models

class QRCode(models.Model):
    nombre = models.CharField(max_length=100)
    url_destino = models.URLField()
    imagen_qr = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    visitas = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre