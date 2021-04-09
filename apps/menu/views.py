from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.menu import serializers
from apps.menu.models import Menu


class MenuViewSet(viewsets.ModelViewSet):
    """Manage menu in the database"""
    serializer_class = serializers.MenuImageSerializer
    queryset = Menu.objects.all()

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a menu"""
        menu = self.get_object()
        serializer = self.get_serializer(
            menu,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
