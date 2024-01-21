from django.db import models

class SchoolInfo(models.Model):
    name = models.CharField(max_length=1000,verbose_name="Полное название школы")
    short_name = models.CharField(max_length=255, verbose_name="Краткое название школы")
    number = models.CharField(max_length=255,verbose_name="Номер школы")
    mos_ru_auth = models.BooleanField(default=True, verbose_name="Использовать авторизацию через МЭШ")
    token = models.CharField(max_length=1000, verbose_name="Токен школы")