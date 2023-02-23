#coding:utf8
import gazu


class LogIn:
    def __init__(self):
        gazu.client.set_host("http://192.168.3.116/api")
        gazu.log_in("pipeline@rapa.org", "netflixacademy")
