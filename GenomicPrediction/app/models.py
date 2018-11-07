from django.contrib.auth.models import User
"""
Definition of models.
"""

from django.db import models

# Create your models here.
class Patient(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 100)
    email = models.EmailField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Embryo(models.Model):
    code_name = models.CharField(max_length = 100)
    karyotype = models.CharField(max_length = 100)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def embryo_sex(self):
        tokens = self.karyotype.split(',')
        try:        
            if tokens[1].lower() == 'XY'.lower():
                return 'Male'
            else:
                return 'Female'
        except IndexError:
            return ''

    @property
    def embryo_downs(self):
        tokens = self.karyotype.split(',')
        try:
            if int(tokens[0]) == 46:
                return 'Normal'
            elif int(tokens[0]) > 46:
                return 'Downs'
            else:
                return
        except IndexError:
            return ''
        except ValueError:
            return ''
