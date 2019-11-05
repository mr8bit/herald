from django.db import models


# Create your models here.
class User(models.Model):
    """
        Модель пользователя
    """
    lang = ((0, 'Русский'), (1, "English"))
    # Базовые значения
    choices = ((0, 'Telegram'), (1, 'Viber'), (2, 'VK'), (3, 'Facebook'))
    user_id = models.CharField(max_length=300, default='', primary_key=True, verbose_name="ID Пользователя")
    messenger = models.IntegerField(choices=choices, verbose_name="Мессенджер")
    first_name = models.CharField(max_length=300, default='', blank=True, null=True, verbose_name="Имя")
    second_name = models.CharField(max_length=300, default='', blank=True, null=True, verbose_name="Фамилия")
    state = models.CharField(max_length=300, blank=True, null=True, verbose_name="Место нахождение пользователя")
    prev_state = models.CharField(max_length=300, blank=True, null=True, verbose_name="Предыдущее состояние")
    telegram_slug = models.CharField(max_length=300, blank=True, null=True, verbose_name="Телеграм ник")

    # Значения модификаторы
    language = models.IntegerField(choices=lang, default=0)
    group = models.CharField(max_length=300, verbose_name="Номер группы", default="")

    def __str__(self):
        if self.messenger == 0:
            return self.telegram_slug
        return "{} {}".format(self.first_name, self.second_name)


class Notification(models.Model):
    """
        Млдель оповещений
    """
    name = models.CharField(max_length=300, verbose_name="Название")
    message = models.TextField(verbose_name="Сообщение")


class Request(models.Model):
    """
        Запросы
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Пользователь", blank=True, null=True)
    state = models.TextField(verbose_name="Экран", blank=True, null=True)
    date = models.DateField(auto_now=True, verbose_name="Время")
    text = models.TextField(blank=True, null=True )

    @staticmethod
    def create_request(user, state, text):
        Request.objects.create(user=user, state=state, text=text).save()


class Error(models.Model):
    """
        Ошибки
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Пользователь", blank=True, null=True)
    state = models.TextField(verbose_name="Экран", blank=True, null=True)
    date = models.DateField(auto_now=True, verbose_name="Время")
    text = models.TextField(blank=True, null=True )

    @staticmethod
    def create_error(user, state, text):
        Error.objects.create(user=user, state=state).save()

