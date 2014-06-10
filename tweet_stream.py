from threading import Thread
from collections import deque  # No locking for append() and popleft()
from twython import TwythonStreamer
from requests.exceptions import ChunkedEncodingError


class TwitterStream(TwythonStreamer):

    def __init__(self, consumer_key, consumer_secret, token, token_secret, tqueue):
        self.tweet_queue = tqueue
        super(TwitterStream, self).__init__(consumer_key, consumer_secret, token, token_secret)

    def on_success(self, data):
        if 'text' in data:
            self.tweet_queue.append(data)

    def on_error(self, status_code, data):
        print(status_code)
        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()


def stream_tweets(tweets_queue):
    # Input your credentials below
    consumer_key = ''
    consumer_secret = ''
    token = ''
    token_secret = ''
    try:
        stream = TwitterStream(consumer_key, consumer_secret, token, token_secret, tweets_queue)
        # You can filter on keywords, or simply draw from the sample stream
        #stream.statuses.filter(track='twitter', language='en')
        stream.statuses.sample(language='en')
    except ChunkedEncodingError:
        # Sometimes the API sends back one byte less than expected which results in an exception in the
        # current version of the requests library
        stream_tweets(tweet_queue)


def process_tweets(tweets_queue):
    while True:
        if len(tweets_queue) > 0:
            #  Do something with the tweets
            print(tweets_queue.popleft())

if __name__ == '__main__':

    tweet_queue = deque()

    tweet_stream = Thread(target=stream_tweets, args=(tweet_queue,), daemon=True)
    tweet_stream.start()

    process_tweets(tweet_queue)