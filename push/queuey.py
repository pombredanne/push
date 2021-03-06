import json

import requests


class QueueyException(Exception):
    """Exception raised if queuey does not respond with a 200."""


class Queuey(object):

    def __init__(self, url, application_key):
        self.url = url[:-1] if url.endswith('/') else url
        self.application_key = application_key
        self.headers = {'Authorization': 'Application ' + self.application_key}

    def request(self):
        return requests.session(headers=self.headers,
                                hooks={'response': self.json_response})

    def json_response(self, response):
        """Turn a response into JSON or raise an error."""
        if response.status_code in (200, 201):
            try:
                response.json = json.loads(response.content)
            except Exception:
                raise QueueyException(response)
        else:
            raise QueueyException(response)

    def new_queue(self, queue_name=None):
        data = {'queue_name': queue_name} if queue_name else None
        response = self.request().post(self.url, data=data)
        return response.json['queue_name']

    def delete_queue(self, queue):
        response = self.request().delete(self.url + '/' + queue)
        return response.json

    def new_message(self, queue, message):
        response = self.request().post(self.url + '/' + queue,
                                       message)
        return response.json

    def get_messages(self, queue, since=None, limit=None, order=None):
        keys = ('since', 'limit', 'order')
        qs = dict((k, v) for k, v in zip(keys, (since, limit, order)) if v)
        response = self.request().get(self.url + '/' + queue,
                                      params=qs)
        return response.json['messages']
