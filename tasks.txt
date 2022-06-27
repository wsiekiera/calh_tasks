1. Pod adresem https://coding-academy.pl/all_customers znajduje się lista numerów cunbr klientów banku.
Serwis zwraca dane w formacie xml. Napisz skrypt łączący się ze ww serwisem, pobierający dane i zapisujący je do pliku tekstowego (każdy numer w osobnym wierszu; nazwa pliku task1_solution.txt).

Aby uznać zadanie za zaliczone użyj bibliotek:
Requests [https://requests.readthedocs.io/en/latest/]
ElementTree [https://docs.python.org/3/library/xml.etree.elementtree.html]

Przykład:
## wejście (fragment pozyskany z https://coding-academy.pl/all_customers) ##
<all_customers>
<customer>2878037</customer>
<customer>9151082</customer>
<customer>3728381</customer>
...

## wyjście (to zapisujesz do pliku) ##
2878037
9151082
3728381
...

2. Każdy klient banku ma przypisane do siebie numery kont. Numery dla poszczególnych klientów można pobrać z serwisu:
https://coding-academy.pl/customer/<cunbr> (zobacz np. https://coding-academy.pl/customer/2878037). Niestety serwis zwraca dane w formacie xml, a w aplikacji potrzebujemy jsona. Napisz adapter:
- zmieniający request w json na poprawne wywołanie serwisu
- zmieniający odpowiedź w xml na poprawną odpowiedź w formacie json

Przykładowy request:
{
  "customer_request": {
    "customer": {
      "cunbr": "2878037"
    }
  }
}
zamieniamy na
https://coding-academy.pl/customer/2878037

Wykonujemy request do serwisu i uzyskujemy odpowiedź:
<customer_data>
    <customer>2878037</customer>
    <accounts>
        <account>92374593074</account>
        <account>12429840547</account>
        <account>48940397874</account>
        <account>28007854550</account>
        <account>26016119210</account>
    </accounts>
</customer_data>

Zamieniamy odpowiedź na jsona i zwracamy w takiej postaci:
{
  "customer_response": {
    "customer": {
      "cunbr": "2878037",
      "accounts": ["92374593074", "12429840547", "48940397874", "28007854550", "26016119210"]
    }
  }
}

Aby zaliczyć zadanie:
- użyj wzorca Adapter do konwersji json->http_call->xml->json
- użyj wzorca Builder aby przygotować zapytanie w json i odpowiedź w json (klasy JsonRequestBuilder, JsonResponseBuilder)
- zapisz zapytania w json (wygenerowane na podstawie danych z input_data.txt) do pliku json_requests.txt
- zapisz odpowiedzi serwisu w json (po konwersji adapterem!) do pliku json_responses.txt
- zapytania i odpowiedzi wygeneruj za pomocą wcześniej przygotowanych builderów

sample_input_data.txt, sample_json_requests.txt i sample_json_responses.txt zawierają przykładowe dane wraz z rozwiązaniem.