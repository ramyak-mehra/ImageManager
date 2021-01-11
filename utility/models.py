from django.db import models

class TimestampModel(models.Model):
    ''' 
    A utility model for adding abstracting created at
    and upated at fields for various models
    created_at: date and time when the object was created
    updated_at:date and time whent the object was updated

    '''

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True