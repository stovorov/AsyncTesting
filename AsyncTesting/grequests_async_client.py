"""Asynchronous code using grequests."""

import grequests
import time


def process_response(response):
    """Models response processing."""
    time.sleep(0.001)


def run_asynced(base_url, num_iter):
    urls = [base_url] * num_iter
    response_futures = (grequests.get(u) for u in urls)
    response = grequests.imap(response_futures, size=100)
    [process_response(r.text) for r in response]

if __name__ == '__main__':
    delay = 2   # sleep time on server side in ms
    num_iter = 500
    base_url = 'http://127.0.0.1:5000/some_endpoint?delay={}'.format(delay)

    start = time.time()
    run_asynced(base_url, num_iter)
    end = time.time()
    print('grequests time: {}'.format(end - start))
