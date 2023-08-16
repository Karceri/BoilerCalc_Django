import warnings
from django.shortcuts import render
from django.http import HttpResponse
from .classes import visio_recognition
warnings.filterwarnings('error')


# Create your views here.

def main(request):
    if request.method == 'POST':
        visio_recognition.read_visio()
        visio_recognition.copy_visio()
        return HttpResponse('Ура')
    return render(request, 'main.html')


# def main(request):
#     if request.method == "POST":
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid(): # Проверяем, является ли форма валидной
#             initial_obj = form.save(commit=False)
#             initial_obj.save()
#             file_path = initial_obj.document
#             #result = visio_recognition.read_visio(file_path)
#             #file = form.cleaned_data['file']
#             #file_path = handle_uploaded_file(file)
#             return render(request, 'main.html', {'file_path': file_path})
#     else:
#         form = FileUploadForm()
#     return render(request, 'main.html', {'form': form})

# def handle_uploaded_file(file):
#     file_path = 'path/to/save/file/' + file.name
#     with open(file_path, 'wb+') as destination:
#         for chunk in file.chunks():
#             destination.write(chunk)
#     return file_path
