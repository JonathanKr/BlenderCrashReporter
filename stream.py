import psutil
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import qrcode
from PIL import Image
import subprocess as sb
from sys import platform

hostName = "0.0.0.0"
serverPort = 8000

def get_ipv4(): #get Windows IPv4
    con_ipv4_array = []
    ipv4 = []
    result = sb.run(['ipconfig'], stdout=sb.PIPE)
    result = str(result.stdout.decode('utf-8'))
    to_process = result
    for i in range (result.count("IPv4")):
        contains_ipv4 = to_process[:to_process.find("Subnet Mask")]
        to_process = to_process.replace(contains_ipv4+"Subnet Mask","")
        con_ipv4_array.append(contains_ipv4)
    for i in range (len(con_ipv4_array)):
        if ("Ethernet adapter Ethernet" in con_ipv4_array[i]):
            con_ipv4 = con_ipv4_array[i][con_ipv4_array[i].find("IPv4"):]
            con_ipv4 = con_ipv4[:con_ipv4.find("Subnet Mask")]
            ipv4.append(con_ipv4[con_ipv4.find(":"):].replace(": ","").replace(" ",""))
        elif ("Wireless LAN adapter" in con_ipv4_array[i]):
            con_ipv4 = con_ipv4_array[i][con_ipv4_array[i].find("IPv4"):]
            con_ipv4 = con_ipv4[:con_ipv4.find("Subnet Mask")]
            ipv4.append(con_ipv4[con_ipv4.find(":"):].replace(": ","").replace(" ",""))
    return ipv4

class ReportServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Report Server</title><meta name='viewport' content='width=device-width, initial-scale=1'></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<button id='checkButton'>Check</button><br>", "utf-8"))
        self.wfile.write(bytes("<script>function reloadCheck(){location.reload()}document.getElementById('checkButton').addEventListener('click',reloadCheck);</script>", "utf-8"))
        self.wfile.write(bytes("CPU: " + str(psutil.cpu_percent(interval=1)) + "%<br>RAM: " + str(psutil.virtual_memory().percent) + "%<br>", "utf-8"))
        isBlenderRunning = False
        for p in psutil.process_iter():
            if "blender" in p.name() or "Blender" in p.name():
                isBlenderRunning = True
        if isBlenderRunning:
            self.wfile.write(bytes("Blender is running", "utf-8"))
        else:
            self.wfile.write(bytes("Blender prob. crashed", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), ReportServer)
    if platform == "win32":
        qrCodeImg = qrcode.make("http://"+get_ipv4()[0]+":"+str(serverPort))
        qrCodeImg.show()
    else:
        ipv4Input = str(input("Your IPv4 Adress: "))
        qrCodeImg = qrcode.make("http://"+ipv4Input+":"+str(serverPort))
        qrCodeImg.show()
    print("Server started.")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")