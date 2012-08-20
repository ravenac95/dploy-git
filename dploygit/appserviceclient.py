import requests
from urlparse import urljoin


class AppServiceClient(object):
    request_mimetype = 'application/json'

    def __init__(self, base_uri):
        self._base_uri = base_uri

    def start_new_release(self, git_repo, release_note):
        data = dict(release_note=release_note)
        return self._releases_request('post', git_repo, 'start-new', data)

    def commit_release(self, git_repo, release):
        return self._releases_request('post', git_repo, 'commit', data=release)

    def _releases_request(self, method, git_repo, action, data=None):
        return self._make_request(method, git_repo.name,
                'releases', action, data=data)

    def _make_request(self, method, *joins, **kwargs):
        headers = {'content-type': self.request_mimetype}
        kwargs['headers'] = headers
        complete_uri = self._make_complete_uri(*joins)
        response = requests.request(method, complete_uri, **kwargs)
        return response.json

    def _make_complete_uri(self, *joins):
        service_endpoint = '/'.join(joins)
        return urljoin(self._base_uri, service_endpoint)
