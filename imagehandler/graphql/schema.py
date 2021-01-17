import graphene
import django_filters
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType, DjangoConnectionField
from imagehandler.models import Tag, ImageHandler
from graphene_django.filter import DjangoFilterConnectionField
from django.contrib.auth.models import User
from django.db import models

""" ImageNode extending DjangoObjecType
    It will map ImageHandler model's  fields to ImageNode.
    This is configured in the ImageNode's Meta class
    Same thing is done for tag and user nodes
"""


class ImageNode(DjangoObjectType):
    class Meta:
        description = "A single Image Node"
        model = ImageHandler
        fields = "__all__"
        interfaces = (relay.Node, )
    """ We override how original_image field is resolved. 
        Here we return the aws url for that image.
    """
    def resolve_original_image(root, info, **kwargs):
        return root.original_image.url


""" Created A filter class to filter images 
    as per clients requirements.
"""


class ImageFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains')

    class Meta:
        model = ImageHandler
        exclude = ['original_image']
        filter_overrides = {
            models.ImageField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains'
                }
            }
        }
    order_by = django_filters.OrderingFilter(
        fields=(
            ('title', 'created_at'),
        )
    )


class TagNode(DjangoObjectType):
    class Meta:
        description = "A single Tag Node"
        model = Tag
        fields = ['tag']
        interfaces = (relay.Node, )


class UserNode(DjangoObjectType):
    class Meta:
        description = "A single User Node"
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        interfaces = (relay.Node, )
