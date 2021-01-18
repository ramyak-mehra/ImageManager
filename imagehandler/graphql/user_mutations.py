from .schema import UserNode
import graphene
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from graphql_relay.node.node import from_global_id
from graphql_jwt.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate


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
    """ using django's inbuilt validation for validating 
        email,password and checking for unique usernames
    """
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


class ChangeUserPassword(graphene.relay.ClientIDMutation):

    success = graphene.Boolean()

    class Input:
        username = graphene.String(
            required=True, description="User's username")
        old_password = graphene.String(
            required=True, description="User's old password")
        new_password = graphene.String(
            required=True, description="User's new password")

    @classmethod
    @login_required
    def mutate_and_get_payload(self, root, info, **input):
        username = input.get('username')
        old_password = input.get('old_password')
        new_password = input.get('new_password')
        user = authenticate(username=username, password=old_password)
        if user is not None:
            user.set_password(new_password)
        else:
            raise Exception("Please check the credentials")
        return ChangeUserPassword(success=True)


class DeleteUser(graphene.relay.ClientIDMutation):
    success = graphene.Boolean

    class Input:
        username = graphene.String(
            required=True, description="User's username")
        password = graphene.String(
            required=True, description="User's password")

    @classmethod
    @login_required
    def mutate_and_get_payload(self, root, info, **input):
        username = input.get('username')
        password = input.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            user.delete()
        else:
            raise Exception("Please check the credentials")
        return ChangeUserPassword(success=True)


class UpdateUserDetails(graphene.relay.ClientIDMutation):
    """Create user mutation """
    user = graphene.Field(UserNode)

    class Input:
        image_queries = "Details to Create a new User"
        username = graphene.String(
            required=True, description="Username for the user")
        new_first_name = graphene.String(
            required=False, description="First Name of the user")
        new_last_name = graphene.String(
            required=False, description="Last Name of the user")
        new_email = graphene.String(
            required=False, description="Email address of the user")
        new_username = graphene.String(
            required=False, description="New username for the user.")
    """ using django's inbuilt validation for validating 
        email,password and checking for unique usernames
    """
    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        username = input.get('username')
        new_email = input.get('new_email', None)
        new_first_name = input.get('first_name', None)
        new_last_name = input.get('last_name', None)
        new_username = input.get('new_username', None)
        user = User.objects.get(username=username)
        if user is None:
            raise Exception("User Not Found")
        if new_email:
            try:
                validate_email(new_email)
                user.email = new_email

            except:
                raise Exception("Please provide a valid email address")
        if new_username:
            if User.objects.filter(username=new_username).exists():
                raise Exception("Please use a different username")
            else:
                user.username = new_username
        if new_first_name:
            user.first_name = new_first_name
        if new_last_name:
            user.last_name = new_last_name
        user.save()
        return UpdateUserDetails(user=user)
