from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ImageHandler
from PIL import Image

"""Helper Signal to save a low resolution copy image"""

# @receiver(post_save , sender=ImageHandler)
# def make_low_res_image(sender  , instace:ImageHandler, created:bool , **kwargs):
#     if created:
#         image =  Image.open(instace.original_image.path)
#         image.save(instace.low_res_image.path , quality=50 , optimize=True)
#         instace.save()
