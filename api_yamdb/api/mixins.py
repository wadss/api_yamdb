from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)

from .permissions import (
    IsAdminOrReadOnly,
)


class CreateListDestroyMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Миксин для viewset'ов Category и Genres."""

    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
