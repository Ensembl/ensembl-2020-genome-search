import requests, urllib.parse as urlparse


class EnsemblRest(object):

    """ Simple REST class. Add/update code as it evolves"""

    def __init__(self):
        pass

    def do_rest_request(self, **kwargs):

        if 'url' not in kwargs:
            raise Exception('No URL provided')
        else:
            query_url = kwargs['url']

        if 'query_params' in kwargs:
            query_url = kwargs['url'] + '?' + urlparse.urlencode(kwargs['query_params'])

        if 'method' in kwargs and kwargs['method'] == 'POST':
            raise Exception('POST not supported yet')
        else:
            rest_response = self.__get(query_url)

        return rest_response

    def __get(self, url):
        print("Querying {}".format(url))
        rest_response = requests.get(url, headers={'content-type': 'application/json'})
        return rest_response





