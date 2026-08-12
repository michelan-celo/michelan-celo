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
- `YUKLEME.md`

GitHub yükleme ekranında **Replace files** seçeneğini kabul et. Eski
`README.md`, `assets`, `data`, `scripts` ve `.github` içeriklerinin yenileriyle
değiştiğinden emin ol.

Doğru yüklemeden sonra depo kökünde doğrudan `README.md` ve `assets` görünür.
`profile-space-mission/README.md` biçiminde fazladan bir üst klasör
oluşmamalıdır.

İlk yüklemeden sonra **Actions → Refresh mission console → Run workflow**
adımını bir kez çalıştır. Gerekirse **Settings → Actions → General → Workflow
permissions → Read and write permissions** seçeneğini etkinleştir.

Profil sayfasını kontrol ederken `Ctrl + F5` kullan. README yalnızca
`assets/profile-console.webp` dosyasını gösterir; bu tek dosya hareketli arka
planı, iki uyduyu ve bütün panelleri içerdiği için birleşim çizgisi oluşmaz.
