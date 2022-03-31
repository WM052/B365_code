import requests
import uuid
import json
import ipaddress
import sys
from netaddr import IPNetwork,IPAddress

count = 0
testcount = 0
#######################################
#This section requests info from MS and displays number of sections with IP addresses



x = uuid.uuid4()
y = str(x)
call = requests.get('https://endpoints.office.com/endpoints/worldwide?ClientRequestID='+y)

if call.status_code> 199 and call.status_code<300:
    print("\nStatus code good! Proceed\n")
elif  not call.status_code> 199 and  not call.status_code<300:
    print("Status code error occured! Unable to retrieve information currently. Please try again later!")
    exit()
else:
    ("Code error occured, please close and review code or wait a few minutes and try again")

data = json.loads(call.text)
userip=""


repeat = True

while repeat == True:

    while True:
        userip = input("Please enter which IP you are seeing dropped, or type quit/q to exit: ")
        if userip.lower().startswith("q"):
            print("Exiting!")
            exit()
        else:
            try:
                print(ipaddress.ip_address(userip))
                print("Valid IP!\n")
                break
            except ValueError:
                print("*" * 50)
                print("IP not valid, please retry!\n")
                
    matchipadd = IPAddress(userip)

    print("\nIP validity checked passed, checking for relevant MS Services\n")
    print("*" * 50)
    stringlist = []
    iplist =[]
    print("Range of MS Services with Active IP's: \n")
    for service in data:
        for subnet in (service.get('ips',[])):
            if IPAddress(matchipadd) in IPNetwork(subnet):
                print("Service found!")            
                print("Service area: ",service.get('serviceArea'))
                print("IP Network: ",subnet)
                print("TCP Ports: ", service.get('tcpPorts'))
                print("URL's to whitelist for DNS resolution-capable systems: ", service.get('urls'),"\n")
                areatemp = service.get('serviceArea',[])
                subnettemp = subnet
                porttemp = service.get('tcpPorts',[])
                urltemp = service.get('urls',[])
                stringlist.extend([areatemp,subnettemp,porttemp,urltemp])
                print("*" * 50)
                count += 1
                break
                
    if count == 0:
        print("*" * 50)
        print("\nNo matching MS Services!\n")

    
    jsonlist=json.dumps(stringlist)
    print("\njson list: \n",json.dumps(stringlist,indent=4))

