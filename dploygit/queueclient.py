class BuildQueueClient(object):
    """Client to the dploy-center build queue"""
    def __init__(self, uri):
        self._uri = uri

    def send_deploy_request(self, repository, app_file):
        return "hello"
