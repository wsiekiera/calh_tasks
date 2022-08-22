# Aby zaliczyć zadanie:
# - użyj wzorca Adapter do konwersji json->http_call->xml->json
# - użyj wzorca Builder aby przygotować zapytanie w json i odpowiedź w json (klasy JsonRequestBuilder, JsonResponseBuilder)
# - zapisz zapytania w json (wygenerowane na podstawie danych z input_data.txt) do pliku json_requests.txt
# - zapisz odpowiedzi serwisu w json (po konwersji adapterem!) do pliku json_responses.txt
# - zapytania i odpowiedzi wygeneruj za pomocą wcześniej przygotowanych builderów



import json
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs
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

    def request(self, cunbr) -> str:
        # Make request to xml webservice with cunbr number
        # returns xml webservice response as string
        # IMPLEMENT ME PLZ!
        res = requests.get(f'https://coding-academy.pl/customer/{cunbr}')
        return res.text


class Adapter(Target):
    def __init__(self, adaptee: XMLWebServiceInvoker):
        super().__init__()
        self.adaptee = adaptee

    def request(self, json_request) -> str:
        # json_request - request w formacie json zgodny z formatem:
        # {
        #     "customer_request": {
        #         "customer": {
        #             "cunbr": "2878037"
        #         }
        #     }
        # }
        #
        # Wyłuskaj numer cunbr z requesta i wykonaj zapytanie do serwisu
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
        customer_request = json.loads(json_request)
        cunbr = customer_request['customer_request']['customer']['cunbr']
        response_ = self.adaptee.request(cunbr)
        bs_content = bs(response_, features='lxml')
        accounts = [account.text for account in bs_content.findAll('account')]
        return (JsonResponseBuilder()
                .with_cunbr(cunbr)
                .with_accounts(accounts)
                .build())


class AbstractJsonBuilder(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def with_cunbr(self, cunbr):
        pass


    @abstractmethod
    def build(self):
        pass
        # IMPLEMENT ME PLZ!
        #raise NotImplementedError


class JsonRequestBuilder(AbstractJsonBuilder):
    def __init__(self):
        self.json_request = {
            "customer_request": {
                "customer": {
                    "cunbr": None
                }
            }
        }

    def with_cunbr(self, cunbr):
        self.json_request['customer_request']['customer']['cunbr'] = cunbr
        return self

    def build(self):
        # return self.json_request
        return json.dumps(self.json_request)


class JsonResponseBuilder(AbstractJsonBuilder):
    def __init__(self):
        self.json_response = {
            "customer_response": {
                "customer": {
                    "cunbr": None,
                    "accounts": None
                }
            }
        }

    def with_cunbr(self, cunbr):
        self.json_response['customer_response']['customer']['cunbr'] = cunbr
        return self

    def with_accounts(self, accounts):
        self.json_response['customer_response']['customer']['accounts'] = accounts
        return self

    def build(self):
        return json.dumps(self.json_response)


def client_code(service: Adapter, payload) -> str:
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