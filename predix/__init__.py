"""
package predix
By: Adi Suresh
"""
import urllib2
import socket
import os


def get_proxy():
    ip = socket.gethostbyname(socket.gethostname())
    if ip[0:2] == '3.':
        return 'http://PITC-Zscaler-Americas-Alpharetta3pr.proxy.corporate.ge.com:80'
    else:
        return None
