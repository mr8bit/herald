from django.db import models


# Create your models here.
class User(models.Model):
    """
        Модель пользователя
    """

    choices = ((0, 'Telegram'), (1, 'Viber'))
    user_id = models.CharField(max_length=300, default='', primary_key=True, verbose_name="ID Пользователя")
    messenger = models.IntegerField(choices=choices, verbose_name="Мессенджер")
    read_invitation = models.BooleanField(default=False)
    first_name = models.CharField(max_length=300, default='', blank=True, null=True, verbose_name="Имя")
    second_name = models.CharField(max_length=300, default='', blank=True, null=True, verbose_name="Фамилия")
    state = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.second_name)
