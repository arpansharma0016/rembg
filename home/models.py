from django.db import models

import os
def image_name(instance, filename):
    folder = os.path.join('media/', str(instance.pk))
    return os.path.join(folder, filename)

class Images(models.Model):
    create = models.BooleanField(default=False)
    input_image = models.ImageField(blank=True, upload_to=image_name)
    resized_input_image = models.ImageField(blank=True, upload_to=image_name)
    output_image = models.ImageField(blank=True,upload_to=image_name)
    resized_output_image = models.ImageField(blank=True,upload_to=image_name)
    created = models.DateTimeField(auto_now_add=True)