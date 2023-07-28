from celery import shared_task
import traceback
import pandas as pd
import chardet
import os
from getData.models import File, Earthquake
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


@shared_task
def write_to_db(folder_path, name):
    try:
        file_list = os.listdir(folder_path)
        dfs = []  # DataFrame'leri depolamak için boş bir liste oluşturuyoruz

        for i in file_list:
            file_full_path = os.path.join(folder_path, i)
            encoding = detect_encoding(file_full_path)  # Dosyanın karakter kodlamasını tespit ediyoruz

            if file_full_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_full_path, engine="openpyxl")
            elif file_full_path.endswith('.csv'):
                df = pd.read_csv(file_full_path, encoding=encoding)  # Tespit edilen kodlamayı kullanıyoruz
            else:
                print(f"Dosya türü desteklenmiyor: {file_full_path}")
                continue

            # DataFrame'inizdeki sütun sayısını kontrol edin
            if len(df.columns) > 5:
                # İlk iki kolonu birleştirerek 'Datetime' sütununu oluşturun
                df['Datetime'] = df.iloc[:, 0].astype(str) + ' ' + df.iloc[:, 1].astype(str)

                # İlk iki kolonu DataFrame'den kaldırın
                df.drop(columns=df.columns[:2], inplace=True)

                # Son sütunu (son indeksi olan sütunu) 0. indekse alalım
                son_sutun = df.columns[-1]
                yeni_sutunlar = [son_sutun] + [kolon for kolon in df.columns if kolon != son_sutun]
                df = df[yeni_sutunlar]

            dfs.append(df)  # Oluşturduğumuz DataFrame'i listeye ekliyoruz
            file_extension = i.split('.')[-1]

            # Check if a File object with the same name and file_type exists before creating a new one
            file_object, created = File.objects.get_or_create(
                file_name=i,
                file_type=file_extension,
                created_by=name
            )

            # DataFrame üzerinde dolaşmak yerine to_dict kullanalım
            for index, row in df.iterrows():
                # Check if an Earthquake object with the same values exists before creating a new one
                eq_datetime = row.iloc[0]
                longitude = row.iloc[1]
                latitude = row.iloc[2]
                depth = row.iloc[3]
                magnitude = row.iloc[4]

                earthquake, created = Earthquake.objects.get_or_create(
                    file_UUID=file_object,
                    eq_datetime=eq_datetime,
                    longitude=longitude,
                    latitude=latitude,
                    depth=depth,
                    magnitude=magnitude
                )

                # Check if the Earthquake object was created or already existed
                if not created:
                    print(f"Duplicate entry found for: {earthquake}")
                else:
                    print(f"New entry created: {earthquake}")

    except Exception as e:
        traceback_str = traceback.format_exc()
        print(traceback_str)
        print(e)