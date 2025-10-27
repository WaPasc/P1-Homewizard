# Test database
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "EnergyData"
org = "MyHome"
token = "supersecret-stadenberg-token-8840-WP-ID1"
# Store the URL of your InfluxDB instance
url="http://localhost:8086"

client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)


p = influxdb_client.Point("my_measurement").tag("location", "Belgium").field("temperature", 29.3)
write_api.write(bucket=bucket, org=org, record=p)