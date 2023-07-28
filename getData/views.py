import os
from django.shortcuts import render
from .models import Earthquake, File
import uuid
from getData.tasks import write_to_db
from django.core.files.storage import FileSystemStorage
from django.conf import settings


def file_list(request):
    earthquake_objects = Earthquake.objects.select_related('file_UUID').values(
    'UUID', 'file_UUID__file_name', 'eq_datetime', 'longitude', 'latitude', 'depth', 'magnitude')
    if request.method == 'POST':
        name = request.POST.get('name', '')
        file_paths = request.FILES.getlist("folder")
        # Rastgele isimli bir klasör oluşturma
        random_folder_name = str(uuid.uuid4())[:8]  # 8 karakterlik rastgele bir isim oluşturuyoruz
        folder_path = os.path.join(settings.MEDIA_ROOT, random_folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Dosyaları oluşturulan klasöre kaydetme
        fs = FileSystemStorage(location=folder_path)
        for file in file_paths:
            fs.save(file.name, file)

        write_to_db.delay(folder_path,name)

        # Dosya listesini veritabanından çekme
        file_objects = File.objects.all()
        
        return render(request, 'file_list.html', { 'file_objects': file_objects, 'earthquake_objects': earthquake_objects})
    return render(request, 'file_list.html', {  'earthquake_objects': earthquake_objects})


