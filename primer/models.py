from django.db import models
import re
# Create your models here
class Prime(models.Model):
    number = models.IntegerField(unique=True)
    def __str__(self):
        return str(self.number)
    def prime_check(self):
        if re.match(r'^1?$|^(11+?)\1+$', '1' * self.number):
            raise Exception('Number is not prime')
