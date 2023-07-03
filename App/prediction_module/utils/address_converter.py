import requests
import xml.etree.ElementTree as ET

def get_nominatim_geocode(address):
    api_url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&countrycodes=TR&addressdetails=1"
    response = requests.get(api_url)
    data = response.json()
    if len(data) > 0:
        return (data[0]['lat'], data[0]['lon'])
    else:
        return None
    
def get_yandex_map_geocoder(address):

    encoded_address = requests.utils.quote(address)

    api_key = "d7d2934d-eea3-4580-946a-bc2c3c3cd21c"
    api_url = f"https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&format=json&geocode={address}&lang=en-US"
    response = requests.get(api_url)
    data = response.json()
    try:
        geocodes = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()
        print(geocodes)
        if len(geocodes) > 0:
            return (geocodes[1], geocodes[0])
        else:
            return None
    except Exception as e:
        print(e)
        return None
    
def get_opencagedata(address):
    pass

# address = "İstiklal Caddesi, Beyoğlu, İstanbul, Türkiye"
# address = "Mustafa Kemal Mahallesi, Çankaya, Ankara"
# address = "Bahçelievler Mah 501 Sokak, KIRIKHAN, HATAY"
# geocode = get_yandex_map_geocoder(address)
# print(geocode)