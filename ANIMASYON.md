# Uydu animasyonu

Profildeki iki uydu aynı 12 saniyelik döngüyü kullanır:

1. X, Y ve Z açılarına farklı yönlerde sabit açısal hız atanır.
2. Açılar ileri-geri salınmadan kareden kareye birikir.
3. Normal görünüm 6 saniye sürer ve aynı pozda holograma geçer.
4. On ikinci saniyede her eksen toplam tam 360 derece tamamlamış olur.
5. Son tutum başlangıç tutumuyla aynı olduğu için animasyon kesintisiz tekrarlar.

Animasyon 60 kare ve kare başına 200 ms kullanır. İki uydunun başlangıç tutumu
ve X/Y/Z dönüş yönleri farklıdır. GitHub profil README dosyaları JavaScript
çalıştırmadığı için hızlar ziyaretçi başına yeniden rastgele seçilemez; render
sırasında belirlenir ve bütün döngü boyunca sabit kalır.
