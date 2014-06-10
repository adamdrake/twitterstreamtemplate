twitterstreamtemplate
=====================

A simple starting point for stream processing experimentation using the Twitter streaming API.

This is only a skeleton and does not include, tests, logging, etc.

The stream is consumed from a separate thread and stream items placed into a deque.

Besides the standard library, twython is the only dependency.

Tested with Python 3.4