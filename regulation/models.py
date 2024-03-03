from django.db import models
from django.utils.translation import gettext_lazy as _


class Section(models.Model):
    name = models.CharField(_("название"), max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("родительский раздел"))
    header = models.CharField(_("заголовок"), max_length=200)
    content = models.TextField(_("содержимое"))
    footer = models.CharField(_("нижний колонтитул"), max_length=200, default="", blank=True)

    class Meta:
        verbose_name = _("раздел")
        verbose_name_plural = _("разделы")

    def __str__(self):
        return self.name


class Image(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='images', verbose_name=_("раздел"))
    image = models.ImageField(upload_to='images/', verbose_name=_("изображение"))
    caption = models.CharField(_("подпись"), max_length=200, blank=True)

    class Meta:
        verbose_name = _("изображение")
        verbose_name_plural = _("изображения")

    def __str__(self):
        return f"{_('Изображение для')} {self.section.name}"


class File(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='files', verbose_name=_("раздел"))
    file = models.FileField(upload_to='files/', verbose_name=_("файл"))
    description = models.CharField(_("описание"), max_length=200, blank=True)

    class Meta:
        verbose_name = _("файл")
        verbose_name_plural = _("файлы")

    def __str__(self):
        return f"{_('Файл для')} {self.section.name}"
