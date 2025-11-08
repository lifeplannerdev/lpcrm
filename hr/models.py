from django.db import models

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    join_date = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    penalty = models.CharField(max_length=100, blank=True, null=True)
    attendance = models.TextField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
    
