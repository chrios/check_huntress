#!/usr/bin/env python3

### =============================================================== ###
### A Nagios plugin to check the huntress API for incident reports  ###
### Uses: ./check_huntress.py -p PUBLICKEY -s SECRETKEY             ###
### =============================================================== ###

import requests, base64, argparse, sys

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--publickey", type=str, help="Your Huntress API public key")
parser.add_argument("-s", "--secretkey", type=str, help="Your Huntress API private key")

args = parser.parse_args()

huntress_public_key = args.publickey
huntress_private_key = args.secretkey

huntress_combined_key = f"{huntress_public_key}:{huntress_private_key}"
huntress_base64_combined_key = base64.b64encode(bytes(huntress_combined_key,'utf-8'))

api_auth_header = {
        'Authorization': f"Basic {huntress_base64_combined_key.decode()}",
        'Accept': 'application/json'
        }
api_params = {
        'limit': 500
        }

response = requests.get(
        'https://api.huntress.io/v1/incident_reports',
        headers=api_auth_header,
        params=api_params
        )

if response.status_code != 200:
    print(f"UNKNOWN - HTTP error connecting to huntress api: {response.status_code} ")
    sys.exit(3)

json_response = response.json()

if len(json_response['incident_reports']) > 0:
    for report in json_response['incident_reports']:
        if report['status'] == 'sent':
            print(f"CRITICAL - Sent incident report found! Subject: {report['subject']}")
            sys.exit(2)
        elif report['status'] == 'closed':
            print(f"WARNING - Closed incident report found! Subject: {report['subject']}")
            sys.exit(1)
else:
    print('OK - No incident reports found')
    sys.exit(0)
