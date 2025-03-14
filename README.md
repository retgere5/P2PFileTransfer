# P2P Dosya Transferi

Python ve WebRTC ile geliştirilmiş, tarayıcı tabanlı gerçek zamanlı dosya paylaşım uygulaması.

## Özellikler

- 🔄 WebRTC üzerinden P2P dosya transferi
- 💬 Gerçek zamanlı sohbet özelliği
- 🔒 Uçtan uca şifrelenmiş bağlantı
- 📁 Sürükle-bırak dosya yükleme
- 🚀 Yüksek hızlı veri aktarımı (256KB chunk boyutu)
- 👥 Kullanıcı yönetimi ve oda sistemi
- 🌐 Tarayıcı tabanlı, kurulum gerektirmeyen arayüz
- 📱 Responsive tasarım ile mobil uyumluluk
- 🔄 Arka planda dosya transferi (Web Workers)
- 📊 Dosya transfer ilerleme göstergesi
- 🖼️ Resim, video ve PDF önizleme
- 🌍 Ngrok ile internet üzerinden erişim imkanı

## Proje Yapısı

```
p2p_file_transfer/
├── app/                    # Ana uygulama klasörü
│   ├── static/             # Statik dosyalar
│   │   ├── css/            # CSS dosyaları
│   │   ├── js/             # JavaScript dosyaları
│   │   └── img/            # Resimler ve favicon
│   ├── templates/          # HTML şablonları
│   │   ├── base.html       # Ana şablon
│   │   ├── index.html      # Ana sayfa
│   │   ├── about.html      # Hakkında sayfası
│   │   ├── errors/         # Hata sayfaları
│   │   └── p2p/            # P2P sayfaları
│   │       ├── create_room.html  # Oda oluşturma
│   │       └── room.html         # Oda sayfası
│   ├── __init__.py         # Uygulama başlatıcı
│   ├── routes.py           # URL yönlendirmeleri
│   ├── socket_events.py    # Socket.IO olayları
│   └── errors.py           # Hata yönetimi
├── config.py               # Yapılandırma dosyası
├── run.py                  # Uygulamayı çalıştırma scripti
└── requirements.txt        # Bağımlılıklar
```

## Gereksinimler

- Python 3.6+
- Gerekli kütüphaneler:
  - Flask (web sunucusu)
  - Flask-SocketIO (gerçek zamanlı iletişim)
  - eventlet (asenkron işlemler)
  - python-dotenv (ortam değişkenleri)
- Ngrok (dış ağa paylaşım için, opsiyonel)

## Kurulum

1. Depoyu klonlayın
```bash
git clone https://github.com/kullanici/P2PFileTransfer.git
cd P2PFileTransfer
```

2. Sanal ortam oluşturun (opsiyonel)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Bağımlılıkları yükleyin
```bash
pip install -r requirements.txt
```

4. Uygulamayı çalıştırın
```bash
python run.py
```

Uygulama varsayılan olarak `http://localhost:5000` adresinde çalışacaktır.

## Ngrok ile Dış Ağa Paylaşma

Ngrok, yerel sunucunuzu internet üzerinden erişilebilir hale getiren bir tünel hizmetidir. Bu özellik sayesinde, uygulamanızı yerel ağınızın dışındaki kullanıcılarla paylaşabilirsiniz.

### Ngrok Kurulumu

1. [Ngrok'un web sitesinden](https://ngrok.com/download) işletim sisteminize uygun sürümü indirin

2. İndirdiğiniz dosyayı açın ve kurulum talimatlarını izleyin

3. Ngrok hesabı oluşturun ve auth token alın
   - [Ngrok'un web sitesine](https://ngrok.com/) gidin ve ücretsiz bir hesap oluşturun
   - Hesabınıza giriş yaptıktan sonra, auth token'ınızı [dashboard](https://dashboard.ngrok.com/get-started/your-authtoken) sayfasından alın

4. Auth token'ı yapılandırın
```bash
ngrok authtoken YOUR_AUTH_TOKEN
```

### Ngrok ile Uygulamayı Paylaşma

1. Önce uygulamayı normal şekilde başlatın
```bash
python run.py
```

2. Yeni bir terminal penceresi açın ve ngrok komutunu çalıştırın
```bash
# Varsayılan port 5000 için
ngrok http 5000
```

3. Ngrok terminal çıktısında görünen URL'yi not edin (örn. `https://a1b2c3d4.ngrok.io`)

4. Bu URL'yi diğer kullanıcılarla paylaşın. Artık internet üzerinden uygulamanıza erişebilirler.

### Ngrok Avantajları

- 🌐 İnternet üzerinden erişim
- 🔄 Otomatik SSL sertifikası
- 📊 Trafik izleme ve analiz
- 🛡️ DDoS koruması

### Ngrok Sınırlamaları

- Ücretsiz hesaplar için sınırlı bağlantı süresi (2 saat)
- Her yeniden başlatmada değişen URL (ücretli hesaplar için sabit URL)
- Ücretsiz hesaplar için sınırlı bant genişliği

## Kullanım

### Oda Oluşturma

1. Ana sayfada "Oda Oluştur" butonuna tıklayın
2. Oluşturulan oda ID'sini kopyalayın ve karşı tarafa gönderin
3. Dosya transferi ve sohbet için hazırsınız

### Odaya Katılma

1. Ana sayfada "Odaya Katıl" butonuna tıklayın
2. Size verilen oda ID'sini girin
3. Bağlantı kurulduktan sonra dosya transferi ve sohbet yapabilirsiniz

### Dosya Transferi

- Dosyaları sürükle-bırak yaparak veya "Dosya Seç" butonuyla yükleyebilirsiniz
- Birden fazla dosya seçildiğinde, dosyalar sırayla transfer edilir
- Transfer sırasında ilerleme çubuğu ile durum takip edilebilir
- Alınan dosyalar "Alınan Dosyalar" bölümünde görüntülenir ve indirilebilir

### Sohbet

- Sağ paneldeki sohbet bölümünden mesaj gönderebilirsiniz
- Kullanıcı adınızı değiştirmek için kullanıcılar panelindeki düzenleme simgesine tıklayın

## Teknik Detaylar

### WebRTC Bağlantısı

Uygulama, tarayıcılar arasında doğrudan bağlantı kurmak için WebRTC teknolojisini kullanır. Bağlantı kurulumu için sinyal sunucusu olarak Flask-SocketIO kullanılır, ancak veri aktarımı tamamen P2P olarak gerçekleşir.

### Dosya Transfer Optimizasyonu

- Chunk boyutu: 256KB (yüksek hız için optimize edilmiş)
- Web Workers kullanılarak arka planda transfer
- Sayfa görünürlük API'si ile sekme arka plandayken bile transfer devam eder
- Dosya kuyruk sistemi ile çoklu dosya transferi

### Güvenlik

Tüm veri transferi WebRTC'nin sağladığı uçtan uca şifreleme ile korunur. Hiçbir dosya sunucu üzerinden geçmez, doğrudan kullanıcılar arasında transfer edilir.

### Ngrok Tünelleme

Ngrok, uygulamanızı internet üzerinden erişilebilir hale getirmek için güvenli bir tünel oluşturur. Bu, NAT ve güvenlik duvarı sınırlamalarını aşmanıza olanak tanır. WebRTC sinyal sunucusu olarak çalışan Flask uygulamanız, ngrok tüneli üzerinden erişilebilir olur, böylece internet üzerindeki kullanıcılar P2P bağlantı kurabilir.

## Tarayıcı Desteği

- Google Chrome (önerilen)
- Mozilla Firefox
- Microsoft Edge
- Safari (kısmi destek)

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## İletişim

Sorularınız veya önerileriniz için GitHub üzerinden issue açabilir veya pull request gönderebilirsiniz. 