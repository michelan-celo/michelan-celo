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
│   │   ├── *.png
│   │   └── *.webp
│   ├── languages-card.svg
│   ├── profile-background.png
│   ├── profile-background-source.gif
│   ├── profile-console-poster.png
│   ├── profile-console.webp
│   ├── profile-header.svg
│   ├── quote-card.svg
│   ├── song-1.svg
│   ├── spacecraft-01.gif
│   ├── spacecraft-02.gif
│   ├── toolkit-icons/
│   │   ├── catia.png
│   │   ├── freeflyer.png
│   │   ├── gmat.png
│   │   ├── orekit.png
│   │   ├── solidworks.png
│   │   ├── spenvis.png
│   │   └── stk.png
│   └── toolkit-card.svg
├── data/
│   ├── current-selection.json
│   ├── music.json
│   └── quotes.json
├── scripts/
│   ├── build_background.py
│   ├── build_profile_animation.py
│   └── update_dashboard.py
├── ANIMASYON.md
├── KURULUM.md
├── YUKLEME.md
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

`profile-space-mission` klasörünün kendisini depoya yükleme; bu klasörün
içindekileri yükle. Doğru durumda depo kökünde doğrudan `README.md`, `.github`,
`assets`, `data` ve `scripts` görünür.

Yükleme tamamlanınca `README.md` ile `assets` klasörü aynı kök dizinde
görünmelidir.

## 3. Canlı yenilemeyi ilk kez çalıştır

1. Deponun **Actions** sekmesine gir.
2. Soldan **Refresh mission console** iş akışını seç.
3. **Run workflow** düğmesine bas.

İlk çalıştırmadan sonra contribution panelindeki önizleme uyarısı GitHub'ın
tam yıllık contribution calendar verisiyle değiştirilir. Panelin gösterdiği
toplam, çizilen günlük hücrelerin toplamına eşit değilse işlem bilerek hata
verir. Takvim izometrik bir 3B düzlem olarak çizilir: katkısız günler açık renk
karolardır; katkılı günler GitHub'ın yeşil paletini kullanır ve gerçek günlük
katkı sayısı arttıkça yeşil sütunun yüksekliği artar. Bütün gün hücreleri aynı
geometriyi kullanır.
Aynı işlem listenden bir şarkı ve Fatih
Terim, Şenol Güneş veya Abdullah Avcı sözlerinden birini seçerek iki kartı
günceller. Son seçim `data/current-selection.json` içinde tutulduğu için arka
arkaya aynı şarkı veya aynı söz gelmez. **Run workflow** düğmesine her basışında
yeni bir seçim yapılır.

İş akışı her gün bir kez otomatik çalışır. İstersen **Run workflow** düğmesiyle
istediğin anda elle yenileyebilirsin. GitHub README sayfa ziyaretinde kod çalıştıramadığı için
seçim tarayıcıdaki her F5 işleminde değil, bu iş akışı çalıştığında değişir.
GitHub yoğunluğuna bağlı olarak zamanlanmış çalışmalarda gecikme olabilir.
Yeni çalışmada katkı paneli GitHub GraphQL API verisinden baştan üretilir; API
başarısız olursa eski veya boş paneli gerçekmiş gibi yayımlamak yerine iş akışı
hata verir. Ek uygulama bağlantısı, kişisel
erişim anahtarı veya elle oluşturulmuş secret gerekmez; yalnızca GitHub'ın bu
depoya özel otomatik `GITHUB_TOKEN` yetkisini kullanır.

`GITHUB_TOKEN` varsayılan kurulumda hesabın token tarafından görülebilen
katkılarını getirir. GitHub profilinde anonim özel contribution'ları göstermeyi
açtıysan, profil sayfasının sayısı ile bu kart arasında fark kalabilir; özel
depoları okuyacak ek bir kişisel erişim anahtarı bu pakete bilerek eklenmemiştir.

### Yazma yetkisi hatası görülürse

Depoda **Settings → Actions → General → Workflow permissions** bölümüne girip
**Read and write permissions** seçeneğini etkinleştir. Ardından iş akışını
yeniden çalıştır.

## Animasyon davranışı

Her uydu GIF'i 60 karelik, 12 saniyelik kesintisiz bir döngüdür:

- normal görünümde 6 saniyede tam 360 derece dönüş,
- aynı konum ve eksende holograma geçiş,
- hologram görünümünde 6 saniyede tam 360 derece dönüş,
- birkaç derecelik yavaş ve dikişsiz eksen kayması.

İki uydu farklı eksen yolları izler. GitHub profil README dosyası JavaScript
çalıştırmadığından ziyaretçi başına rastgele veya fareyle etkileşimli eksen
seçimi yapılamaz; ayrıntılı teknik not `ANIMASYON.md` içindedir.

Uydu animasyonlarında ayrı kart çerçevesi, Ay veya yörünge çizgisi yoktur.
İki uydu da profilin ortak Dünya arka planındaki kendi bölümünde döner.

## Arka plan

Profilin ana tasarım tuvali `1280 × 1348 px` ölçüsündedir. Kaynak Dünya GIF'inin
12 saniyelik ışık döngüsü korunur; yapay yakınlaşma veya kayma efekti eklenmez.
GitHub SVG içine gömülmüş animasyonu her zaman oynatmadığı için son görünüm tek
bir `assets/profile-console.webp` dosyası olarak hazırlanır. Arka plan, iki
uydu, paneller, contribution takvimi, şarkı ve söz aynı 1280 × 1348 hareketli
yüzeyde birleştirilir. Böylece panel birleşimlerinde arka plan parçalara ayrılmaz
ve hareket tarayıcıda doğrudan WebP animasyonu olarak oynar.

Sohbet yüklemesinde animasyon tek kareye dönüştüğü için aynı kaynağın hareketli
kopyası kullanıldı: `https://giphy.com/gifs/earth-planet-americas-l5JbspfwZ0yjHjlJ0K`.

Tasarım çerçevesizdir: başlık kutusu, panel sınırları, ilgi alanı kapsülleri,
toolkit kutuları ve ikon konturları kullanılmaz. Panellerin içinde ayrıca
karartılmış bir kutu katmanı da yoktur; yalnızca bütün arka plana eşit uygulanan
hafif karartma bulunur. Renkli barlar ile contribution hücreleri veri işaretleri
olduğu için korunur.

Engineering Toolkit alanındaki STK, GMAT, FreeFlyer, Orekit, SPENVIS,
SOLIDWORKS ve CATIA işaretleri `assets/toolkit-icons/` klasöründe saklanır ve
SVG içine veri olarak gömülür. Bu nedenle GitHub README görünümünde harici bir
ikon sunucusuna bağlı değildir.

Arka plan görselini daha sonra değiştirmek için yeni görseli
`assets/profile-background-source.gif` adıyla koyup yerel bilgisayarında
önce `python3 -m pip install Pillow`, ardından
`python3 scripts/build_background.py` komutunu çalıştırabilirsin. Bu komut ana
animasyonu hafifçe karartır ve paneller için gereken eşleşen parçaları üretir.
Ardından `ALLOW_PREVIEW_DATA=1 python3 scripts/update_dashboard.py` komutu kartları
ve tek parça profil animasyonunu yeniden üretir.

Dağıtım ZIP'i yalnızca yerel QA/önizleme dosyalarını içermez. Otomatik GitHub
Actions yenilemesi için gereken kaynak arka plan GIF'i, uydu GIF'leri, kartlar,
ikonlar ve oluşturma komutları pakette bulunur.
