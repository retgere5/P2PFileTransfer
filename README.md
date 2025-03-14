# 🔄 P2P Dosya Transferi

<div align="center">

![P2P File Transfer](app/static/img/favicon.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-red.svg)](https://flask.palletsprojects.com/)
[![WebRTC](https://img.shields.io/badge/WebRTC-Enabled-green.svg)](https://webrtc.org/)

**Python ve WebRTC ile geliştirilmiş, tarayıcı tabanlı gerçek zamanlı dosya paylaşım uygulaması.**

[Özellikler](#özellikler) • 
[Kurulum](#kurulum) • 
[Kullanım](#kullanım) • 
[Teknik Detaylar](#teknik-detaylar) • 
[Ngrok ile Paylaşım](#ngrok-ile-dış-ağa-paylaşma)

</div>

## ✨ Özellikler

<table>
  <tr>
    <td>
      <ul>
        <li>🔄 WebRTC üzerinden P2P dosya transferi</li>
        <li>💬 Gerçek zamanlı sohbet özelliği</li>
        <li>🔒 Uçtan uca şifrelenmiş bağlantı</li>
        <li>📁 Sürükle-bırak dosya yükleme</li>
        <li>🚀 Yüksek hızlı veri aktarımı (256KB chunk boyutu)</li>
        <li>👥 Kullanıcı yönetimi ve oda sistemi</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>🌐 Tarayıcı tabanlı, kurulum gerektirmeyen arayüz</li>
        <li>📱 Responsive tasarım ile mobil uyumluluk</li>
        <li>🔄 Arka planda dosya transferi (Web Workers)</li>
        <li>📊 Dosya transfer ilerleme göstergesi</li>
        <li>🖼️ Resim, video ve PDF önizleme</li>
        <li>🌍 Ngrok ile internet üzerinden erişim imkanı</li>
      </ul>
    </td>
  </tr>
</table>

## 📂 Proje Yapısı

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

## 🛠️ Gereksinimler

<table>
  <tr>
    <th>Gereksinim</th>
    <th>Açıklama</th>
  </tr>
  <tr>
    <td>Python 3.6+</td>
    <td>Uygulama çalışma ortamı</td>
  </tr>
  <tr>
    <td>Flask</td>
    <td>Web sunucusu framework'ü</td>
  </tr>
  <tr>
    <td>Flask-SocketIO</td>
    <td>Gerçek zamanlı iletişim için</td>
  </tr>
  <tr>
    <td>eventlet</td>
    <td>Asenkron işlemler için</td>
  </tr>
  <tr>
    <td>python-dotenv</td>
    <td>Ortam değişkenleri yönetimi</td>
  </tr>
  <tr>
    <td>Ngrok (opsiyonel)</td>
    <td>Dış ağa paylaşım için</td>
  </tr>
</table>

## 🚀 Kurulum

<details open>
<summary><b>1. Depoyu klonlayın</b></summary>

```bash
git clone https://github.com/kullanici/P2PFileTransfer.git
cd P2PFileTransfer
```
</details>

<details open>
<summary><b>2. Sanal ortam oluşturun (opsiyonel)</b></summary>

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```
</details>

<details open>
<summary><b>3. Bağımlılıkları yükleyin</b></summary>

```bash
pip install -r requirements.txt
```
</details>

<details open>
<summary><b>4. Uygulamayı çalıştırın</b></summary>

```bash
python run.py
```

Uygulama varsayılan olarak `http://localhost:5000` adresinde çalışacaktır.
</details>

## 🌐 Ngrok ile Dış Ağa Paylaşma

<div align="center">
  
  ![Ngrok](https://ngrok.com/static/img/ngrok-black.svg)
  
</div>

Ngrok, yerel sunucunuzu internet üzerinden erişilebilir hale getiren bir tünel hizmetidir. Bu özellik sayesinde, uygulamanızı yerel ağınızın dışındaki kullanıcılarla paylaşabilirsiniz.

### 📥 Ngrok Kurulumu

<details>
<summary><b>1. Ngrok'u indirin ve kurun</b></summary>

[Ngrok'un web sitesinden](https://ngrok.com/download) işletim sisteminize uygun sürümü indirin ve kurulum talimatlarını izleyin.
</details>

<details>
<summary><b>2. Ngrok hesabı oluşturun ve auth token alın</b></summary>

- [Ngrok'un web sitesine](https://ngrok.com/) gidin ve ücretsiz bir hesap oluşturun
- Hesabınıza giriş yaptıktan sonra, auth token'ınızı [dashboard](https://dashboard.ngrok.com/get-started/your-authtoken) sayfasından alın
</details>

<details>
<summary><b>3. Auth token'ı yapılandırın</b></summary>

```bash
ngrok authtoken YOUR_AUTH_TOKEN
```
</details>

### 🔗 Ngrok ile Uygulamayı Paylaşma

<details open>
<summary><b>1. Uygulamayı başlatın</b></summary>

```bash
python run.py
```
</details>

<details open>
<summary><b>2. Yeni bir terminal penceresi açın ve ngrok komutunu çalıştırın</b></summary>

```bash
# Varsayılan port 5000 için
ngrok http 5000
```
</details>

<details open>
<summary><b>3. URL'yi paylaşın</b></summary>

Ngrok terminal çıktısında görünen URL'yi not edin (örn. `https://a1b2c3d4.ngrok.io`) ve bu URL'yi diğer kullanıcılarla paylaşın.
</details>

### ⚡ Ngrok Avantajları ve Sınırlamaları

<table>
  <tr>
    <th>Avantajlar</th>
    <th>Sınırlamalar</th>
  </tr>
  <tr>
    <td>
      <ul>
        <li>🌐 İnternet üzerinden erişim</li>
        <li>🔄 Otomatik SSL sertifikası</li>
        <li>📊 Trafik izleme ve analiz</li>
        <li>🛡️ DDoS koruması</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>⏱️ Ücretsiz hesaplar için sınırlı bağlantı süresi (2 saat)</li>
        <li>🔄 Her yeniden başlatmada değişen URL</li>
        <li>📊 Ücretsiz hesaplar için sınırlı bant genişliği</li>
      </ul>
    </td>
  </tr>
</table>

## 📝 Kullanım

### 🏠 Oda Oluşturma ve Katılma

<table>
  <tr>
    <th width="50%">Oda Oluşturma</th>
    <th width="50%">Odaya Katılma</th>
  </tr>
  <tr>
    <td>
      <ol>
        <li>Ana sayfada "Oda Oluştur" butonuna tıklayın</li>
        <li>Oluşturulan oda ID'sini kopyalayın ve karşı tarafa gönderin</li>
        <li>Dosya transferi ve sohbet için hazırsınız</li>
      </ol>
    </td>
    <td>
      <ol>
        <li>Ana sayfada "Odaya Katıl" butonuna tıklayın</li>
        <li>Size verilen oda ID'sini girin</li>
        <li>Bağlantı kurulduktan sonra dosya transferi ve sohbet yapabilirsiniz</li>
      </ol>
    </td>
  </tr>
</table>

### 📤 Dosya Transferi

- Dosyaları sürükle-bırak yaparak veya "Dosya Seç" butonuyla yükleyebilirsiniz
- Birden fazla dosya seçildiğinde, dosyalar sırayla transfer edilir
- Transfer sırasında ilerleme çubuğu ile durum takip edilebilir
- Alınan dosyalar "Alınan Dosyalar" bölümünde görüntülenir ve indirilebilir

### 💬 Sohbet

- Sağ paneldeki sohbet bölümünden mesaj gönderebilirsiniz
- Kullanıcı adınızı değiştirmek için kullanıcılar panelindeki düzenleme simgesine tıklayın

## 🔧 Teknik Detaylar

<details open>
<summary><b>WebRTC Bağlantısı</b></summary>

Uygulama, tarayıcılar arasında doğrudan bağlantı kurmak için WebRTC teknolojisini kullanır. Bağlantı kurulumu için sinyal sunucusu olarak Flask-SocketIO kullanılır, ancak veri aktarımı tamamen P2P olarak gerçekleşir.
</details>

<details open>
<summary><b>Dosya Transfer Optimizasyonu</b></summary>

- **Chunk boyutu:** 256KB (yüksek hız için optimize edilmiş)
- **Web Workers** kullanılarak arka planda transfer
- **Sayfa görünürlük API'si** ile sekme arka plandayken bile transfer devam eder
- **Dosya kuyruk sistemi** ile çoklu dosya transferi
</details>

<details open>
<summary><b>Güvenlik</b></summary>

Tüm veri transferi WebRTC'nin sağladığı uçtan uca şifreleme ile korunur. Hiçbir dosya sunucu üzerinden geçmez, doğrudan kullanıcılar arasında transfer edilir.
</details>

<details open>
<summary><b>Ngrok Tünelleme</b></summary>

Ngrok, uygulamanızı internet üzerinden erişilebilir hale getirmek için güvenli bir tünel oluşturur. Bu, NAT ve güvenlik duvarı sınırlamalarını aşmanıza olanak tanır. WebRTC sinyal sunucusu olarak çalışan Flask uygulamanız, ngrok tüneli üzerinden erişilebilir olur, böylece internet üzerindeki kullanıcılar P2P bağlantı kurabilir.
</details>

## 🌐 Tarayıcı Desteği

<table>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/chrome/chrome_48x48.png" width="24px" height="24px" alt="Chrome"><br>Chrome</td>
    <td align="center"><img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/firefox/firefox_48x48.png" width="24px" height="24px" alt="Firefox"><br>Firefox</td>
    <td align="center"><img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/edge/edge_48x48.png" width="24px" height="24px" alt="Edge"><br>Edge</td>
    <td align="center"><img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/safari/safari_48x48.png" width="24px" height="24px" alt="Safari"><br>Safari*</td>
  </tr>
  <tr>
    <td align="center">✅</td>
    <td align="center">✅</td>
    <td align="center">✅</td>
    <td align="center">⚠️</td>
  </tr>
</table>

\* Safari'de kısmi destek bulunmaktadır.

## 📄 Lisans

<div align="center">
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
  
  Bu proje MIT lisansı altında lisanslanmıştır.
  
</div>

## 📞 İletişim

Sorularınız veya önerileriniz için GitHub üzerinden issue açabilir veya pull request gönderebilirsiniz.

---

<div align="center">
  <sub>❤️ ile geliştirilmiştir</sub>
</div> 