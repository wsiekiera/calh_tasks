import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

import requests


class Target:
    def __init__(self):
        pass

    def request(self, json_request):
        # sample method to process json request
        # validate json_request ...
        json_dict = json.loads(json_request)
        if 'customer_request' not in json_dict \
                or 'customer' not in json_dict['customer_request'] \
                or 'cunbr' not in json_dict['customer_request']['customer']:
            raise ValueError('json input format seems wrong')
        # ... if valid return sample json response
        return '''{
  "customer_response": {
    "customer": {
      "cunbr": "0000001",
      "accounts": [
        {
          "account_number": "11111111"
        },
        {
          "account_number": "22222222"
        }
      ]
    }
  }
}'''


class XMLWebServiceInvoker:
    def __init__(self):
        pass

    def request(self, cunbr):
        # Make request to xml webservice with cunbr number
        # returns xml webservice response as string
        # IMPLEMENT ME PLZ!
        raise NotImplementedError


class Adapter(Target):
    def __init__(self, adaptee):
        super().__init__()
        self.adaptee = adaptee

    def request(self, json_request):
        # IMPLEMENT ME PLZ!
        # json_request - request w formacie json zgodny z formatem:
        # {
        #     "customer_request": {
        #         "customer": {
        #             "cunbr": "2878037"
        #         }
        #     }
        # }
        #
        # Wyłuskaj numer cunbr z requersta i wykonaj zapytanie do serwisu
        # Pozyskany XML prezkonwertuj na json
        # Pamiętaj o użyciu buildera do stworzenia json response.
        # Zwróc json_response w formie stringa zgodny z formatem:
        # {
        #   "customer_response": {
        #     "customer": {
        #       "cunbr": "2878037",
        #       "accounts": ["92374593074", "12429840547", "48940397874", "28007854550", "26016119210"]
        #     }
        #   }
        # }
        raise NotImplementedError


class AbstractJsonBuilder(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def with_cunbr(self, cunbr):
        pass

    def build(self):
        # IMPLEMENT ME PLZ!
        raise NotImplementedError


class JsonResponseBuilder(AbstractJsonBuilder):
    def __init__(self):
        # IMPLEMENT ME PLZ!
        raise NotImplementedError

    def with_cunbr(self, cunbr):
        # IMPLEMENT ME PLZ!
        raise NotImplementedError

    def with_accounts(self, accounts):
        # IMPLEMENT ME PLZ!
        raise NotImplementedError


class JsonRequestBuilder(AbstractJsonBuilder):
    def __init__(self):
        # IMPLEMENT ME PLZ!
        raise NotImplementedError

    def with_cunbr(self, cunbr):
        # IMPLEMENT ME PLZ!
        raise NotImplementedError


def client_code(service, payload):
    return service.request(payload)


if __name__ == '__main__':
    xml_web_service = XMLWebServiceInvoker()
    adapter = Adapter(xml_web_service)
    json_requests = []
    json_responses = []
    with open('input_data.txt') as file:
        lines = file.readlines()
        for line in lines:
            json_request = JsonRequestBuilder().with_cunbr(line.strip()).build()
            json_response = client_code(adapter, json_request)
            json_responses.append(json_response + '\n')
            json_requests.append(json_request + '\n')
    with open('json_requests.txt', 'w') as file:
        for request in json_requests:
            file.write(request)
    with open('json_responses.txt', 'w') as file:
        for response in json_responses:
            file.write(response)
    # target = Target()
    # response = client_code(target, '{"customer_request": {"customer": {"cunbr": "2878037"}}}')
    # print(response)
    #
    # # Run client code with native xml service (returns 404)
    # xml_web_service = XMLWebServiceInvoker()
    # response = client_code(xml_web_service, '{"customer_request": {"customer": {"cunbr": "2878037"}}}')
    # print(response)
    #
    # # Run client code with webservice using adapter
    # adapter = Adapter(xml_web_service)
    # response = client_code(adapter, '{"customer_request": {"customer": {"cunbr": "2878037"}}}')
    # print(response)
