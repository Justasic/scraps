import time, sys, os, json, tinyurl
from twisted.python import log

class BasicUser():
	def __init__(self, user):
		self.nick = user.split('!', 1)[0]
		self.real = user.split('!', 1)[1].split('@', 1)[0]
		self.user = user.split('!', 1)[1].split('@', 1)[1]

class CommandHandler():
	""" This class handles all the commands sent in private messages """

	def __init__(self, bot, command, user):
		self.command = command
		self.bot = bot
		self.user = BasicUser(user)
		self.COMMANDS = [
			{"addfeed": self.HandleAddFeed, "desc": "Add an RSS feed to announce", "syntax": "\037name\037 \037url\037"},
			{"delfeed": self.HandleDelFeed, "desc": "Delete an RSS feed", "syntax": "\037name\037"},
			{"listfeeds": self.HandleListFeed, "desc": "List all feeds"},
			{"help": self.HandleHelp, "desc": "List help for all available commands"},
		]
		self.HandleCommand()

	def reply(self, msg):
		log.msg("{Notice %s} %s" % (self.user.nick, msg))
		self.bot.notice(self.user.nick, msg.encode('utf-8'))

	def HandleCommand(self):
		params = self.command.strip().split()
		command = params[0].lower()

		for c in self.COMMANDS:
			if command in c:
				try:
					c[command](params)
				except IndexError:
					self.reply("Invalid Parameters")
					self.reply("Syntax: \002%s\002 %s" % (command, c['syntax']))
				return
		
		self.reply("Unknown command \002%s\002. Type \"/msg %s HELP\" for help." % (command, self.bot.nickname))

	def HandleHelp(self, params):
		for c in self.COMMANDS:
			self.reply("%-14s %s" % (c.keys()[0].upper(), c['desc']))

	def HandleAddFeed(self, params):
		feedname = params[1]
		feedurl = params[2]

		db = self.bot.factory.database.getDB()
		if 'Feeds' not in db:
			db['Feeds'] = []

		db['Feeds'].append({'Name': feedname, 'FeedLink': feedurl, 'LastFeed': None})
		self.bot.factory.database.save()
		self.reply("Feed \002%s\002 added." % feedname)

	def HandleDelFeed(self, params):
		feedname = params[1]
		db = self.bot.factory.database.getDB()

		for i, f in enumerate(db['Feeds']):
			if f['Name'] == feedname:
				del db['Feeds'][i]
				self.bot.factory.database.save()
				self.reply("Feed \002%s\002 deleted." % feedname)
				return

		self.reply("Feed \002%s\002 does not exist." % feedname)

	def HandleListFeed(self, params):
		db = self.bot.factory.database.getDB()

		self.reply("%-14s %s" % ("Name", "URL"))
		self.reply("-------------------")
		for f in db['Feeds']:
			self.reply("%-14s %s" % (f['Name'], f['FeedLink']))

