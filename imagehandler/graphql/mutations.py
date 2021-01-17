from imagehandler.models import ImageHandler, Tag
from .schema import ImageNode, TagNode, UserNode
import graphene
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
import re
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload
from graphql_relay.node.node import from_global_id
from graphql_jwt.decorators import login_required
from django.core.exceptions import PermissionDenied,  ObjectDoesNotExist


class CreateUser(graphene.relay.ClientIDMutation):
    """Create user mutation """
    user = graphene.Field(UserNode)

    class Input:
        image_queries = "Details to Create a new User"
        username = graphene.String(
            required=True, description="Username for the user")
        password = graphene.String(
            required=True, description="A secure password")
        first_name = graphene.String(
            required=False, description="First Name of the user")
        last_name = graphene.String(
            required=False, description="Last Name of the user")
        email = graphene.String(
            required=True, description="Email address of the user")

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        username = input.get('username')
        password = input.get('password')
        email = input.get('email')
        first_name = input.get('first_name', None)
        last_name = input.get('last_name', None)
        try:
            validate_email(email)
        except:
            raise Exception("Please check your email address")
        try:
            validate_password(password)
        except:
            raise Exception("Please use a more secured password")
        if User.objects.filter(username=username).exists():
            raise Exception("Please use a different username")
        user = User.objects.create_user(username, email, password)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()
        return CreateUser(user=user)


class UploadSingleImage(graphene.relay.ClientIDMutation):
    image = graphene.Field(ImageNode)

    class Input:
        image = Upload(required=True)
        tags = graphene.List(graphene.String, description="List of tags")
        title = graphene.String(required=False,
                                description="Title for the image. By Default image name will be used.")

    @ classmethod
    @ login_required
    def mutate_and_get_payload(cls, root, info, image, **input):
        tags = input.get('tags')
        title = input.get('title', None)
        user = info.context.user
        image_handler = ImageHandler.objects.create(
            user=user, original_image=image)
        if title:
            image_handler.title = title
        else:
            image_handler.title = re.sub(
                '(original/)', '', image_handler.original_image.name)
        if tags is not None:
            for tag in tags:
                tag, created = Tag.objects.get_or_create(
                    tag=tag, slug=tag.lower())
                image_handler.tags.add(tag.pk)
        image_handler.save()
        return UploadSingleImage(image=image_handler)


class UpdateSingleImage(graphene.relay.ClientIDMutation):
    image = graphene.Field(ImageNode)

    class Input:
        id = graphene.String(required=True, description="ID of the image")
        image = Upload()
        tags = graphene.List(graphene.String, description="List of tags")

    @ classmethod
    @ login_required
    def mutate_and_get_payload(cls, root, info, image=None, **input):
        id = input.get('id')
        tags = input.get('tags', None)
        user = info.context.user
        image_id = from_global_id(id)[1]
        try:
            image_handler = ImageHandler.objects.get(pk=image_id)
        except:
            raise ObjectDoesNotExist
        if (image_handler.user != user):
            raise PermissionDenied
        if tags:
            for tag in tags:
                tag, created = Tag.objects.get_or_create(
                    tag=tag, slug=tag.lower())
                image_handler.tags.add(tag.pk)
        if image:
            image_handler.original_image = image
        image_handler.save()
        return UpdateSingleImage(image=image_handler)


class DeleteImage(graphene.relay.ClientIDMutation):
    success = graphene.Boolean()

    class Input:
        id = graphene.String(required=True, description="ID of the image")

    @ classmethod
    @ login_required
    def mutate_and_get_payload(cls, root, info, id, **input):
        image_id = from_global_id(id)[1]
        user = info.context.user
        print(image_id)
        try:
            image_handler = ImageHandler.objects.get(pk=image_id)
            print(image_handler)
        except:
            raise Exception("Image Not Found. Please check image Id")
        if (image_handler.user != user):
            raise PermissionDenied
        image_handler.delete()
        return DeleteImage(success=True)


class Mutation(graphene.AbstractType):
    upload_single_image = UploadSingleImage.Field()
    update_single_image = UpdateSingleImage.Field()
    delete_image = DeleteImage.Field()
    create_user = CreateUser.Field()
