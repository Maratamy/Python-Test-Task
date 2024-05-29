from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3)
    currency = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class CurrencyRate(models.Model):
    date = models.DateField()
    rate = models.FloatField()
    code = models.CharField(max_length=255)

class Parameter(models.Model):
    date = models.DateField()


class ExchangeRate(models.Model):
    date = models.DateField()
    country = models.TextField(max_length=255)
    base_rate = models.FloatField()
    rate = models.FloatField()
    relative_change = models.FloatField()

    def __str__(self):
        return f"{self.country.code} {self.date} {self.relative_change}"