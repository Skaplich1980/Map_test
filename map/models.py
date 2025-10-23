from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

# TODO Place Место на карте
class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    short_desc = models.TextField(blank=True, verbose_name="Краткое описание")
    long_desc = CKEditor5Field(blank=True, verbose_name="Полное описание", config_name="default")
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")

    class Meta:
        # мои правила наименования, чтобы в админке видеть латинское наименование модели и русское и можно было найти, когда много
        verbose_name = 'Place (Место на карте)'
        verbose_name_plural = 'Place (Места на карте)'

    def __str__(self):
        return f"{self.title} ({self.short_desc[:30]}...) : {self.latitude},{self.longitude}"


# TODO Photo Фотографии
class Photo(models.Model):
    place = models.ForeignKey( Place, on_delete=models.CASCADE, related_name="photos", verbose_name="Место на карте")
    # image_data = models.BinaryField(verbose_name="Фотография") # храним в БД
    image = models.ImageField(upload_to="places", verbose_name="Фотография")
    description = models.TextField(blank=True, verbose_name="Описание")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    class Meta:
        verbose_name = 'Photo (Фото)'
        verbose_name_plural = 'Photo (Фото)'
        ordering = ["order"] # сортировка по приоритету вывода картинки
        # порядок отображения должен быть уникальный для фото в одном месте
        constraints = [
            models.UniqueConstraint(
                fields=["place", "order"],
                name="unique_order_per_place"
            )
        ]

    def __str__(self):
        return f"Фото {self.place.title} описание {self.description} отображать ({self.order})"