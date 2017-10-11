"""Asynchronous code using asyncio."""

import asyncio
import aiohttp
import time


def process_response(response):
    """Models response processing."""
    time.sleep(0.001)


def chunked_http_client(num_chunks):
    semaphore = asyncio.Semaphore(num_chunks)

    @asyncio.coroutine
    def http_get(url):
        nonlocal semaphore
        with (yield from semaphore):
            response = yield from aiohttp.request('GET', url)
            body = yield from response.content.read()
            yield from response.wait_for_close()
        return body
    return http_get


def run_asynced(base_url, num_iter):
    urls = [base_url] * num_iter
    http_client = chunked_http_client(100)
    tasks = [http_client(url) for url in urls]
    for future in asyncio.as_completed(tasks):
        data = yield from future
        process_response(data)


if __name__ == '__main__':
    delay = 2   # sleep time on server side in ms
    num_iter = 500
    base_url = 'http://127.0.0.1:5000/some_endpoint?delay={}'.format(delay)
    loop = asyncio.get_event_loop()
    start = time.time()
    loop.run_until_complete(run_asynced(base_url, num_iter))
    end = time.time()
    print('asyncio time: {}'.format(end - start))
