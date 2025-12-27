from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = RichTextUploadingField(blank=True, null=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    mobile_image = models.ImageField(upload_to='projects/mobile/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    date = models.DateField()
    is_public = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextUploadingField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class NavigationItem(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default='Mon Portfolio')
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    hero_description = RichTextUploadingField(blank=True)
    pwa_icon_192 = models.ImageField(upload_to='site/pwa/', blank=True, null=True)
    pwa_icon_512 = models.ImageField(upload_to='site/pwa/', blank=True, null=True)
    about_title = models.CharField(max_length=200, blank=True, default="À Propos de Nous")
    about_description = RichTextUploadingField(blank=True)
    about_image = models.ImageField(upload_to='site/about/', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SiteSettings, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
