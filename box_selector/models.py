from django.db import models




class Product(models.Model):
    name = models.CharField(max_length=200)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name



class Box(models.Model):
    name = models.CharField(max_length=200)
    internal_length = models.DecimalField(max_digits=10, decimal_places=2)
    internal_width = models.DecimalField(max_digits=10, decimal_places=2)
    internal_height = models.DecimalField(max_digits=10, decimal_places=2)
    max_weight = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name