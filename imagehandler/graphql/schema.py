import graphene
import django_filters
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType, DjangoConnectionField
from imagehandler.models import Tag, ImageHandler
from graphene_django.filter import DjangoFilterConnectionField
from django.db import models


class ImageNode(DjangoObjectType):
    class Meta:
        description = "Details about a single image"
        model = ImageHandler
        interfaces = (relay.Node, )
        fields = "__all__"

    def resolve_original_image(root, info, **kwargs):
        return root.original_image.url


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
        description = "Detail about a single tag"
        model = Tag
        fields = ['tag']
        interfaces = (relay.Node, )


class Query(ObjectType):
    all_images = DjangoFilterConnectionField(
        ImageNode, filterset_class=ImageFilter, description="Get top results of images")
    all_tags = DjangoConnectionField(
        TagNode, description="Get the list of all tags")
    image = relay.Node.Field(
        ImageNode, description="Get a single image from an image id.")
    tag = relay.Node.Field(
        TagNode, description="Get a single tag from a tag id.")
    search_images = graphene.List(
        ImageNode, search_query=graphene.String(required=False), description="Get list of images based on a search query.")

    def resolve_search_images(self, info, search_query, **kwargs):
        from django.db.models import Q
        qs = ImageHandler.objects.filter(
            Q(title__icontains=search_query) | Q(user__username__icontains=search_query) | Q(tags__tag__icontains=search_query))
        return qs

    # def resolve_search_images(self, info, search_query, **kwargs):
    #     from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
    #     vector = SearchVector('title', 'user__username', 'tags__tag')
    #     query = SearchQuery(search_query)
    #     qs = ImageHandler.objects.annotate(
    #         rank=SearRank(vector, query))
