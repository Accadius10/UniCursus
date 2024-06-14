from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash the password if it's a new object
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, password):
        return check_password(password, self.password)

