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

    def showISP():
        return details.org[8:]

    dataISP = showISP()

    def showISPCountry():
        return details.city

    cityISP = showISPCountry()

    def showISPCountry():
        return details.country_name

    countryISP = showISPCountry()

    def showIP():
        return details.ip

    showIP = showIP()

    def showlanglong():
        return f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/pin-l+ff0000({details.longitude},{details.latitude})/{details.longitude},{details.latitude},05.90,20,60/1000x400?access_token={map_img_token}"

    langlong = showlanglong()

    def showISPregion():
        return details.region

    showregion = showISPregion()

    # To check whether the VPN is connected or not
    def showStatus():
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

    showstatus = showStatus()
    return render_template("index.html", yourISP=dataISP, city=cityISP, country=countryISP, ip=showIP,
                           location=langlong, region=showregion, status=showstatus)


@app.route("/share")
def share():
    return "<h1>I am a sharer.</h1>"


if __name__ == '__main__':
    app.run(debug=True)
