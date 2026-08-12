# Uydu animasyonu

Profildeki iki uydu aynı 12 saniyelik döngüyü kullanır:

1. Normal görünümde 6 saniyede tam 360 derece döner.
2. Konumu ve ekseni değişmeden hologram görünümüne geçer.
3. Hologram görünümünde 6 saniyede bir tam tur daha döner.
4. Dönüş ekseni, tur boyunca birkaç derece yavaşça kayar.
5. Son kare başlangıç eksenine yumuşak biçimde döner ve animasyon kesintisiz tekrarlar.

Animasyon 60 kare ve kare başına 200 ms kullanır. İki uydu için farklı,
önceden belirlenmiş eksen yolları vardır. GitHub profil README dosyaları
JavaScript çalıştırmadığı için eksen ziyaretçi başına rastgele seçilemez; bu
yapı aynı görsel etkiyi küçük, kesintisiz bir eksen kaymasıyla verir.
