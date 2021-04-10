from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

import tempfile
import os

from PIL import Image

from apps.menu.models import Menu

def image_upload_url():
    """Return URL for menu image upload"""
    return reverse('menu:menu-upload')

def sample_menu(**params):
    """Create and return a sample menu"""
    defaults = {}
    defaults.update(params)

    return Menu.objects.create(**defaults)

class MenuImageUploadTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.menu = None

    def tearDown(self):
        if self.menu != None:
            self.menu.image.delete()

    def test_upload_image_to_menu(self):
        """Test uploading an image to menu"""
        url = image_upload_url()
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(url, {'image': ntf}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.menu = Menu.objects.get(pk=res.data['id'])
        self.menu.refresh_from_db()
        self.assertTrue(os.path.exists(self.menu.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url()
        res = self.client.post(url, {'image': 'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_upload_image_bad_image(self):
        """Test uploading an invalid image"""
        url = image_upload_url()
        res = self.client.post(url, {'image': '' }, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
