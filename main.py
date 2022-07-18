from flask import Flask, render_template
import ipinfo
import subprocess
import os

app = Flask(__name__)

access_token = os.getenv("ACCESS_TOKEN")
map_img_token = os.getenv("STATIC_MAP_IMG")


@app.route("/")
def main():
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails()

    def show_isp():
        return details.org[8:]

    data_isp = show_isp()

    def show_isp_Country():
        return details.city

    city_isp = show_isp_Country()

    def show_isp_Country():
        return details.country_name

    country_isp = show_isp_Country()

    def show_ip():
        return details.ip

    ip = show_ip()

    def showlanglong():
        return f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/pin-l+ff0000({details.longitude},{details.latitude})/{details.longitude},{details.latitude},05.90,20,60/1000x400?access_token={map_img_token}"

    langlong = showlanglong()

    def show_isp_region():
        return details.region

    show_region = show_isp_region()

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
    return render_template("index.html", yourISP=data_isp, city=city_isp, country=country_isp, ip=ip,
                           location=langlong, region=show_region, status=status)


@app.route("/share/<ip>")
def share(ip):
    # print(ip)
    # To return the whole page as main route
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails(ip)

    def show_isp():
        return details.org[8:]

    data_isp = show_isp()

    def show_isp_Country():
        return details.city

    city_isp = show_isp_Country()

    def show_isp_Country():
        return details.country_name

    country_isp = show_isp_Country()

    def show_ip():
        return details.ip

    ip = show_ip()

    def showlanglong():
        return f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/pin-l+ff0000({details.longitude},{details.latitude})/{details.longitude},{details.latitude},05.90,20,60/1000x400?access_token={map_img_token}"

    langlong = showlanglong()

    def show_isp_region():
        return details.region

    show_region = show_isp_region()

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
    return render_template("shareip.html", yourISP=data_isp, city=city_isp, country=country_isp, ip=ip,
                           location=langlong, region=show_region, status=status)


if __name__ == '__main__':
    app.run(debug=True)
