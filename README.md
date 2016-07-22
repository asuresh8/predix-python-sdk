## Predix SDK

### Security

#### User Account Authentication
```python
# import package
from ge.predix.security import UserAccountAuthentication
# connect to instance
uaa = UserAccountAuthentication('<url>')
# authenticate admin
uaa_token = uaa.authenticate_admin('<short_token>')
# authenticate client
uaa_token = uaa.authenticate_client('<short_token>', '<client>')
# authenticate user
uaa_token = uaa.authenticate_user('<short_token>', 'username', 'password')
# create client
client = uaa.create_client('<client_name>', '<client_secret>')
# create user
user = uaa.create_user('username', 'password', 'email')
# get user
user = uaa.get_user('username')
# create group
group = uaa.create('<group>')
# get group
group = uaa.get_group('<group>')
# add_to_group
uaa.add_to_group('username', 'group_name')
```

#### Tenant Management
```python
# import package
from ge.predix.security import TenantManagement
# connect to instance
tm = TenantManagement('<instance_id>', '<token>')
# create tenant
tm.create({<tenant_data>})
# delete tenant
tm.delete('<tenant_name>')
# get tenant
tm.get{'<tenant_name'}
# update tenant
tm.update({<tenant_data>})
```

#### Access Control Service
```python
# import package
from ge.predix.security import AccessControlService
# connect to instance
acs = AccessControlService('<instance_id>', '<token>')
# get resources
resources = acs.get_resources()
# create resource
acs.create_resource({<resource>})
# delete resource
acs.delete_resource('<resource_id>')
# get resource
resource = acs.get_resource('<resource_id>')
# update resource
acs.update_resource('<resource_id>', {<resource>})
# get subjects
subjects = acs.get_subjects()
# create subject
acs.create_subject({<subject>})
# delete subject
acs.delete_subject('<subject_id>')
# get subject
subject = acs.get_subject('<subject_id>')
# update subject
acs.update_subject('<subject_id>', {<subject>})
# get policies
policies = acs.get_policies()
# delete policy
acs.delete_policy('<policy_set_id>')
# update policy
acs.update_policy_set('<policy_set_id>', policy_set)
```

### Geospatial services

#### Geo Enhance
```python
# import package
from ge.predix.geospatial_services import GeoEnhance
# create instance
geo = GeoEnhance('<instance_id>', '<token>')
# find address by Location
address = geo.address_by_location('<lat>', '<lon>')
# poi by Location
points = geo.poi_by_location('<lat>', '<lon>')
# place by Location
place = geo.place_by_location('<lat>', '<lon>')
# timezone by Location
timezone = geo.timezone_by_location('<lat>', '<lon>')
```

#### Smart World Intelligent Mapping
```python
# import package
from ge.predix.geospatial_services import SmartWorldIntelligentMapping
# create instance
smart_map = ('<instance_id>', '<token>')
# get collections
collections = smart_map.get_collection()
# get specific collection
collection = smart_map.get('<name>')
# delete collection
smart_map.delete('<name>')
# spatial query
smart_map.spatial_query('<name>', '<x1>', '<x2>', '<y1>', '<y2>')
# text query
smart_map.text_query('<name>', '<text>')
```

####Intelligent Environments
*All classes have the same functions in the current version of Predix*
```python
# import package
from ge.predix.intelligent_envrionments import TrafficPlanning, ParkingPlanning, PedestrianPlanning, PublicSafety, IndoorPositioning, EnterpriseEnvironment
# connect to instance
current_system = TrafficPlanning('<instance_id>', '<token>')
# get assets
assets = current_system.assets()
# search assets
assets = current_system.search_assets('<q-type>', '<q-value>', [<bbox>], <page>, <size>)
# get asset
asset = current_system.get_asset('<asset_id>')
# get events
events = current_system.get_events('<asset_id>', [<event_types>], <start>, <end>, <size>)
# get live events
live_events = current_system.get_live_events('<asset_id>', [<event_types>], <size>)
# get media
media = current_system.get_media('<asset_id>', [<media_types>], <start>, <end>, '<location_id>', <page>, <size>)
# get locations
locations = current_system.locations()
# search location
locations = current_system.search_location('<location_type>', [<bbox>], <page>, <size>)
# get location
location = get_location('<location_id>')
# get location analytics
analysis = get_location_analytics('<location_id>', [<analytic_names>], [<analytic_categories>], <start>, <end>)
```

### Data Management

#### Asset Data
```python
# import package
from ge.predix.data_management import AssetData
# connect to database
db = AssetData('<instance_id>', '<uaa_token>')
# post to database
db.post('<item>', {<data>})
# select from database
data = db.get('<item>', filters={<filters>}, fields=[<fields>], page_size=<page_size>)
# delete from database
db.delete('<item>')
# audit trace
audit_data = db.audit(filters={<filters>}, page_size=<page_size>)
```

#### Time Series
```python
# import package
from ge.predix.data_management import TimeSeries
# connect to database
db = TimeSeries('<instance_id>', '<uaa_token>')
# ingest data
db.ingest({<data>})
# query database
data = db.query({<query>})
```

#### Message Queue
```python
# import package
from ge.predix.data_management import MessageQueue
# create instance
ampq = MessageQueue('<host>')
# send message
ampq.send('<queue>', '<message>', exchange='<exchange>', properties={<properties>})
# receive message
ampq.receive(<callback_function>, '<queue>')
```
*Use [pika](https://www.rabbitmq.com/tutorials/tutorial-one-python.html) for more advanced usage*

#### Key Value Store
```python
# import package
from ge.predix.data_management import KeyValueStore
# connect to instance
redis_db = KeyValueStore(host='<host>', password='<password>', port='<port>')
```
*KeyValueStore is a simple inheritance of [redis-py](https://github.com/andymccurdy/redis-py), see [documentation](https://redis-py.readthedocs.io/en/latest/)*

#### SQL Database
```python
# import package
from ge.predix.data_management import SQLDatabase
# connect to instance
pgdb = SQLDatabase(host='<host>', database='<database>', user='<user>', password='<password>')
```
*See documentation further down on using postgres databases*

#### Blobstore
```python
# import package
from ge.predix.data_management import Blobstore
# connect to instance
blob = Blobstore('<access_key_id>', '<secret_access_key>', '<bucket_name>')
# put new items
blob.put('<filename>', '<data>')
# get items
blob.get('<filename>', '<target_filename>')
```
