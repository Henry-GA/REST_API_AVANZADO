from rest_framework import viewsets,mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag

from recipe import serializers
# Create your views here.

class TagViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    """ Handle the tags on the db """
    authentication_classes = (TokenAuthentication,)
    permissions_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')