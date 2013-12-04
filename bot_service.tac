import os
from twisted.application import service, internet
from twisted.web import static, server
import Bot

channel = ["#Computers", "#News"]
#channel = "#Test"
host = "15.0.1.10"
port = 6667

application = service.Application("RSSBot")

botservice = Bot.BotFactory(channel)

service = internet.TCPClient(host, port, botservice)
service.setServiceParent(application)
