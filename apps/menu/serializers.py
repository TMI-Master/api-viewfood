from rest_framework import serializers

from apps.menu.models import Menu


class MenuImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to menu"""

    class Meta:
        model = Menu
        fields = ('id', 'image')
        read_only_fields = ('id',)
