
# import json
# from ner.entity_finder import EntityFinder
# with open("prediction_module/nlp_sources/Gazzeters/il_ilce_mahalle_gazetters.json", encoding="utf-8") as f:
#     gazzeters = json.load(f)

# town_list = []
# neignours_list = []

# for pro_name, towns in gazzeters.items():
#     for town_name, neignours in towns.items():
#         town_list += town_name
#         neignours_list += neignours

# print(len(town_list))
# print(len(neignours_list))

# ef = EntityFinder()

# def turkish_to_english(text):
#     turkish_chars = "çğıöşüÇĞİÖŞÜ"
#     english_chars = "cgiosuCGIOSU"
#     translation_table = str.maketrans(turkish_chars, english_chars)l
#     return text.translate(translation_table)

# Bitişik Yazım Testi
##sentence = " battalgazi buhara caddesi tan doğan mahallesi 1 sokak" # tan doğan LİSTEDE BİTİŞİK YAZILMIŞ.
##sentence = "ürgen paşa mahallesi atatürk cad 18 sok yurtcan apt antakya" # ürgen paşa LİSTEDE BİTİŞİK YAZILMIŞ.
##sentence = "mimarsinan mahallesinde . alparslan türkeş bulvarı no kervan pastanesinin üst binası onikişubat kahramanmaraş adresinde" # MİMAR SİNAN LİSTEDE AYRI YAZILMIŞ.

# Bulvar Test
##sentence = "adiyaman atatürk bulvarı yavuz selim mahallesi 1 nolu sağlık ocağı göçer apartmanı" #Done ***Found Missing il
##sentence = "bebek ekinci mahallesi i̇nönü bulvarı no 128 alya uçar apartmanı hatay antakya" #Done
##sentence = "mimar sinan mahallesi alparslan türkeş blv no 42 kervan pastanesi üstü kahraman maraş" #Done
##sentence = "hayrullah mahallesi kuddusi baba bulvarı telbisoğlu apartmanı onikişubat kahramanmaraş" #Done
##sentence = "mimar sinan mahallesi alparslan türkeş blv no 42 kervan pastanesi üstü kahraman kahramanmaraş" #Done
##sentence = "kahramanmaraş . i̇smetpaşa mah . azerbaycan bulvari . no 17 belli̇ apartmani" #Done

# Sokak Test
sentence = "ekinci mahallesi 3011 sokak candemir apartmanı antakya hatay" #Done
##sentence = "orhangazi mahallesi akcakoyunlu sokak no ondort kahramanmaraş onikisubat bagli" #Done
##sentence = "akevler mahalle 4 . akevler sok . behzatoğlu si̇tesi̇ no i̇ç kapi no antakya hatay bihter karaca yakını" #Done
##sentence = "odabaşı mahallesi kayuka kazi anne sokak akademi sitesi blok" #Done
##sentence = "hatay i̇skenderun barıştepe mahallesi ali 356 sokak" #Done
##sentence = "akevler mahallesi meltem sokak tuğçe apartmanı antakya hatay" #Done 
##sentence = "hatay i̇skenderun barıştepe mahallesi 356 sokak" #Done
##sentence = "1266 . akevler . mahalle 4 . akevler sok . behzatoğlu si̇tesi̇ no i̇ç kapi no antakya bihter karaca yakını antakya" #TODO İncele neden mahalle bulamıyor.

# Cadde Test
##sentence = "ürgenpaşa mahallesi atatürk cad 18 sok yurtcan apt antakya" #Done #TODO:NOKTA KOYMUYOR.
##sentence = "kurtderesi mahallesi sait döner caddesi no samandağ hatay‼️‼️‼️" #Done
##sentence = "şazibey mahallesi stad caddesi gülbike apartmanı no un kahramanmaraş" 
##sentence = "general şükrü kanatlı cad hakkı dede beyoğlu sk . çağlar ap no34 / 4 hatay" #Done
##sentence = "mehmet akif ersoy caddesi no 67 / yılmaz apartmanı daire i̇skenderun ," #Done
##sentence = "altınşehir mahallesi gökkuşağı caddesi no 5 d blok merkez adiyaman" # Done

# Sokak Cadde Test
##sentence = "Alsancak Mahallesi Ayasofya caddesi 221 . Sokak Kırıkhan / HATAY" #Done
##sentence = "hasan tütün mahallesi şekip önder caddesi üzümlü kent sokak apartmanları blok besni adıyaman" #Done
##sentence = "Alsancak Mustafa bey caddesinde ki  çocukların iş yeri için aynı şeyi söyleyemiyorum kirişler de ve duvarlarda derin çatlaklar oluştu bina komple acil boşaltıldı. https://t.co/EXlSAEVAaa"
##sentence = "İstanbul Pendik'te bugün meydana gelen deprem sonrası bir binada çatlaklar oluştu. Bina sakinleri evlerinden tahliye edilirken, çevrede geniş çaplı güvenlik önlemi alındı. https://t.co/dk1SjfBrvj https://t.co/iLmud9EK6R"
##sentence = "Deprem sırasında ailem İzmirdeydi. Ve evimiz depremden en çok etkilenen bölge Manavkuyu, Mansuroğlu’nda. Evde 1-2 çatlak"

#sentence = "Mithatpaşa cad. No. 1189 Arifbey apt. Fahrettin Altay adresindeki bitişik nizamda bulunan apartmanımız" #Done
#sentence = "fatih’te" #Done
#sentence = "Kemeraltı’nın en eski binalarından biri olan Bilen İş Hanı deprem sonrası kırık ve çatlak kolonlarına rağmen, defalarca kez başvurulduğu halde neden hala denetlenmedi ve her aramada oyalıyorsunuz? @izmirhim @izmirbld"
#sentence = "esentepe mah . evren apt . hatay🙏2 avustralya"
#sentence = "kışlasaray mahallesi harbiye caddesi nilüfer apartmanında" #TODO: Apartman yanındakine bişi demesin #Done
#sentence = " turgut reis mahallesi eski valilik sokak gürsoy apartmanı" # reis mahallesi buluyor
#sentence = "kırıkhan mahallesi sakarya sokak hatay" #TODO: sokak diye etiketlenen varsa başka bir tag yapma. #Done
#sentence = "karapınar caddesi no" # cadde diye etiketlenen varsa başka bir tag alma.
#sentence = "cumhuriyet mahallesi 25184 nolu sokak Narlıkuyu sitesi Zeliha ve Yusuf Karadoğan enkaz altındalar ulaşamıyoruz yardım edin lütfe" #nolu sokak case'i
#sentence = "yeni mahallesi 2638sok no"
#sentence = "i̇stasyon mahallesi osmaniye sokak no petrol ofisi yanı türkoğlu kahramanmaraş yaylım lğtfen"
#sentence = "azerbaycan bulvari belediye binasi aydin apartmani kahramanmaras hayrullah ertuğrul atiye" #Done
#sentence = "barbaros hayrettin paşa mahallesi 1614sk klas apartman" #Done
#sentence = " hatayda odabaşı mahallesi kurşunlu sokak ılgın apartmanı migrosun antakya" #Done
#sentence = "barboros mahallesi atatürk bulvarı aydın apartmanı no daire 7 merkez adiyaman" #Done
#sentence = "karapınar mahallesi bağdere caddesinde yağmur kent sitesinde" #ilk önce adres identifierları işaretlet. #Done
sentence = "adiyama i̇si̇as hotele"
sentence = "‼️ aci̇l 🆘 bu yavrumuz hatay’da enkaz altında kurtarılmayı bekliyor lütfen yardım edecek bir allahım kulu yok mu ? allah’ını seven rt yapsın, vicdanı olan rt yapsın (adres: ekinci mahallesi güneş caddesi gökküşağı ap. hatay merkez )"
sentence = "ankara adıyaman adıyaman cumhuriyet mahallesi" #TODO: ilk bulduuğu ili almasın hepsine baksın il var mı diye.
#TODO: 
# 1999 depremi, 99 depremi geçen tweeleri filtrele hiç sokma classification sonrası.
# Sadece 1 adres belirteci olanı alma. EntityFiner outputunda ve geocodera gönderme. Örnek: Turkeş bulvarı alma.
# Otomatik Test Senaryolarını koşacak bir yapı yap.
# print(sentence)
# print(ef.address_filter(sentence.split()))

from pymongo import MongoClient
import uuid

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['DamagedBuildingsDB']
collection = db['Maras_DamagedTweets_1_v2']

# Find documents that don't have a 'uuid' field
query = {'uuid': {'$exists': False}}
documents = collection.find(query)

# Update documents with UUID
for document in documents:
    # Generate a UUID
    new_uuid = str(uuid.uuid4())

    # Update the document with the UUID
    collection.update_one(
        {'_id': document['_id']},
        {'$set': {'uuid': new_uuid}}
    )

print('UUIDs added to existing documents.')


