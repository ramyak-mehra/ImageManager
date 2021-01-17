import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from django.db import models
from imagehandler.graphql.schema import ImageNode, ImageFilter, TagNode, UserNode


class Query(ObjectType):
    all_images = DjangoFilterConnectionField(
        ImageNode, filterset_class=ImageFilter, description="Get top results of images")
    all_tags = DjangoConnectionField(
        TagNode, description="Get the list of all tags")
    all_users = DjangoConnectionField(
        UserNode, description="Get the list of all the users")
    user = relay.Node.Field(
        UserNode, description="Get a single user from global user id")
    image = relay.Node.Field(
        ImageNode, description="Get a single image from an global image id.")
    tag = relay.Node.Field(
        TagNode, description="Get a single tag from a global tag id.")
    """ query for searching among the image database
         based on a search query
    """
    search_images = graphene.List(
        ImageNode, search_query=graphene.String(required=False), description="Get list of images based on a search query.")
    """ resolver for search image query it uses
        django's optimized quering to filter out the results
    """

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
