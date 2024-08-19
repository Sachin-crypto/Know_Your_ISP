from flask import Blueprint, render_template
import ipinfo
import subprocess
import os
from appwrite.client import Client
from appwrite.id import ID
from appwrite.services.databases import Databases
from appwrite.query import Query

home_bp = Blueprint("home", __name__)

"""Setting Environment variables"""
access_token = os.getenv("ACCESS_TOKEN")
map_img_token = os.getenv("STATIC_MAP_IMG")
project_id = os.getenv("PROJECT_ID")
api_key = os.getenv("API_KEY")
database_id = os.getenv("DATABASE_ID")
collection_id = os.getenv("COLLECTION_ID")

""" Appwrite Credential """
# Initialize the Appwrite client
client = Client()
# Appwrite API endpoint
client.set_endpoint('https://cloud.appwrite.io/v1')
# Appwrite project ID
client.set_project(project_id)
# Appwrite API key
client.set_key(api_key)

# Create a new instance of the Database service
databases = Databases(client)
# Database ID
db_id = database_id
# For generating unique document ID
dc_id = ID.unique()
# Collection ID where we want to add data
collection_id = collection_id
"""Ends here"""


@home_bp.route("/")
def main():
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails()

    # To check whether the VPN is connected or not
    def show_status():
        host = details.ip
        ping = subprocess.Popen(["ping.exe", "-n", "1", "-w", "1", host], stdout=subprocess.PIPE).communicate()[0]
        if ('unreachable' in str(ping)) or ('timed' in str(ping)) or ('failure' in str(ping)):
            ping_chk = 0
        else:
            ping_chk = 1

        if ping_chk == 1:
            return "Protected"
        else:
            return "Unprotected"

    status = show_status()

    # Getting the document if exists for the specified IP otherwise add to db
    try:
        ip = details.ip
        # Check document for existing data
        entry = databases.list_documents(
            database_id=db_id,
            collection_id=collection_id,
            queries=[
                Query.search("ip", ip)  # 1st arg - attribute name and 2nd arg - Query to search
            ]
        )

        # If found any data then fetch from db and render
        if entry['documents']:
            data = entry['documents'][0]
            return render_template("index.html", yourISP=data['isp'].strip(), city=data['city'],
                                   country=data['country'], ip=data['ip'], location=data['location'],
                                   region=data['region'], status=status)

        # If data not found then add to db and render
        else:
            # Data as a dictionary
            data = {
                'isp': details.org[8:],
                'ip': details.ip,
                'city': details.city,
                'region': details.region,
                'country': details.country_name,
                'location': f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/pin-l+ff0000({details.longitude},{details.latitude})/{details.longitude},{details.latitude},05.90,20,60/1000x400?access_token={map_img_token}"
            }
            global dc_id
            response = databases.create_document(
                database_id=db_id,
                document_id=dc_id,
                collection_id=collection_id,
                data=data
            )

            return render_template("index.html", yourISP=response['isp'].strip(), city=response['city'],
                                   country=response['country'], ip=response['ip'], location=response['location'],
                                   region=response['region'], status=status)

    # If other exceptions occurs then render error page
    except ConnectionError:
        return render_template("404.html")
