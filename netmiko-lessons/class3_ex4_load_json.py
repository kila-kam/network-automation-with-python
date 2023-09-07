import json
from pprint import pprint

with open('arista_arp.json') as f:
	data=json.load(f)
#	data=json.dumps(data, indent=4, sort_keys=True)
pprint(data)



