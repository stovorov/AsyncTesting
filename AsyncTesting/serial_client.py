""" Serial code client."""

import requests
import time


def process_response(response):
    """Models response processing."""
    time.sleep(0.001)


def run_serial(base_url, num_iter):
    urls = [base_url] * num_iter
    for url in urls:
        response = requests.get(url)
        process_response(response.text)

if __name__ == '__main__':
    delay = 2
    num_iter = 500
    base_url = 'http://127.0.0.1:5000/some_endpoint?delay={}'.format(delay)

    start = time.time()
    run_serial(base_url, num_iter)
    end = time.time()
    print('serial time: {}'.format(end - start))
