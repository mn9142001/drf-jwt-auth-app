from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from user.models import User
from ..serializers import PromoteUserPermissionSerializer
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from ..filters import UserMailFilter
from ..permissions import IsSuperuser


class PromoteUserPermissionView(ListModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = PromoteUserPermissionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserMailFilter
    permission_classes = (IsSuperuser,)
    filterset_fields = ['email']



