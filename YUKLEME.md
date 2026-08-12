# GitHub'a yüklenecek dosyalar

Bu ZIP'i açtıktan sonra `profile-space-mission` klasörünün **içine gir**.
Klasörün kendisini değil, içindeki bütün dosya ve klasörleri
`michelan-celo/michelan-celo` deposunun köküne yükle:

- `.github/`
- `assets/`
- `data/`
- `scripts/`
- `README.md`
- `KURULUM.md`
- `ANIMASYON.md`
- `YUKLEME.md`

GitHub yükleme ekranında **Replace files** seçeneğini kabul et. Eski
`README.md`, `assets`, `data`, `scripts` ve `.github` içeriklerinin yenileriyle
değiştiğinden emin ol.

Doğru yüklemeden sonra depo kökünde doğrudan `README.md` ve `assets` görünür.
`profile-space-mission/README.md` biçiminde fazladan bir üst klasör
oluşmamalıdır.

İlk yüklemeden sonra **Actions → Refresh mission console → Run workflow**
adımını bir kez çalıştır. Otomatik yenileme günde bir kez çalışır; profil
ziyaretçiler için yalnızca hazırlanmış WebP dosyasını yüklediğinden daha hafiftir. Gerekirse **Settings → Actions → General → Workflow
permissions → Read and write permissions** seçeneğini etkinleştir.

Profil sayfasını kontrol ederken `Ctrl + F5` kullan. README, hareketli arka
planı, iki uyduyu ve bütün panelleri tek `assets/profile-console.webp` dosyası
olarak gösterir; böylece birleşim çizgisi oluşmaz. Ana görsel bağlantısızdır.
Altındaki `COLLABORATE ↗` ve seçili şarkı adı iki ayrı bağlantıdır.
