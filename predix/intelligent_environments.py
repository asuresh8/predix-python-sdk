"""
module ge.predix.intelligent_planning
"""
import requests
import yaml
import json
from ge.data.utilities import get_proxy


class _CurrentSystem:
    def __init__(self, instance_id, token, url):
        self.url = url
        self.headers = {'Content-Type': 'application/hal+json',
                        'Authorization': 'bearer ' + token,
                        'Predix-Zone-Id': instance_id}

    def assets(self):
        r = requests.get(self.url+'/assets', proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def search_assets(self, q_type=None, q_value=None, bbox=None, page=None, size=None):
        params = {}
        if q_type is not None and q_value is not None:
            if q_type not in ['device-type', 'media-type', 'event-type']:
                raise Exception('invalid q type')
            
            elif q_type == 'device-type':
                if type(q_value) in ['list', 'tuple']:
                    if any(q_value) not in ['NODE', 'CAMERA', 'MIC', 'ENV']:
                        raise Exception('Invalid q value for device_type')
                    else:
                        params['q'] = 'device-type:' + ';'.join(q_value)
                elif type(q_value).__name__ != 'str':
                    raise Exception('Invalid type for q value')
                elif q_value not in ['NODE', 'CAMERA', 'MIC', 'ENV']:
                    raise Exception('Invalid q value for device-type')
                else:
                    params['q'] = 'device-type:' + q_value

            elif q_type == 'media-type':
                if type(q_value) in ['list', 'tuple']:
                    if any(q_value) not in ['IMAGE', 'VIDEO', 'AUDIO']:
                        raise Exception('Invalid q value for media_type')
                    else:
                        params['q'] = 'media-type:' + ';'.join(q_value)
                elif type(q_value).__name__ != 'str':
                    raise Exception('Invalid type for q value')
                elif q_value not in ['IMAGE', 'VIDEO', 'AUDIO']:
                    raise Exception('Invalid q value for media-type')
                else:
                    params['q'] = 'media-type:' + q_value
                
            elif q_type == 'event-type':
                if type(q_value) in ['list', 'tuple']:
                    if any(q_value) not in ['PKIN', 'PKOUT', 'SFIN', 'SFOUT', 'TFEVT', 'ENCGH'
                                                            'TEMP', 'OCCUPANCY', 'LIGHT_LEVEL']:
                        raise Exception('Invalid q value for event_type')
                    else:
                        params['q'] = 'event-type:' + ';'.join(q_value)
                elif type(q_value).__name__ != 'str':
                    raise Exception('Invalid type for q value')
                elif q_value not in ['PKIN', 'PKOUT', 'SFIN', 'SFOUT', 'TFEVT', 'ENCGH'
                                                            'TEMP', 'OCCUPANCY', 'LIGHT_LEVEL']:
                    raise Exception('Invalid q value for event-type')
                else:
                    params['q'] = 'event-type:' + q_value

        if bbox is not None and type(bbox).__name__ in ['tuple', 'list'] and len(bbox) == 4:
            params['bbox'] = str(bbox[0])+':'+str(bbox[1])+','+str(bbox[2])+':'+str(bbox[3])

        if page is not None and type(page).__name__ in ['int', 'float', 'long', 'complex']:
            params['page'] = int(page)

        if size is not None and type(size).__name__ in ['int', 'float', 'long', 'complex']:
            params['size'] = int(size)

        r = requests.get(self.url + '/assets/search', proxies=get_proxy(), headers=self.headers, params=params)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def get_asset(self, asset_id):
        r = requests.get(self.url + '/assets/' + asset_id, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def get_events(self, asset_id, event_types, start, end, size=None):
        params = {}
        if type(event_types) in ['list', 'tuple']:
            for event_type in event_types:
                if event_type not in ['PKIN', 'PKOUT', 'SFIN', 'SFOUT', 'TFEVT', 'ENCGH', 
                                      'TEMP', 'OCCUPANCY', 'LIGHT_LEVEL']:
                    raise Exception('Invalid Event Type')
            params['event-types'] = ','.join(event_types)

        params['start-ts'] = start
        params['end-ts'] = end
        if size is not None and type(size).__name__ in ['int', 'float', 'long', 'complex']:
            params['size'] = int(size)

        r = requests.get(self.url + '/assets/' + asset_id + 'events', proxies=get_proxy(), headers=self.headers,
                         params=params)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def get_live_events(self, asset_id, event_types, size):
        params = {}
        if type(event_types) in ['list', 'tuple']:
            for event_type in event_types:
                if event_type not in ['PKIN', 'PKOUT', 'SFIN', 'SFOUT', 'TFEVT', 'ENCGH',
                                      'TEMP', 'OCCUPANCY', 'LIGHT_LEVEL']:
                    raise Exception('Invalid Event Type')
            params['event-types'] = ','.join(event_types)


        if size is not None and type(size).__name__ in ['int', 'float', 'long', 'complex']:
            params['size'] = int(size)

        r = requests.get(self.url + '/assets/' + asset_id + '/live-events', proxies=get_proxy(),
                         headers=self.headers, params=params)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def get_media(self, asset_id, media_types, start, end, location_id=None, page=None, size=None):
        params = {}
        if type(media_types) in ['list', 'tuple']:
            for media_type in media_types:
                if media_type not in ['IMAGE', 'VIDEO', 'AUDIO']:
                    raise Exception('Invalid media Type')
            params['media-types'] = ','.join(media_types)

        params['start-ts'] = start
        params['end-ts'] = end

        if location_id is not None and type(location_id).__name__ == 'str':
            params['locationId'] = location_id
        if page is not None and type(page).__name__ in ['int', 'float', 'long', 'complex']:
            params['page'] = int(page)
        if size is not None and type(size).__name__ in ['int', 'float', 'long', 'complex']:
            params['size'] = int(size)

        r = requests.get(self.url + '/assets/' + asset_id + '/media', proxies=get_proxy(),
                         headers=self.headers, params=params)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def locations(self):
        r = requests.get(self.url+'/locations', proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def search_location(self, location_type=None, bbox=None, page=None, size=None):
        params = {}
        if location_type is not None:
            if type(location_type).__name__ == 'str':
                if location_type not in ['PARKING_SPOT','PARKING_ZONE','CROSSWALK','TRAFFIC_LANE',
                                         'RETAIL_STORE', 'PARKING_SPOT,PARKING_ZONE']:
                    raise Exception('Invalid location type for parking')
                else:
                    params['q'] = 'location_-type:' + location_type
            elif type(location_type).__name__ in ['list', 'tuple']:
                if any(location_type) not in ['PARKING_SPOT','PARKING_ZONE','CROSSWALK','TRAFFIC_LANE',
                                              'RETAIL_STORE', 'PARKING_SPOT,PARKING_ZONE']:
                    raise Exception('Invalid location type for parking')
                else:
                    params['q'] = 'location_-type:' + ';'.join(location_type)

        if bbox is not None and type(bbox).__name__ in ['tuple', 'list'] and len(bbox) == 4:
            params['bbox'] = str(bbox[0])+':'+str(bbox[1])+','+str(bbox[2])+':'+str(bbox[3])

        if page is not None and type(page).__name__ in ['int', 'float', 'long', 'complex']:
            params['page'] = int(page)

        if size is not None and type(size).__name__ in ['int', 'float', 'long', 'complex']:
            params['size'] = int(size)

        r = requests.get(self.url + '/locations/search', proxies=get_proxy(), headers=self.headers,
                         params=params)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def get_location(self, location_id):
        r = requests.get(self.url + '/locations/' + location_id, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def get_location_analytics(self, location_id, analytic_names, analytic_categories, start, end):
        params = {}
        if type(analytic_names).__name__ in ['list', 'tuple']:
            params['analytic-names'] = ';'.join(analytic_names)
        elif type(analytic_names).__name__ =='str':
            params['analytic-names'] = analytic_names
        
        if type(analytic_categories).__name__ in ['list', 'tuple']:
            params['analytic-categories'] = ';'.join(analytic_categories)
        elif type(analytic_categories).__name__ =='str':
            params['analytic-categories'] = analytic_categories

        params['start-ts'] = start
        params['end-ts'] = end

        r = requests.get(self.url + '/locations/' + location_id + '/analytics', proxies=get_proxy(),
                         headers=self.headers, params=params)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))


class TrafficPlanning(_CurrentSystem):
    def __init__(self, instance_id, token, url='https://ie-traffic.run.aws-usw02-pr.ice.predix.io'):
        _CurrentSystem.__init__(self, instance_id, token, url)


class ParkingPlanning(_CurrentSystem):
    def __init__(self, instance_id, token, url='https://ie-parking.run.aws-usw02-pr.ice.predix.io'):
        _CurrentSystem.__init__(self, instance_id, token, url)


class PedestrianPlanning(_CurrentSystem):
    def __init__(self, instance_id, token, url='https://ie-pedestrian.run.aws-usw02-pr.ice.predix.io'):
        _CurrentSystem.__init__(self, instance_id, token, url)


class PublicSafety(_CurrentSystem):
    def __init__(self, instance_id, token, url='https://ie-public-safety.run.aws-usw02-pr.ice.predix.io'):
        _CurrentSystem.__init__(self, instance_id, token, url)


class IndoorPositioning(_CurrentSystem):
    def __init__(self, instance_id, token, url='https://ie-positioning.run.aws-usw02-pr.ice.predix.io'):
        _CurrentSystem.__init__(self, instance_id, token, url)


class EnterpriseEnvironment(_CurrentSystem):
    def __init__(self, instance_id, token, url='https://ie-environmental.run.aws-usw02-pr.ice.predix.io'):
        _CurrentSystem.__init__(self, instance_id, token, url)

