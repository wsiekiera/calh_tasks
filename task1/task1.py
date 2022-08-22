# 1. Pod adresem https://coding-academy.pl/all_customers znajduje się lista numerów cunbr klientów banku.
# Serwis zwraca dane w formacie xml. Napisz skrypt łączący się ze ww serwisem, pobierający dane i zapisujący je do pliku tekstowego (każdy numer w osobnym wierszu; nazwa pliku task1_solution.txt).
#
# Aby uznać zadanie za zaliczone użyj bibliotek:
# Requests [https://requests.readthedocs.io/en/latest/]
# ElementTree [https://docs.python.org/3/library/xml.etree.elementtree.html]
#
# Przykład:
# ## wejście (fragment pozyskany z https://coding-academy.pl/all_customers) ##
# <all_customers>
# <customer>2878037</customer>
# <customer>9151082</customer>
# <customer>3728381</customer>
# ...
#
# ## wyjście (to zapisujesz do pliku) ##
# 2878037
# 9151082
# 3728381
# ...

import json
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs
from abc import ABC, abstractmethod

import requests

def task1_solution():
    res = requests.get('https://coding-academy.pl/all_customers')
    bs_content = bs(res.text, features='lxml')
    customer_numbers = [customer.text for customer in bs_content.findAll('customer')]
    with open('task1_solution.txt', 'w') as f:
        f.write('\n'.join(customer_numbers))


if __name__ == '__main__':
    task1_solution()