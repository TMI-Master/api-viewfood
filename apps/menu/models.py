import os
import uuid

from django.db import models


def menu_image_file_path(instance, filename):
    """Generate file path for new menu image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/menu/', filename)


def translated_image_file_path(instance, filename):
    """Generate file path for new translated image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('translateds/menu/', filename)


class Menu(models.Model):
    """Menu object"""

    image = models.ImageField(null=False, upload_to=menu_image_file_path)
    lang = models.CharField(
        max_length=10, blank=False, null=False, default="EN"
    )
    description = models.TextField(blank=True, null=True)
    original = models.TextField(blank=True, null=True)
    translated_image = models.ImageField(
        null=True, upload_to=translated_image_file_path
    )

    def __str__(self):
        return str(self.image)
