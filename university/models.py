from django.db import models

# Create your models here.


class Teacher(models.Model):
    first_name = models.CharField(max_length=300, verbose_name="Имя")
    second_name = models.CharField(max_length=300, verbose_name="Отчество")
    last_name = models.CharField(max_length=300, verbose_name="Фамилия")
    guid = models.CharField(max_length=500, verbose_name="Идентификатор препода")