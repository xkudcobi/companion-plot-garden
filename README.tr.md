# Komşu Tarla (Companion Plot)

In English: [README.md](README.md)

**Komşu Tarla bir bahçe yatağı bulmacası: bitkileri yatağa diz, hangi komşuların birbirine iyi geldiğini, hangilerinin kavga ettiğini gör; canlı bir puan bahçenin ne kadar verimli olacağını söylesin.**

Açıldığında yatak zaten dolu, yani hemen kurcalamaya başlayabilirsin. Bir bitkiye, sonra bir kareye dokun; yatak yeşile (mutlu komşular) ya da kırmızıya (kavgacı komşular) döner. Bir ekim ayı seç; mevsimi olmayan bitkilerde kar tanesi belirir. Takılırsan istediğin kare için öneri iste.

Hesap açmak, ek paket kurmak, ayar yapmak yok. Kendi bilgisayarında çalışır, hiçbir bilgi dışarı çıkmaz.

## Çalıştırma

Tek ihtiyacın Python 3.8 veya üstü.

```
python3 -m companion_plot
```

Tarayıcın kendiliğinden açılır. Açılmazsa terminalde yazan adresi aç (genelde `http://127.0.0.1:8765/`). Durdurmak için terminalde Ctrl+C'ye bas.

## Dil

Sayfanın sağ üstündeki **TR | EN** düğmesini kullan; bütün sayfa anında değişir ve seçimin hatırlanır. İlk açılışta tarayıcının diline bakılır. Terminalde `--lang tr` ya da `--lang en` yazabilirsin; yazmazsan sistem dili kullanılır, bulunamazsa İngilizce.

## Nasıl oynanır

1. Yatağın altındaki sıradan bir bitki seç (ya da silgiyi).
2. Yatakta kareleri tıklayarak ek. Aynı bitkinin olduğu kareye tekrar dokunursan kare boşalır.
3. Sağdaki puana bak. Yeşil karelerin dost komşuları var, kırmızıların düşmanı. Karenin üstündeki küçük sayı onun ruh halidir.
4. Ekim ayını seç. O ay ekilemeyen bitkiler kesik çizgili mavi çerçeve ve kar tanesi alır, puanından da düşer.
5. **Seçili kareye öneri ver** düğmesi, tüm yatağın puanını en çok yükselten bitkiyi bulur.
6. Aşağıdaki hasat takviminde yatağındaki her bitkinin hangi aylarda ekilebildiğini ve sepetin (🧺) ne zaman dolacağını görürsün.

### Puan nasıl hesaplanıyor

| Durum | Puan |
| --- | --- |
| İki dost bitki yan yana (üst, alt, sol, sağ) | +2 |
| İki düşman bitki yan yana | -3 |
| Aynı bitki yan yana (zararlılar yayılır) | -1 |
| Mevsimi dışında ekilmiş bitki | -2 |
| Çeşitlilik ödülü: her farklı bitki için, en çok 6 | +1 |

Toplam, dolu karelerin sayısına bölünüp 0-100 arasına ölçeklenir.

## Komut satırı seçenekleri

```
python3 -m companion_plot [--lang tr|en] [--port 8765] [--no-browser] [--show]
```

- `--lang` terminal dili.
- `--port` denenecek ilk port; doluysa sıradaki boş port kullanılır.
- `--no-browser` tarayıcıyı açmaz.
- `--show` örnek tarlayı ve puanını terminale yazdırıp çıkar.

## Proje yapısı

- `companion_plot/data.py` bitkiler, ekim ayları, dost/düşman tablosu.
- `companion_plot/engine.py` puanlama, hasat ayları, kare önerileri.
- `companion_plot/strings.py` Türkçe ve İngilizce bütün metinler, tek tabloda.
- `companion_plot/server.py` standart kütüphaneyle yazılmış küçük HTTP sunucusu (JSON API ve sayfa).
- `companion_plot/web/` sayfanın kendisi: HTML, CSS ve sade JavaScript.
- `tests/` birim testleri.

Testleri şöyle çalıştırırsın:

```
python3 -m unittest discover -s tests -t .
```

## Notlar ve sınırlar

Bitki eşleşmeleri yaygın bahçıvanlık geleneklerine dayanır; bir oyun olarak düşünülmüştür, ziraat tavsiyesi değildir. Ekim ayları kuzey yarımküredeki ılıman iklime göre yazılmıştır.

## Hakkında

farmOS gibi çiftlik kayıt uygulamalarının konusundan esinlenildi ama tamamen kendi küçük işi: kimin kimin yanına oturması gerektiğini düşündüren bir oyuncak. Projenin geliştirilmesinde yapay zekâ destekli araçlardan (Claude) yararlanıldı.
