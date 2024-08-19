import re

from flask import Blueprint, render_template, request
import ipinfo
import subprocess
import os

search_bp = Blueprint("search", __name__)

"""Setting Environment variables"""
access_token = os.getenv("ACCESS_TOKEN")
map_img_token = os.getenv("STATIC_MAP_IMG")


@search_bp.route("/search", methods=['GET', 'POST'])
def search_ip():

    if request.method == 'POST':
        ipaddr = request.form.get('ipaddr')  # Get the IP address from the form

        # Validating IP address from the form
        ip_pattern = r"\b((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\b"
        match_pattern = re.match(ip_pattern, ipaddr)
        if ipaddr.isalpha() == True or not match_pattern:
            return render_template("404.html")

        # If everything is Okay then passing the ip address to the handler
        handler = ipinfo.getHandler(access_token)
        details = handler.getDetails(ipaddr)

        try:
            # To check whether the VPN is connected or not
            def show_status():
                host = details.ip
                ping = subprocess.Popen(["ping.exe", "-n", "1", "-w", "1", host], stdout=subprocess.PIPE).communicate()[
                    0]
                if ('unreachable' in str(ping)) or ('timed' in str(ping)) or ('failure' in str(ping)):
                    ping_chk = 0
                else:
                    ping_chk = 1

                if ping_chk == 1:
                    return "Protected"
                else:
                    return "Unprotected"

            status = show_status()

            # Checking if 'org' attribute exists
            if hasattr(details, 'org'):
                isp = details.org[8:].strip()  # Strip the first 8 characters
            else:
                isp = "Unknown ISP"

            # Location of ISP
            location = f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/pin-l+ff0000({details.longitude},{details.latitude})/{details.longitude},{details.latitude},05.90,20,60/1000x400?access_token={map_img_token}"

            # Render the template
            return render_template("index.html", yourISP=isp, city=details.city,
                                   country=details.country_name, ip=details.ip, location=location,
                                   region=details.region, status=status)

        # If other exception occurs render error page
        except ConnectionError:
            return render_template("404.html")
