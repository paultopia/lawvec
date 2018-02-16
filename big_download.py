import requests, concurrent.futures, time


class FailedRequest(object):
    def __init__(self, type_of_failure, details):
        self.type = type_of_failure
        self.message = details


def __download(url, headers, delay, timeout):
    filename = url.rpartition("/")[-1]
    try:
        time.sleep(delay)
        response = requests.get(url, headers=headers, timeout=timeout, stream=True)
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        response.close()
        return filename
    except Exception as e:
        if response:
            response.close()
        return FailedRequest("thrown", str(e))


def parallel_download(urls, maxthreads=4, headers=None, delay=0, timeout=5):
    """
    urls: list of URLS to download
    maxthreads: maximum number of threads to use
    header: dict of headers for each request
    delay: time in seconds to wait before firing each request (to avoid rate-limiting servers)
    timeout: timeout to pass directly to request (is timeout for failed connections, not for entire content---see caveat in requests docs)

    Returns: tuple: list of successful downlads by url (unordered), list of FailedRequest (unordered).  
    """
    successes = []
    failures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=maxthreads) as executor:
        results = [executor.submit(__download, url, headers, delay, timeout) for url in urls]
        for future in concurrent.futures.as_completed(results):
            res = future.result()
            if isinstance(res, FailedRequest):
                failures.append(res)
                print(res.type)
                print(res.message)
            else:
                url = res
                successes.append(url)
        return successes, failures
