# GitHub profilini yayınlama

Bu paket `michelan-celo` hesabı için hazırlanmıştır. Profil sayfasının tamamı
İngilizcedir. Mevcut GitHub profil fotoğrafını veya hesap ayarlarını değiştirmez.

## Paket içeriği

```text
profile-space-mission/
├── .github/
│   └── workflows/
│       └── refresh-dashboard.yml
├── assets/
│   ├── about-card.svg
│   ├── activity-card.svg
│   ├── background/
│   │   └── *.png
│   ├── languages-card.svg
│   ├── profile-background.png
│   ├── profile-background-source.png
│   ├── profile-header.svg
│   ├── quote-card.svg
│   ├── song-1.svg
│   ├── spacecraft-01.gif
│   ├── spacecraft-02.gif
│   └── toolkit-card.svg
├── data/
│   ├── music.json
│   └── quotes.json
├── scripts/
│   ├── build_background.py
│   └── update_dashboard.py
├── KURULUM.md
└── README.md
```

## 1. Profil deposunu oluştur

1. GitHub'da **New repository** seçeneğine gir.
2. Depo adını kullanıcı adınla tamamen aynı yaz: `michelan-celo`.
3. Depoyu **Public** olarak oluştur.
4. Otomatik README ekleme; pakette hazır bir `README.md` bulunuyor.

## 2. Dosyaları yükle

ZIP dosyasını bilgisayarında aç. İçindeki bütün dosya ve klasörleri
`michelan-celo/michelan-celo` deposunun köküne yükle. Özellikle `.github`,
`assets`, `data` ve `scripts` klasörlerinin yapısını koru.

Yükleme tamamlanınca `README.md` ile `assets` klasörü aynı kök dizinde
görünmelidir.

## 3. Günlük yenilemeyi ilk kez çalıştır

1. Deponun **Actions** sekmesine gir.
2. Soldan **Refresh mission console** iş akışını seç.
3. **Run workflow** düğmesine bas.

İlk çalıştırmadan sonra contribution panelindeki `SYNC PENDING` yazısı gerçek
GitHub etkinlik verinle değiştirilir. Aynı işlem listenden bir şarkı ve Fatih
Terim, Şenol Güneş veya Abdullah Avcı sözlerinden birini seçerek iki kartı
günceller. **Run workflow**
düğmesine her basışında yeni bir rastgele seçim yapılır.

İş akışı ayrıca her gün otomatik çalışır. GitHub README sayfa ziyaretinde kod
çalıştıramadığı için seçim her sayfa yenilemesinde değil, bu iş akışı
çalıştığında değişir. Ek uygulama bağlantısı, kişisel
erişim anahtarı veya elle oluşturulmuş secret gerekmez; yalnızca GitHub'ın bu
depoya özel otomatik `GITHUB_TOKEN` yetkisini kullanır.

### Yazma yetkisi hatası görülürse

Depoda **Settings → Actions → General → Workflow permissions** bölümüne girip
**Read and write permissions** seçeneğini etkinleştir. Ardından iş akışını
yeniden çalıştır.

## Animasyon davranışı

Her uydu GIF'i yaklaşık 12 saniyelik kesintisiz bir döngüdür:

- yaklaşık 6 saniye normal malzeme,
- aynı kamera açısında ani hologram geçişi,
- yaklaşık 6 saniye hologram malzemesi,
- başlangıç pozuna kesintisiz dönüş.

Uydu animasyonlarında ayrı kart çerçevesi, Ay veya yörünge çizgisi yoktur.
İki uydu da profilin ortak Dünya arka planındaki kendi bölümünde döner.

## Arka plan

Profilin ana tasarım tuvali `1280 × 1348 px` ölçüsündedir. Yüklenen kaynak
dosya GIF uzantılı olmasına rağmen tek kare PNG içeriğine sahip olduğu için
arka plan sabittir; uydu animasyonları hareket etmeye devam eder.

Arka plan görselini daha sonra değiştirmek için yeni görseli
`assets/profile-background-source.png` adıyla koyup yerel bilgisayarında
önce `python3 -m pip install Pillow`, ardından
`python3 scripts/build_background.py` komutunu çalıştırabilirsin. Bu komut ana
görseli hafifçe karartır ve paneller için gereken eşleşen parçaları üretir.
