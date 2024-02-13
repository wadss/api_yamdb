from rest_framework import viewsets

from reviews.models import Title

from api.permissions import IsAdminOrReadOnlyPermission

from api.serializers import TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)


class GenreViewSet:
    pass


class CategoryViewSet:
    pass
