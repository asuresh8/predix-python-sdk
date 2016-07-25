import requests
import yaml
from predix import get_proxy
import json

class UserAccountAuthentication:
    def __init__(self, url):
        self.url = url
        self.admin_token = ''

    def authenticate_admin(self, short_token):
        headers = {'Pragma': 'no-cache',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept': 'application/json',
                   'Cache-Control': 'no-cache',
                   'Authorization': 'Basic ' + short_token,
                   'Connection': 'keep-alive'}
        data = "grant_type=client_credentials"
        r = requests.post(self.url+'/oauth/token', proxies=get_proxy(), headers=headers, data=data)
        r.raise_for_status()
        self.admin_token = r.json()['access_token']
        return self.admin_token

    def authenticate_client(self, short_token, client):
        headers = {'Pragma': 'no-cache',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept': 'application/json',
                   'Cache-Control': 'no-cache',
                   'Authorization': 'Basic ' + short_token}
        data = 'client_id='+client+'&grant_type=client_credentials'
        r = requests.post(self.url+'/oauth/token', proxies=get_proxy(), headers=headers, data=data)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))['access_token']

    def authenticate_user(self, short_token, username, password):
        headers = {'Pragma': 'no-cache',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept': 'application/json',
                   'Cache-Control': 'no-cache',
                   'Authorization': 'Basic ' + short_token}
        data = 'username='+username+'&password='+password+'&grant_type=password'
        r = requests.post(self.url+'/oauth/token', proxies=get_proxy(), headers=headers, data=data)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))['access_token']

    def create_client(self, client_name, client_secret):
        if not self.admin_token:
            raise Exception("Must authenticate as admin")
        else:
            headers = {'Pragma': 'no-cache',
                       'Content-Type': 'application/json',
                       'Accept': 'application/json',
                       'Cache-Control': 'no-cache',
                       'Authorization': 'Basic ' + self.admin_token}
            data = {"client_id": client_name,
                    "client_secret": client_secret,
                    "scope": ["uaa.none","openid"],
                    "authorized_grant_types": ["authorization_code","client_credentials","refresh_token","password"],
                    "authorities": ["openid","uaa.none","uaa.resource"],
                    "autoapprove": ["openid"]}
            r = requests.post(self.url+'/oauth/clients', proxies=get_proxy(), headers=headers, data=data)
            r.raise_for_status()
            return yaml.safe_load(json.dumps(r.json()))

    def create_user(self, username, password, email):
        if not self.admin_token:
            raise Exception("Must authenticate as admin")
        else:
            headers = {'Pragma': 'no-cache',
                       'Content-Type': 'application/json',
                       'Accept': 'application/json',
                       'Cache-Control': 'no-cache',
                       'Authorization': 'Basic ' + self.admin_token}
            data = {"userName": username,
                    "password": password,
                    "emails": [{"value":email}]}
            r = requests.post(self.url+'/Users', proxies=get_proxy(), headers=headers, data=data)
            r.raise_for_status()
            return yaml.safe_load(json.dumps(r.json()))

    def create_group(self, group_name):
        if not self.admin_token:
            raise Exception("Must authenticate as admin")
        else:
            headers = {'Pragma': 'no-cache',
                       'Content-Type': 'application/json',
                       'Accept': 'application/json',
                       'Cache-Control': 'no-cache',
                       'Authorization': 'Basic ' + self.admin_token}
            data = {"displayName": group_name}
            r = requests.post(self.url+'/Groups', proxies=get_proxy(), headers=headers, data=data)
            r.raise_for_status()
            return yaml.safe_load(json.dumps(r.json()))

    def get_group(self, group_name):
        if not self.admin_token:
            raise Exception("Must authenticate as admin")
        else:
            headers = {'Pragma': 'no-cache',
                       'Content-Type': 'application/json',
                       'Accept': 'application/json',
                       'Cache-Control': 'no-cache',
                       'Authorization': 'Basic ' + self.admin_token}
            r = requests.get(self.url + '/Groups?filter=displayName+eq+%22'+ group_name +'%22&startIndex=1',
                              proxies=get_proxy(),
                              headers=headers)
            r.raise_for_status()
            return yaml.safe_load(json.dumps(r.json()))

    def get_user(self, username):
        if not self.admin_token:
            raise Exception("Must authenticate as admin")
        else:
            headers = {'Pragma': 'no-cache',
                       'Content-Type': 'application/json',
                       'Accept': 'application/json',
                       'Cache-Control': 'no-cache',
                       'Authorization': 'Basic ' + self.admin_token}
            r = requests.get(self.url + '/Users?attributes=id%2CuserName&filter=userName+eq+%22'+ username +'%22&startIndex=1',
                             proxies=get_proxy(),
                             headers=headers)
            r.raise_for_status()
            return yaml.safe_load(json.dumps(r.json()))

    def add_to_group(self, username, group_name):
        if not self.admin_token:
            raise Exception("Must authenticate as admin")
        else:
            headers = {'Pragma': 'no-cache',
                       'Content-Type': 'application/json',
                       'Accept': 'application/json',
                       'Cache-Control': 'no-cache',
                       'Authorization': 'Basic ' + self.admin_token}
            data = {'displayName': group_name,
                    'userName': username}
            r = requests.put(self.url + '/Groups',
                             proxies=get_proxy(),
                             headers=headers)
            r.raise_for_status()


class TenantManagement:
    def __init__(self, instance_id, token, url='https://tms-vpc.run.aws-usw02-pr.ice.predix.io'):
        self.url = url
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': 'Basic ' + token,
                        'Predix-Zone-Id': instance_id}

    def create(self, tenant_data):
        r = requests.post(self.url + '/tenant',
                         proxies=get_proxy(),
                         headers=self.headers,
                         data = tenant_data)
        r.raise_for_status()

    def delete(self, tenant_name):
        r = requests.delete(self.url + '/tenant/'+tenant_name,
                         proxies=get_proxy(),
                         headers=self.headers)
        r.raise_for_status()

    def get(self, tenant_name):
        r = requests.get(self.url + '/tenant/' + tenant_name,
                         proxies=get_proxy(),
                         headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def update(self, tenant_data):
        r = requests.get(self.url + '/tenant',
                         proxies=get_proxy(),
                         headers=self.headers,
                         data = tenant_data)
        r.raise_for_status()


class AccessControlService:
    def __init__(self, instance_id, token, url='https://predix-acs.run.aws-usw02-pr.ice.predix.io'):
        self.url = url
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': 'Basic ' + token,
                        'Predix-Zone-Id': instance_id}

    def get_resources(self):
        r = requests.get(self.url + '/resource/',
                         proxies=get_proxy(),
                         headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def create_resource(self, resource):
        r = requests.post(self.url + '/resource/',
                         proxies=get_proxy(),
                         headers=self.headers,
                         data = resource)
        r.raise_for_status()

    def delete_resource(self, resource_id):
        r = requests.delete(self.url + '/resource/'+resource_id,
                          proxies=get_proxy(),
                          headers=self.headers)
        r.raise_for_status()

    def get_resource(self, resource_id):
        r = requests.get(self.url + '/resource/'+resource_id,
                         proxies=get_proxy(),
                         headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def update_resource(self, resource_id, resource):
        r = requests.put(self.url + '/resource/' + resource_id,
                         proxies=get_proxy(),
                         headers=self.headers,
                         data=resource)
        r.raise_for_status()

    def get_subjects(self):
        r = requests.get(self.url + '/subject/',
                         proxies=get_proxy(),
                         headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def create_subject(self, subject):
        r = requests.post(self.url + '/subject/',
                          proxies=get_proxy(),
                          headers=self.headers,
                          data=subject)
        r.raise_for_status()

    def delete_subject(self, subject_id):
        r = requests.delete(self.url + '/subject/' + subject_id,
                            proxies=get_proxy(),
                            headers=self.headers)
        r.raise_for_status()

    def get_subject(self, subject_id):
        r = requests.get(self.url + '/subject/' + subject_id,
                         proxies=get_proxy(),
                         headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def update_subject(self, subject_id, subject):
        r = requests.put(self.url + '/subject/' + subject_id,
                         proxies=get_proxy(),
                         headers=self.headers,
                         data=subject)
        r.raise_for_status()

    def get_policies(self):
        r = requests.get(self.url + '/policy-set/',
                         proxies=get_proxy(),
                         headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def delete_policy(self, policy_set_id):
        r = requests.delete(self.url + '/policy-set/' + policy_set_id,
                            proxies=get_proxy(),
                            headers=self.headers)
        r.raise_for_status()

    def get_policy(self, policy_set_id):
        r = requests.get(self.url + '/policy-set/' + policy_set_id,
                         proxies=get_proxy(),
                         headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def update_policy_set(self, policy_set_id, policy_set):
        r = requests.put(self.url + '/policy-set/' + policy_set_id,
                         proxies=get_proxy(),
                         headers=self.headers,
                         data=policy_set)
        r.raise_for_status()

class DataIntegrityAssurance:
    pass
