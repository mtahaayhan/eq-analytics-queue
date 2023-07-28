# Proje Adı

Bu proje, Django, Celery, PostgreSQL ve RabbitMQ teknolojilerini Docker kullanarak çalıştırmak için tasarlanmıştır.

## Gereksinimler

Projenin yerel bir ortamda çalıştırılabilmesi için aşağıdaki araçların yüklü olması gereklidir:

- Docker
- Docker Compose

## Kurulum

1. Bu depoyu klonlayın:

```bash
git clone <repository_url>
cd <repository_name>

```
- Projeyi bilgisayarınıza indirdikten sonra env_example dosyasını .env olarak adını değiştirin

```bash
# Bu komutu projenin ana dizininde terminalde çalıştırın
docker-compose -f docker-compose.yml up -d --build
```
- Bu işlemlerden sonra proje http://localhost:8000/ dizininde ayakta olacaktır.

- Projede bilgisayarınızdan excel dosyalarınızın olduğu bir klasör seçin ve oluşturucu kişi olarak bir ad girin.
- Daha sonra gönder butonuna tıklayın. Tıkladıktan sonra işlemleriniz celery - rabbitmq ile arka planda kuyruğa alınır ve databaseye yazılma işlemleri gerçekleşir.
- Eğer herhangi bir duplicate durumu olursa bunun uyarısını celery container loglarından takip edebilirsiniz.



