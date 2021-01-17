from .schema import UserNode
import graphene
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from graphql_relay.node.node import from_global_id
from graphql_jwt.decorators import login_required
from django.core.exceptions import PermissionDenied


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
