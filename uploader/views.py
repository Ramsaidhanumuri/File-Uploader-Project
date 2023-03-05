import os
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
import pandas as pd
from .models import FileUpload
from IPython.display import HTML

# Create your views here.
def index(request):
    upload_file_details = None
    if request.user.is_authenticated and request.user.username=='admin':
        upload_file_details = FileUpload.objects.all()

    if request.method == 'POST':
        fileName = request.POST.get('fileName')
        file = request.FILES['file']
        upload_file = FileUpload(filename=fileName, file=file)
        upload_file.save()

        context = {'message':'Success', 'filename':fileName, 'upload_file_details':upload_file_details}

        return render(request, 'index.html', context)

    return render(request, 'index.html', {'upload_file_details':upload_file_details})


def download_file(request, id):
    uploaded_file = FileUpload.objects.get(id=id)
    file_path = uploaded_file.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def open_file(request, id):
    uploaded_file = FileUpload.objects.get(id=id)
    file_path = uploaded_file.file.path
    if file_path.endswith('.xlsx'):
        df = pd.ExcelFile(file_path) 
        sheet_name = df.sheet_names
        print(sheet_name)
        df = pd.read_excel(df, sheet_name[0])
        df = df.style.hide_index()

    else:
        df = pd.read_csv(file_path)
        
    df = df.style.hide_index()
    data = df.to_html()

    return HttpResponse(data)