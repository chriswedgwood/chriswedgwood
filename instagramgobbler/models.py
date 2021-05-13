from django.db import models


class InstaToken(models.Model):
    user_id = models.BigIntegerField(null=False, blank=False)
    long_lived_token = models.TextField(null=False, blank=False)
    expiry_date = models.DateField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_id} - {self.expiry_date}'
