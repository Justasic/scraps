from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log
import sys, time, feedparser, tinyurl

""" RSS_FEEDS is a dictionary of dictionaries. The entry name is the feed
    name which will be announced in IRC. FeedLink is the link used to get
    feed information. LastFeed is the object of the last parsed feed.
"""
RSS_FEEDS = [
	{'Name': 'Drudge', 'FeedLink': 'http://www.drudgereportfeed.com/rss.xml', 'LastFeed': None},
	{'Name': 'Mojang', 'FeedLink': 'https://mojang.com/feed/', 'LastFeed': None},
]

class Bot(irc.IRCClient):
	nickname = "Feeds"
	realname = "Realtime RSS feed announcer"
	username = "RSSBot"
	versionName = "RSS Bot"
	versionNum = "1.0"
	versionEnv = "Python 2.7 on Linux"
	checkTimer = None

	def kickedFrom(self, channel, kicker, message):
		log.msg("%r was kicked from %r by %r: %r" % (self, channel, kicker, message))
		self.join(channel)

	def connectionMade(self):
		irc.IRCClient.connectionMade(self)
		log.startLogging(sys.stdout)
		log.msg("[connected at %s]" %
				time.asctime(time.localtime(time.time())))

	def connectionLost(self, reason):
		irc.IRCClient.connectionLost(self, reason)
		log.msg("[disconnected at %s]" %
			time.asctime(time.localtime(time.time())))

	# callbacks for events

	def signedOn(self):
		"""Called when bot has succesfully signed on to server."""
		self.join(self.factory.channel)

	def joined(self, channel):
		"""This will get called when the bot joins the channel."""
		log.msg("[I have joined %s]" % channel)
		# Start the feed checking ball rolling.
		self.CheckFeeds()

	def privmsg(self, user, channel, msg):
		"""This will get called when the bot receives a message."""
		user = user.split('!', 1)[0]
		log.msg("<%s> %s" % (user, msg))

		# Check to see if they're sending me a private message
		if channel == self.nickname:
			msg = "It isn't nice to whisper!  Play nice with the group."
			self.msg(user, msg)
			return

		# Otherwise check to see if it is a message directed at me
		if msg.startswith(self.nickname + ":"):
			msg = "%s: I am a log bot" % user
			self.msg(channel, msg)
			log.msg("<%s> %s" % (self.nickname, msg))

	def action(self, user, channel, msg):
		"""This will get called when the bot sees someone do an action."""
		user = user.split('!', 1)[0]
		log.msg("* %s %s" % (user, msg))

	# irc callbacks

	def irc_NICK(self, prefix, params):
		"""Called when an IRC user changes their nickname."""
		old_nick = prefix.split('!')[0]
		new_nick = params[0]
		log.msg("%s is now known as %s" % (old_nick, new_nick))


	# For fun, override the method that determines how a nickname is changed on
	# collisions. The default method appends an underscore.
	def alterCollidedNick(self, nickname):
		"""
		Generate an altered version of a nickname that caused a collision in an
		effort to create an unused related name for subsequent registration.
		"""
	        import random, time
        	random.seed(time.time())
		return nickname + '-%d' % random.randint(1, 999)

	def AnnounceFeed(self, feedname, feed):
		""" Announce a feed which supplies a feedparser instance """
		# Check if the old feed entries were already there in the new feed.
		# This will prevent re-announcements
		for e in feed.entries:
				url = tinyurl.create_one(e['link'])
				message = "[\0032%s\017]: %s \002\00310--\017 \00314%s\017" % (feedname['Name'], e['title'], url)
				self.msg(self.factory.channel, message.encode('utf-8'))

	def CheckFeeds(self):
		""" Check all the feeds we're supposed to check and see
		    if they need to be announced or not """
		for feed in RSS_FEEDS:
			log.msg("Checking feed \"%s\"..." % feed['Name'])
			if feed['LastFeed'] == None:
				f = feedparser.parse(feed['FeedLink'])
			else:
				lf = feed['LastFeed']
				if hasattr(lf, 'etag'):
					f = feedparser.parse(feed['FeedLink'], etag=lf.etag, modified=lf.modified)
				else:
					f = feedparser.parse(feed['FeedLink'], modified=lf.modified)

			# See if the feed has updates, announce them if it does.
			if f.status == 200:
				log.msg("Feed %s has %d updates." % (feed['Name'], len(f.entries)))
				f = feedparser.parse(feed['FeedLink'])
				# Announce the feed only if the previous feed was there
				if feed['LastFeed'] != None:
					self.AnnounceFeed(feed, f)
                		else:
					log.msg("Skipping feed %s because it's never been announced before." % (feed['Name']))
				# update Last feed last so we can use it in AnnounceFeed.
				feed['LastFeed'] = f

		# Call back later to check for feeds.
		self.checkTimer = reactor.callLater(15, self.CheckFeeds)


class BotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channel, nick = "Feeds", ident = "RSSBot", real = "RSS Feeds bot"):
        self.channel = channel
        self.ident = ident
        self.nick = nick
        self.real = real

    def buildProtocol(self, addr):
        p = Bot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


#if __name__ == "__main__":
#	log.startLogging(sys.stdout)
#	BotFactory("#Computers", "15.0.1.10")
#	reactor.run()
