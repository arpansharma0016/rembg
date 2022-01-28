from django.shortcuts import render
from .models import Images
from django.conf import settings as django_settings
import os
from django.core.files import File
import shutil
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rembg.bg import remove
import numpy as np
import io
from PIL import Image, ImageFile

from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def index(request):
    return render(request, "index.html")

@csrf_exempt
def upload(request):
    if request.method == "POST":
        inputt = request.FILES.get('image')
        exts = ['jpg', 'JPG', 'png', 'PNG', 'jpeg', 'JPEG', 'jfif', 'JFIF']
        if inputt:
            if not inputt.name.split('.')[-1] in exts:
                return JsonResponse({'status':'fail', 'message':'Invalid file format.'})
        else:
            return JsonResponse({'status':'fail', 'message':'No file found.'})

        try:
            image = Images.objects.create(create=True)
            image.input_image = inputt
            image.save()

            opened = Image.open(image.input_image)
            rat = opened.height/opened.width
            wid = 0
            hei = 0
            if (opened.width / 2) > 400:
                wid = 400
            else:
                wid = opened.width / 2

            hei = rat * wid

            resized = opened.resize((int(wid), int(hei)))

            tempfile_io = BytesIO()
            resized.save(tempfile_io, format='PNG')
            image_file = InMemoryUploadedFile(tempfile_io, None, 'r-input.png','image/png',tempfile_io.tell, None)
            image.resized_input_image.save("r-input.png", image_file)

        except Exception as e:
            print(e)
            return JsonResponse({'status':'fail', 'message':'Something went wrong while uploading your file. Try again'})

        return JsonResponse({'status':'success', 'id':image.id})


def detach(request, id):
    try:
        image = Images.objects.get(id=id)
    except:
        image = None

    if image:
        try:
            ImageFile.LOAD_TRUNCATED_IMAGES = True
            
            f = np.fromfile(image.resized_input_image)
            result = remove(f)
            img = Image.open(io.BytesIO(result)).convert("RGBA")

            tempfile_io = BytesIO()
            img.save(tempfile_io, format='PNG')
            image_file = InMemoryUploadedFile(tempfile_io, None, 'r-output.png', 'image/png', tempfile_io.tell, None)
            image.resized_output_image.save("r-output.png", image_file)
            
        except:
            return JsonResponse({'status':'fail', 'message':'Something went wrong while removing background from your image. Try again'})

        image = f"https://mediafiles-arpan.s3.ap-south-1.amazonaws.com/media/{image.id}/r-output.png"
        return JsonResponse({'status':'success', 'image':image})

    else:
        return JsonResponse({'status':'fail', 'message':'This file does not exists'})


def detachhd(request, id):
    try:
        image = Images.objects.get(id=id)
    except:
        image = None

    if image:
        try:
            ImageFile.LOAD_TRUNCATED_IMAGES = True
            
            f = np.fromfile(image.input_image)
            result = remove(f)
            img = Image.open(io.BytesIO(result)).convert("RGBA")

            tempfile_io = BytesIO()
            img.save(tempfile_io, format='PNG')
            image_file = InMemoryUploadedFile(tempfile_io, None, 'output.png', 'image/png', tempfile_io.tell, None)
            image.output_image.save("output.png", image_file)
            
        except Exception as e:
            print(e)
            imag = f"https://mediafiles-arpan.s3.ap-south-1.amazonaws.com/media/{image.id}/r-output.png"
            return JsonResponse({'status':'fail', 'message':'Something went wrong while removing background from your image. Try again', 'image':imag})

        imag = f"https://mediafiles-arpan.s3.ap-south-1.amazonaws.com/media/{image.id}/r-output.png"
        imagehd = f"https://mediafiles-arpan.s3.ap-south-1.amazonaws.com/media/{image.id}/output.png"
        return JsonResponse({'status':'success', 'image':imag, 'imagehd':imagehd})

    else:
        return JsonResponse({'status':'fail', 'message':'This file does not exists'})