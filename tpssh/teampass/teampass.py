import requests
from collections import OrderedDict
from tpssh.teampass.exceptions import TeampassHttpException, TeampassApiException


class TeampassClient:
    TYPE_MODIFICATION = {'item': 'items'}

    def __init__(self, api_endpoint, api_key):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        requests.packages.urllib3.disable_warnings()

    def search(self, type, search_string):
        if type in self.TYPE_MODIFICATION:
            local_type = self.TYPE_MODIFICATION[type]

        url = '{0}/find/{1}/{2}?apikey={3}'\
              .format(self.api_endpoint, local_type, search_string, self.api_key)
        req = requests.get(url, verify=False)
        if req.status_code != 200:
            if req.json() and 'err' in req.json():
                raise TeampassApiException(req.json()['err'])
            else:
                raise TeampassHttpException(req.status_code, req.text)
        else:
            if 'err' in req.json() and req.json()['err'] == 'No results':
                raise TeampassApiException(req.json()['err'])
            else:
                result = self.__format_result(type, req.json())
                return result

    def __format_result(self, type, data):
        result = []
        for item in data:
            result.append(OrderedDict([
                                      ('Login', item['login']),
                                      ('Password', item['pw'])
                                      ]))
        return result
