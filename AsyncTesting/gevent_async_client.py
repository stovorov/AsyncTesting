"""Asynchronous code using gevent."""

import gevent
import gevent.monkey
import requests
import time

try:
    from gevent.coros import Semaphore
except ImportError:
    from gevent.lock import Semaphore

gevent.monkey.patch_all()


def process_response(response):
    """Models response processing."""
    time.sleep(0.001)


def download(url, semaphore):
    with semaphore:
        data = requests.get(url)
        return data.text


def chunked_requests(urls, chunk_size=100):
    semaphore = Semaphore(chunk_size)
    reqs = [gevent.spawn(download, url, semaphore) for url in urls]
    for response in gevent.iwait(reqs):
        yield response  # yields greenlet object


def run_asynced(base_url, num_iter):
    urls = [base_url] * num_iter
    response_futures = chunked_requests(urls)
    [process_response(r.value) for r in response_futures]


if __name__ == '__main__':
    delay = 2   # sleep time on server side in ms
    num_iter = 500
    base_url = 'http://127.0.0.1:5000/some_endpoint?delay={}'.format(delay)

    start = time.time()
    run_asynced(base_url, num_iter)
    end = time.time()
    print('gevent time: {}'.format(end - start))
