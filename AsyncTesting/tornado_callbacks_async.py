"""Asynchronous code using tornado framework with callbacks."""

from tornado import ioloop
from tornado.httpclient import AsyncHTTPClient

from functools import partial
import time

AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient', max_clients=100)


def process_response(response):
    """Models response processing."""
    time.sleep(0.001)


def fetch_urls(urls, callback):
    http_client = AsyncHTTPClient()
    responses = []

    def _finish_fetch_urls(result):
        responses.append(result)
        if len(responses) == len(urls):
            callback(responses)

    for url in urls:
        http_client.fetch(url, callback=_finish_fetch_urls)


def _finish_asynced(responses, callback):
    process_response([resp for resp in responses])
    callback()


def run_asynced(base_url, num_iter, callback=None):
    callback_passthrou = partial(_finish_asynced, callback=callback)
    urls = [base_url] * num_iter
    fetch_urls(urls, callback_passthrou)


if __name__ == '__main__':
    delay = 2   # sleep time on server side in ms
    num_iter = 500
    base_url = 'http://127.0.0.1:5000/some_endpoint?delay={}'.format(delay)

    _ioloop = ioloop.IOLoop.instance()
    _ioloop.add_callback(run_asynced, base_url, num_iter, _ioloop.stop)
    start = time.time()
    _ioloop.start()
    end = time.time()
    print('tornado callbacks time: {}'.format(end - start))
