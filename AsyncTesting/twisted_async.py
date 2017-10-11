"""Asynchronous code using twisted framework."""

import treq
from twisted.internet import reactor, defer, task
import time


def process_response(response):
    """Models response processing."""
    for status, content in response:
        print(content)
    time.sleep(0.001)


def create_callbacks(urls):
    deffered = []
    for url in urls:
        d = treq.get(url)
        d.addCallback(treq.content)
        deffered.append(d)
    return defer.DeferredList(deffered)


def run_asynced(base_url, num_iter):
    urls = [base_url] * num_iter
    future_results = create_callbacks(urls)
    future_results.addCallback(process_response)


if __name__ == '__main__':
    delay = 2   # sleep time on server side in ms
    num_iter = 500
    base_url = 'http://127.0.0.1:5000/some_endpoint?delay={}'.format(delay)

    start = time.time()
    task.react(run_asynced(base_url, num_iter))
    end = time.time()
    print('twisted time: {}'.format(end - start))
