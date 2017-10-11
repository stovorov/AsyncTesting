"""Asynchronous code using tornado framework."""

import time
from tornado import ioloop
from tornado.httpclient import AsyncHTTPClient
from tornado import gen

from functools import partial

AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient', max_clients=100)


def process_response(response):
    """Models response processing."""
    time.sleep(0.001)


@gen.coroutine
def run_asynced(base_url, num_iter):
    http_client = AsyncHTTPClient()
    urls = [base_url] * num_iter
    responses = yield [http_client.fetch(url) for url in urls]
    [process_response(r.body) for r in responses]
    raise gen.Return()


if __name__ == '__main__':
    delay = 2   # sleep time on server side in ms
    num_iter = 500
    base_url = 'http://127.0.0.1:5000/some_endpoint?delay={}'.format(delay)

    _ioloop = ioloop.IOLoop.instance()
    run_func = partial(run_asynced, base_url, num_iter)
    start = time.time()
    res = _ioloop.run_sync(run_func)
    end = time.time()
    print('tornado time: {}'.format(end - start))
