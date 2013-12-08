from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log
import sys, time, feedparser, tinyurl

""" RSS_FEEDS is a dictionary of dictionaries. The entry name is the feed
    name which will be announced in IRC. FeedLink is the link used to get
    feed information. LastFeed is the object of the last parsed feed.
"""
RSS_FEEDS = [
	#{'Name': 'Drudge', 'FeedLink': 'http://www.drudgereportfeed.com/rss.xml', 'LastFeed': None},
	{'Name': 'Drudge', 'FeedLink': 'http://feeds.feedburner.com/drudgesiren/oGpG?format=xml', 'LastFeed': None},
	{'Name': 'Mojang', 'FeedLink': 'https://mojang.com/feed/', 'LastFeed': None},
]

def feed_modified_date(feed):
    # this is the last-modified value in the response header
    # do not confuse this with the time that is in each feed as the server
    # may be using a different timezone for last-resposne headers than it
    # uses for the publish date

    modified = feed.get('modified')
    if modified is not None:
        return modified

    return None

def max_entry_date(feed):
    entry_pub_dates = (e.get('updated_parsed') for e in feed.entries)
    entry_pub_dates = tuple(e for e in entry_pub_dates if e is not None)

    if len(entry_pub_dates) > 0:
        return max(entry_pub_dates)

    return None

def entries_with_dates_after(feed, date):
    response = []
    for entry in feed.entries:
        if entry.get('updated_parsed') > date:
            response.append(entry)

    return response

class Bot(irc.IRCClient):
	nickname = "Feeds"
	realname = "Realtime RSS feed announcer"
	username = "RSSBot"
	versionName = "RSS Bot"
	versionNum = "1.0"
	versionEnv = "Python 2.7 on Linux"
	checkTimer = None
	isConnected= False

	def kickedFrom(self, channel, kicker, message):
		log.msg("%r was kicked from %r by %r: %r" % (self, channel, kicker, message))
		self.join(channel)

	def connectionMade(self):
		irc.IRCClient.connectionMade(self)
		log.startLogging(sys.stdout)
		self.isConnected = True
		log.msg("[connected at %s]" %
				time.asctime(time.localtime(time.time())))

	def connectionLost(self, reason):
		irc.IRCClient.connectionLost(self, reason)
		self.isConnected = False
		log.msg("[disconnected at %s]" %
			time.asctime(time.localtime(time.time())))

	# callbacks for events

	def signedOn(self):
		"""Called when bot has succesfully signed on to server."""
		for channel in self.factory.channel:
			self.join(channel)
		reactor.callInThread(self.CheckFeeds)
		#self.CheckFeeds()

	def joined(self, channel):
		"""This will get called when the bot joins the channel."""
		log.msg("[I have joined %s]" % channel)

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
		for e in feed:
			url = tinyurl.create_one(e['link'])
			message = "[\0032%s\017]: %s \002\00310--\017 \00314%s\017" % (feedname['Name'], e['title'], url)
			for channel in self.factory.channel:
				self.msg(channel, message.encode('utf-8'))

	def CheckFeeds(self):
		""" Check all the feeds we're supposed to check and see
		    if they need to be announced or not """
		while self.isConnected:
			for feed in RSS_FEEDS:
				#log.msg("Checking feed \"%s\"..." % feed['Name'])
				if feed['LastFeed'] is None:
					f = feedparser.parse(feed['FeedLink'])
				else:
					etag = feed['LastFeed'].get('etag', None)
					modified = feed_modified_date(feed['LastFeed'])
					#log.msg("Feed %s modified %s (etag: %s)" % (feed['Name'], modified, etag))
					f = feedparser.parse(feed['FeedLink'], etag=etag, modified=modified)

				if len(f.entries) > 0:
					if feed['LastFeed'] is None:
						log.msg("Feed %s has not been announced before, skipping..." % feed['Name'])
						feed['LastFeed'] = f
						continue

					log.msg("Feed %s has possible new entries..." % feed['Name'])
					prev_max_date = max_entry_date(f)
					entries = entries_with_dates_after(f, prev_max_date)

					for e in f.entries:
						if e not in feed['LastFeed'].entries:
							entries.append(e)

					log.msg("%d new entries!" % len(entries))

					if len(entries) > 0:
						log.msg("Feed %s has %d new entries!" % (feed['Name'], len(entries)))
						#self.AnnounceFeed(feed, entries)
						reactor.callFromThread(self.AnnounceFeed, feed, entries)
						feed['LastFeed'] = f
					else:
						log.msg("Feed %s has no etag or modified support..." % feed['Name'])
			time.sleep(15)
			# Call back later to check for feeds.
			#self.checkTimer = reactor.callLater(15, self.CheckFeeds)


class BotFactory(protocol.ClientFactory):
    """A factory for RSSBots.

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
