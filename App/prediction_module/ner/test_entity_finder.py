import pytest
from .entity_finder import EntityFinder
ef = EntityFinder()

def test_unified_address():
    assert ef.address_filter(" battalgazi buhara caddesi tan doğan mahallesi 1 sokak".split()) == "tandogan Mahallesi, 1. Sokak, buhara Caddesi, battalgazi, malatya"
    assert ef.address_filter("ürgen paşa mahallesi atatürk cad 18 sok yurtcan apt antakya".split()) == "urgenpasa Mahallesi, 18. Sokak, ataturk Caddesi, antakya, hatay"
    assert ef.address_filter("mimarsinan mahallesinde . alparslan türkeş bulvarı no kervan pastanesinin üst binası onikişubat kahramanmaraş adresinde".split()) == "mimar sinan Mahallesi, alparslan turkes Bulvarı, onikisubat, kahramanmaras"

def test_boulevard_address():
    assert ef.address_filter("mimar sinan mahallesi alparslan türkeş blv no 42 kervan pastanesi üstü kahraman maraş".split()) == "mimar sinan Mahallesi, alparslan turkes Bulvarı, onikisubat, kahramanmaras"
    assert ef.address_filter("adiyaman atatürk bulvarı yavuz selim mahallesi 1 nolu sağlık ocağı göçer apartmanı".split()) == "yavuz selim Mahallesi, ataturk Bulvarı, golbasi, adiyaman"
    assert ef.address_filter("bebek ekinci mahallesi i̇nönü bulvarı no 128 alya uçar apartmanı hatay antakya".split()) == "ekinci Mahallesi, inonu Bulvarı, antakya, hatay"
    assert ef.address_filter("hayrullah mahallesi kuddusi baba bulvarı telbisoğlu apartmanı onikişubat kahramanmaraş".split()) == "hayrullah Mahallesi, kuddusi baba Bulvarı, onikisubat, kahramanmaras"
    assert ef.address_filter("mimar sinan mahallesi alparslan türkeş blv no 42 kervan pastanesi üstü kahraman kahramanmaraş".split()) == "mimar sinan Mahallesi, alparslan turkes Bulvarı, onikisubat, kahramanmaras"
    assert ef.address_filter("kahramanmaraş . i̇smetpaşa mah . azerbaycan bulvari . no 17 belli̇ apartmani".split()) == "ismetpasa Mahallesi, azerbaycan Bulvarı, dulkadiroglu, kahramanmaras"

def test_street_address():
    assert ef.address_filter("ekinci mahallesi 3011 sokak candemir apartmanı antakya hatay".split()) == "ekinci Mahallesi, 3011. Sokak, antakya, hatay"
    assert ef.address_filter("orhangazi mahallesi akcakoyunlu sokak no ondort kahramanmaraş onikisubat bagli".split()) == "orhangazi Mahallesi, akcakoyunlu Sokak, onikisubat, kahramanmaras"
    assert ef.address_filter("akevler mahalle 4 . akevler sok . behzatoğlu si̇tesi̇ no i̇ç kapi no antakya hatay bihter karaca yakını".split()) == "akevler Mahallesi, 4. akevler Sokak, antakya, hatay"
    assert ef.address_filter("odabaşı mahallesi kayuka kazi anne sokak akademi sitesi blok".split()) == "odabasi Mahallesi, kayuka kazi anne Sokak,"
    assert ef.address_filter("hatay i̇skenderun barıştepe mahallesi ali 356 sokak".split()) == "baristepe Mahallesi, ali 356. Sokak, iskenderun, hatay"
    assert ef.address_filter("akevler mahallesi meltem sokak tuğçe apartmanı antakya hatay".split()) == "akevler Mahallesi, meltem Sokak, antakya, hatay"
    assert ef.address_filter("hatay i̇skenderun barıştepe mahallesi 356 sokak".split()) == "baristepe Mahallesi, 356. Sokak, iskenderun, hatay"
    assert ef.address_filter("1266 . akevler . mahalle 4 . akevler sok . behzatoğlu si̇tesi̇ no i̇ç kapi no antakya bihter karaca yakını antakya".split()) == "akevler Mahallesi, 4. akevler Sokak, antakya, hatay"

def test_avenue_address():
    assert ef.address_filter("ürgenpaşa mahallesi atatürk cad 18 sok yurtcan apt antakya".split()) == "urgenpasa Mahallesi, 18. Sokak, ataturk Caddesi, antakya, hatay"
    assert ef.address_filter("kurtderesi mahallesi sait döner caddesi no samandağ hatay‼️‼️‼️".split()) == "kurtderesi Mahallesi, sait doner Caddesi, samandag, hatay"
    assert ef.address_filter("şazibey mahallesi stad caddesi gülbike apartmanı no un kahramanmaraş".split()) == "sazibey Mahallesi, stad Caddesi, onikisubat, kahramanmaras"
    assert ef.address_filter("general şükrü kanatlı cad hakkı dede beyoğlu sk . çağlar ap no34 / 4 hatay".split()) == "hakki dede beyoglu Sokak, kanatli Caddesi, hatay"
    assert ef.address_filter("mehmet akif ersoy caddesi no 67 / yılmaz apartmanı daire i̇skenderun ,".split()) == "ersoy Caddesi, iskenderun, hatay"
    assert ef.address_filter("altınşehir mahallesi gökkuşağı caddesi no 5 d blok merkez adiyaman".split()) == "altinsehir Mahallesi, gokkusagi Caddesi, merkez, adiyaman"

def test_mixed_address():
    assert ef.address_filter("Alsancak Mahallesi Ayasofya caddesi 221 . Sokak Kırıkhan / HATAY".split()) == "alsancak Mahallesi, 221. Sokak, ayasofya Caddesi, kirikhan, hatay"
    assert ef.address_filter("hasan tütün mahallesi şekip önder caddesi üzümlü kent sokak apartmanları blok besni adıyaman".split()) == "hasan tutun Mahallesi, uzumlu kent Sokak, sekip onder Caddesi, besni, adiyaman"
    assert ef.address_filter("Alsancak Mustafa bey caddesinde ki  çocukların iş yeri için aynı şeyi söyleyemiyorum kirişler de ve duvarlarda derin çatlaklar oluştu bina komple acil boşaltıldı. https://t.co/EXlSAEVAaa".split()) == "alsancak Mahallesi, mustafa bey Caddesi,"
    assert ef.address_filter("İstanbul Pendik'te bugün meydana gelen deprem sonrası bir binada çatlaklar oluştu. Bina sakinleri evlerinden tahliye edilirken, çevrede geniş çaplı güvenlik önlemi alındı. https://t.co/dk1SjfBrvj https://t.co/iLmud9EK6R".split()) == "pendik, istanbul"
    assert ef.address_filter("Deprem sırasında ailem İzmirdeydi. Ve evimiz depremden en çok etkilenen bölge Manavkuyu, Mansuroğlu’nda. Evde 1-2 çatlak".split()) == "mansuroglu Mahallesi,"