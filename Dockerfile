# Django projesinin temel görüntüsü
FROM python:3.9-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gerekli dosyaları kopyala
COPY requirements.txt ./
COPY manage.py ./

# Gerekli kütüphaneleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# Diğer dosyaları kopyala
COPY . .

# Gerekli komutu çalıştır
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
