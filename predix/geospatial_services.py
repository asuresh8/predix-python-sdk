"""
module ge.predix.geospatial_services
By: Adi Suresh
"""
import base64
import requests
import yaml
import json
from ge.data.utilities import get_proxy


class GeoEnhance:
    def __init__(self, instance_id, token,
                 url='https://pitney-bowes-geoenhancement-service-basic.run.aws-usw02-pr.ice.predix.io'):
        self.headers = {'Content-Type': 'application/json;charSet=utf-8',
                        'Authorization': 'bearer ' + token,
                        'Predix-Zone-Id': instance_id}
        self.base_url = url

    def address_by_location(self, lat, lon):
        url = self.base_url + '/address/bylocation​?' + 'latitude=' + lat + '&longitude=' + lon
        r = requests.get(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def poi_by_location(self, lat, lon):
        url = self.base_url + '/poi/bylocation​?' + 'latitude=' + lat +'&longitude=' + lon
        r = requests.get(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def place_by_location(self, lat, lon):
        url = self.base_url + '/place/bylocation​?' + 'latitude=' + lat +'&longitude=' + lon
        r = requests.get(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def timezone_by_location(self, lat, lon):
        url = self.base_url + '/timezone/bylocation​?' + 'latitude=' + lat +'&longitude=' + lon
        r = requests.get(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))


class _Geo:
    def __init__(self, api_key, secret):
        base64_key = base64.b64encode(api_key + ":" + secret)
        temp_headers = {'Authorization': 'Basic ' + base64_key,
                        'Content-Type': 'application/x-www-form-urlencoded'}
        data = 'grant_type=client_credentials'
        r = requests.get('https://api.pitneybowes.com/oauth/token', proxies=get_proxy(), headers=temp_headers)
        r.raise_for_status()
        access_token = yaml.safe_load(json.dumps(r.json()))['access_token']
        self.headers = {'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + access_token}


class Geo911(_Geo):
    def __init__(self, api_key, secret):
        _Geo.__init__(self, api_key, secret)

    def psap_by_address(self, address):
        url = 'https://api.pitneybowes.com/location-​intelligence/geo911/v1/psap/byaddress​?address=1 ' + address
        r = requests.get(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def psap_by_location(self, lat, lon):
        url = 'https://api.pitneybowes.com/location-intelligence/geo911/​v1/psap/bylocation?' + \
              'latitude=' + lat + '&longitude=' + lon
        r = requests.get(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

class GeoLife(_Geo):
    def __init__(self, api_key, secret):
        _Geo.__init__(self, api_key, secret)

    def demographics_by_address(self, address):
        url = 'https://api.pitneybowes.com/location-intelligence/geolife/v1/​demographics/byaddress?address=1 ' + address
        r = requests.get(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def demographics_by_location(self, lat, lon):
        url = 'http://api.pitneybowes.com/location-intelligence/geolife/v1/​demographics/bylocation?' + \
              'latitude=' + lat + '&longitude=' + lon
        r = requests.get(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def segmentation_by_address(self, address):
        url = 'https://api.pitneybowes.com/location-intelligence​/geolife/v1/segmentation/byaddress?address=​1 ' + address
        r = requests.get(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def segmentation_by_location(self, lat, lon):
        url = 'https://api.pitneybowes.com/location-​intelligence/geolife/v1/segmentation/bylocation?' + \
              'latitude=' + lat + '&longitude=' + lon
        r = requests.get(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

class GeoSearch(_Geo):
    def __init__(self, api_key, secret):
        _Geo.__init__(self, api_key, secret)

    def geo_search(self, lat, lon, search_text='Global'):
        url = 'https://api.pitneybowes.com/location-intelligence/​geosearch/v1/locations?searchText=1%20' + \
              search_text + '%20V&longitude=' + lon +  '&latitude=' + lat
        r = requests.get(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

class GeoTax(_Geo):
    def __init__(self, api_key, secret):
        _Geo.__init__(self, api_key, secret)

    def tax_by_address(self, address, purchase_amount, tax_rate_type='Auto'):
        url = 'http://api.pitneybowes.com/location-​intelligence/geotax/v1/tax/' + tax_rate_type + \
              '/byaddress?address=' + address + '&purchaseAmount=' + purchase_amount
        r = requests.get(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def tax_by_location(self, lat, lon, purchase_amount, tax_rate_type='Auto'):
        url = 'http://api.pitneybowes.com/location-​intelligence/geotax/v1/tax/' + tax_rate_type + \
              '/bylocation?latitude=' + lat + '&longitude' + lon + '&purchaseAmount=' + purchase_amount
        r = requests.get(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def taxrate_by_address(self, address, tax_rate_type='Auto'):
        url = 'http://api.pitneybowes.com/location-​intelligence/geotax/v1/taxrate/' + tax_rate_type + \
              '/byaddress?address=' + address
        r = requests.get(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def taxrate_by_location(self, lat, lon, tax_rate_type='Auto'):
        url = 'http://api.pitneybowes.com/location-intelligence​/geotax/v1/taxrate/' + tax_rate_type + \
              '/​bylocation?latitude=' + lat + '&longitude=' + lon
        r = requests.get(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

class GeoCode(_Geo):
    def __init__(self, api_key, secret, premium=False):
        _Geo.__init__(self, api_key, secret)
        self.premium = premium

    def get(self, place_name=None, main_address=None, last_line=None, area_name_1=None,
            area_name_2=None, area_name_3=None, area_name_4=None, postal_code=None, country=None):
        if self.premium:
            url = 'https://api.pitneybowes.com​/location-intelligence/​geocode-service/v1/transient​/premium/geocode'
        else:
            url = 'https://api.pitneybowes.com​/location-intelligence/​geocode-service/v1/transient​/basic/geocode'
        params=[]
        if place_name:
            params.append('placeName=' + place_name)
        if main_address:
            params.append('mainAddress=' + main_address)
        if last_line:
            params.append('lastLine=' + last_line)
        if area_name_1:
            params.append('areaName1=' + area_name_1)
        if area_name_2:
            params.append('areaName1=' + area_name_2)
        if area_name_3:
            params.append('areaName1=' + area_name_3)
        if area_name_4:
            params.append('areaName1=' + area_name_4)
        if postal_code:
            params.append('postalCode=' + postal_code)
        if country:
            params.append('country=' + country)
        url += '&'.join(params)
        r = requests.get(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def get_all(self, request_data):
        if self.premium:
            url = 'https://api.pitneybowes.com​/location-intelligence/​geocode-service/v1/transient​/premium/geocode'
        else:
            url = 'https://api.pitneybowes.com​/location-intelligence/​geocode-service/v1/transient​/basic/geocode'
        r = requests.post(url, proxies=get_proxy(), headers=self.headers, data=request_data)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def reverse_get(self):
        url='https://api.pitneybowes.com​/location-intelligence/​geocode-service/v1/transient​/premium/reverseGeocode'
        r = requests.get(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def reverse_get_all(self, request_data):
        url = 'https://api.pitneybowes.com​/location-intelligence/​geocode-service/v1/transient​/premium/reverseGeocode'
        r = requests.post(url, proxies=get_proxy(), headers=self.headers, data=request_data)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))


class SmartWorldIntelligentMapping:
    def __init__(self, instance_id, token, url='https://intelligent-mapping-prod.run.aws-usw02-pr.ice.predix.io'):
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': 'bearer ' + token,
                        'Predix-Zone-Id': instance_id}
        self.url = url

    def get_collections(self):
        r = requests.get(self.url + '/collections', proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def get(self, name):
        r = requests.get(self.url + '/collections/' + name, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def delete(self, name):
        r = requests.delete(self.url + '/collections/' + name, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def spatial_query(self, name, x1, y1, x2, y2):
        temp_url = self.url + '/collections/'+name+'/spatial-query/bbox-interacts/{0},{1},{2},{3}'.format(x1,y1,x2,y2)
        r = requests.delete(temp_url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def text_query(self, name, text):
        temp_url = self.url + '/collections/'+name+'/text-query/free/' + text
        r = requests.delete(temp_url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))
