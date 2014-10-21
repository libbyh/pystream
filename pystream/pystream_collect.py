import sys
import tweepy
import os
import codecs
import ConfigParser
import io
import time
import json
from HTMLParser import HTMLParser

@classmethod
def parse(cls, api, raw):
	status = cls.first_parse(api, raw)
	setattr(status, 'json', json.dumps(raw))
	return status

tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse

api = None
auth = None

def init_auth():
    global api
    global auth
    auth = tweepy.OAuthHandler(os.environ.get('TW_CONSUMER_KEY'), os.environ.get('TW_CONSUMER_SECRET'))
    auth.set_access_token(os.environ.get('TW_ACCESS_TOKEN'), os.environ.get('TW_ACCESS_TOKEN_SECRET'))
    api = tweepy.API(auth)
    
def get_config():
    global config
    config = ConfigParser.RawConfigParser()

    if 'PYSTREAM_CFG' in os.environ:
        config.read(os.environ['PYSTREAM_CFG'])
    else:
        config.read('~/.pystream')

def make_output_file(id):
    return config.get('data', 'path') + '/' + config.get('data', 'jsons') + '/' + str(id) + '.json'

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        outf = io.open(make_output_file(status.id), mode='wt', encoding='utf8')
        outf.write(json.dumps(status.json, ensure_ascii=False, encoding='utf8'))
        outf.flush()
        outf.close()

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

def main():
    get_config()
    
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)

    # make directories for storing data
    # path = config.get('data', 'path')
    # for subdir in 'jsons':
        # try:
            # os.makedirs(path + '/' + config.get('data', subdir))
        # except:
            # print "couldn't make directory"
            # pass

    l = CustomStreamListener()
    init_auth()
    hashtags = ['#gamergate','#stopgamergate2014']
    stream = tweepy.streaming.Stream(auth, l)
    stream.filter(track=hashtags)
    
if __name__ == '__main__':
    main()