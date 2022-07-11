from datetime import datetime

from django.db import models
from django.forms.models import model_to_dict

from core.user.models import User


class UserAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)
    hour_joined = models.TimeField(default=datetime.now)
    ip_address = models.CharField(max_length=30)
    device = models.CharField(max_length=150)

    def __str__(self):
        return self.ip_address

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['date_joined'] = self.date_joined.strftime('%d-%m-%Y')
        item['hour_joined'] = self.hour_joined.strftime('%H:%M %p')
        return item

    class Meta:
        verbose_name_plural = 'Acceso de Usuario'
        verbose_name = 'Accesos de Usuario'
        default_permissions = ()
        permissions = (
            ('view_user_access', 'Can view Acceso de Usuario'),
            ('delete_user_access', 'Can delete Acceso de Usuario'),
        )
        ordering = ['-id']
