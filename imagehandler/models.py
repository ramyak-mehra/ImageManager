from django.db import models
from utility.models import TimestampModel
from django.contrib.auth.models import User


class ImageHandler(TimestampModel):
    '''
    An ImageHandler containes all the detail about an image
    user: the user which uploaded the image
    title:title for the images
    original_image: origial image uploaded by the user
    created_at: the date and time when the image was uploaded
    updated_at: the date and time when the image or its properties were updated
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    original_image = models.ImageField(upload_to='original')
    tags = models.ManyToManyField('imagehandler.Tag', related_name='tags')

    def __str__(self, *args, **kwargs):
        self.original_image.name
        return f"{self.title} {self.pk}"


class Tag(TimestampModel):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.tag
