from django.db import models

# Create your models here.
class FileUpload(models.Model):
    filename = models.CharField(max_length=50)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)