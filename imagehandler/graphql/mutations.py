import graphene
from .user_mutations import CreateUser, ChangeUserPassword, DeleteUser, UpdateUserDetails
from .image_mutations import UpdateSingleImage, UploadSingleImage, DeleteImage


class Mutation(graphene.AbstractType):
    upload_single_image = UploadSingleImage.Field()
    update_single_image = UpdateSingleImage.Field()
    delete_image = DeleteImage.Field()
    create_user = CreateUser.Field()
    change_user_password = ChangeUserPassword.Field()
    update_user_details = UpdateUserDetails.Field()
    delete_user = DeleteUser.Field()
