1 - "nolu" kelimesi "sokak" tan önce geliyorsa sil
2 - sokakta -> sokak
3 - mahalle -> mahallesi
4 - mh. -> mahallesi
5 - cd. -> caddesi
6 - sk. -> sokak
7 - sok. -> sokak
8 - skk -> sokak
9 - cdd -> caddesi
10 - apt. -> apartmanı

4 - no dan sonrasını almasın (nerde)

****
yandex geocoder kullan.
https://yandex.com/dev/maps/geocoder/doc/desc/examples/geocoder_examples.html?from=mapsapi

Received message: ‼️TEYİTLİ‼️ ANTAKYA ‼️ Oda başı mahallesi. Sultanevler 2. Sokak, blok 2/12 merkez Antakya/ Hatay 4 kişi enkaz altında yaşıyorlar enkaz altındakilerden biri Kusay... SES GELİYORMUŞ ACİL EKİP YOLLLANMASI LAZIM
Label: 1
‼️teyi̇tli̇‼️ antakya ‼️ oda başı mahallesi .  sultanevler 2 .  sokak ,  blok 2 / 12 merkez antakya /  hatay 4 kişi enkaz altında yaşıyorlar enkaz altındakilerden biri kusay .  .  .  ses geli̇yormuş aci̇l eki̇p yolllanmasi lazim
['‼️teyi̇tli̇‼️', 'antakya', '‼️', 'oda', 'başı', 'mahallesi', '.', 'sultanevler', '2', '.', 'sokak', ',', 'blok', '2', '/', '12', 'merkez', 'antakya', '/', 'hatay', '4', 'kişi', 'enkaz', 'altında', 'yaşıyorlar', 'enkaz', 'altındakilerden', 'biri', 'kusay', '.', '.', '.', 'ses', 'geli̇yormuş', 'aci̇l', 'eki̇p', 'yolllanmasi', 'lazim']
['O', 'O', 'O', 'O', 'B-LOCATION', 'O', 'O', 'B-LOCATION', 'I-LOCATION', 'I-LOCATION', 'O', 'B-LOCATION', 'I-LOCATION', 'O', 'I-LOCATION', 'O', 'O', 'O', 'O', 'O', 'O', 'B-LOCATION', 'O', 'B-LOCATION', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-PERSON', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
başı sultanevler 2 . , blok / kişi altında


lcoation finderdan dönen loc_value = loc_string

loc_clues = ["mahhale", "cadde", "sokak"]

if loc_string contains [loc_clues]:

********************************************************
--Address Extraction
yandex api de aratırken
addressten "blok", "no" çıkart
addresslerde kısaltmaları düzelt mah -> mahalle sok -> sokak
addresslerden noktalama işaretlerini kaldır.
yandex.api de aratılcağı zaman long, lat diye arat.

--Scrape
Scrape ederken çadır filtresi koy.
Ağır hasarlı yapı ve hafif hasarlı yapı özelinde ara.

1 - Başlangıçtan, Chapter three ye kadar (1 gün)
    1.4 - En son yaz.
2 - Chapter Three (1 gün)
3 - Chapter Four (3 gün) (Datasets and Metodologies)
    3.1 - General Methodology
    3.2 - Datasets
    3.3 - Damage Classification 
    3.4 - Location Extraction
    3.5 - Application
4 - Chapter Five (1 gün)
5 - Chapter Six (2 gün) (Application)
6 - Chapter Seven, Eight (1 gün)
7 - Aplly Tez Format (1 gün)

Appendix koy Example Olarak.

O
O
O
O
B_LOCATION
I_LOCATION
I_LOCATION
I_LOCATION
O
O
B_LOCATION
I_LOCATION
O
O
O
O
O 


[0.201,  0.081,  0.068,  0.062,  0.057,  0.054,  0.051,  0.050,  0.047,  0.046,  0.044,  0.043,  0.041,  0.040,  0.039,  0.038,  0.037,  0.036,  0.035,  0.034,  0.033,  0.033,  0.031,  0.031,  0.031]


[0.130, 0.072, 0.065, 0.062, 0.059, 0.059, 0.058, 0.056, 0.053, 0.053, 0.052, 0.051, 0.052, 0.050, 0.050, 0.049, 0.049, 0.048, 0.049, 0.048, 0.052, 0.048, 0.048, 0.048, 0.048]


	0.68	0.70	0.72	0.71	0.71	0.75	0.69	0.71
	0.67	0.68	0.71	0.67	0.68	0.73	0.71	0.72
	0.70	0.71	0.74	0.71	0.72	0.74	0.71	0.72
	0.68	0.70	0.74	0.68	0.70	0.76	0.71	0.72
	0.68	0.69	0.70	0.68	0.69	0.71	0.68	0.69
	0.69	0.69	0.70	0.70	0.70	0.71	0.70	0.70
	0.67	0.68	0.70	0.66	0.67	0.71	0.68	0.69
	0.70	0.71	0.72	0.69	0.70	0.72	0.70	0.71
	0.66	0.67	0.70	0.61	0.63	0.72	0.68	0.70
	0.64	0.66	0.69	0.64	0.66	0.72	0.65	0.67
	0.65	0.66	0.68	0.65	0.66	0.72	0.66	0.68
	0.66	0.67	0.68	0.66	0.67	0.73	0.68	0.70

 0.72 0.71 0.72 0.74 0.70 0.70 0.70 0.72 0.68 0.69 0.68 0.68

[0.181 ,0.079 ,0.067 ,0.060 ,0.056 ,0.053 ,0.051 ,0.048 ,0.046 , 0.045 , 0.044 , 0.042 , 0.041 , 0.040 , 0.039 , 0.038 , 0.037 , 0.036 , 0.035 , 0.035 , 0.034 , 0.033 , 0.033 , 0.032 , 0.031]

[0.086, 0.114, 0.065, 0.061, 0.059, 0.057, 0.058, 0.055, 0.054, 0.056, 0.053, 0.051, 0.051, 0.051, 0.050, 0.050, 0.049, 0.050, 0.049, 0.048, 0.049, 0.051, 0.049, 0.049, 0.048]