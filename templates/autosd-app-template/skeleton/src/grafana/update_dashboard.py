#!/usr/bin/env python3

import argparse
import json
import sys
import requests

# If you need to edit the dashboard:
# - Enable login in files/grafana.ini
# - Start graphana (using build.sh)
# - Log in using admin/admin
# - Make the changes you want to see on the dashboard
# - Retrieve the update JSON for the dashboard:
#   curl http://admin:admin@localhost:3000/api/dashboards/uid/pcp-vector-checklist |python -m json.tool
# - Save it into: files/new.json

base_url = "http://admin:admin@localhost:3000/api"
dashboard_uid = "pcp-vector-checklist"


def main():
    """ Main function """
    url = f"{base_url}/dashboards/uid/{dashboard_uid}"
    req = requests.get(url)
    data = req.json()

    with open("files/new.json") as stream:
        data2 = json.load(stream)

    output = data
    del(output["meta"])
    output["dashboard"]["panels"] = data2["dashboard"]["panels"]
    output["overwrite"] = True
    output["message"] = "Updated panels"

    print("===")
    url = f"{base_url}/dashboards/db"
    print(json.dumps(output, indent=4))
    headers = {"Content-Type": "application/json"}
    req = requests.post(url, data=json.dumps(output), headers=headers)
    print(req.url)
    print(req.ok)
    print(req.text)

if __name__ == "__main__":
    main()
    exit(0)
