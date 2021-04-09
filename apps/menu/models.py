import os
import uuid

from django.db import models


def menu_image_file_path(instance, filename):
    """Generate file path for new menu image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/menu/', filename)


class Menu(models.Model):
    """Menu object"""

    image = models.ImageField(null=True, upload_to=menu_image_file_path)

    def __str__(self):
        return str(self.image)
