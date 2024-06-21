# BfArM Data Explorer API

## Übersicht

Dies ist eine Flask-basierte API zum Erkunden der Referenzdatenbank des BfArM. Die API ermöglicht es, Informationen zu medizinischen Produkten, pharmazeutischen Produkten und Substanzen abzurufen und zu durchsuchen.

## Projektstruktur

````
explorer/
├── init.py
├── main.py
├── models.py
data/
└── 20240617-REFERENCE.zip
requirements.txt
````


## Installation

1. **Erstelle eine virtuelle Umgebung:**

    ```sh
    python3 -m venv venv
    ```

2. **Aktiviere die virtuelle Umgebung:**

    ```sh
    source venv/bin/activate
    ```

3. **Installiere die Pakete:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Starte den Flask-Server:**

    ```sh
    cd explorer
    gunicorn -w 4 -b 0.0.0.0:8000 main:app
    ```

## Endpunkte

### 1. Get Medicinal Product by PZN

- **URL:** `/pzn/<pzn>`
- **Method:** `GET`
- **Beschreibung:** Ruft Informationen zu einem medizinischen Produkt anhand der Pharmazentralnummer (PZN) ab.
- **Beispiel:** `GET /pzn/18027927`

#### Antwortformat:

```json
{
    "key": 18027927,
    "pzn": 18027927,
    "count_substance": 2,
    "multiple_ppt": 1,
    "put_short": "KombiPg",
    "put_long": "Kombipackung",
    "name": "Filmtablette und Tablette",
    "term_id": 3000148042,
    "pharmaceutical_products": [
        {
            "key": "08839535-1",
            "number": 1,
            "put_short": "Tabl",
            "put_long": "Tablette",
            "name": "Tablette",
            "term_id": 2350000038,
            "description": "Tablette",
            "substances": [
                {
                    "key": "10102003-1-1",
                    "name": "Cobicistat",
                    "strength": "150 mg",
                    "substance_id": 39570,
                    "rank": 1,
                    "link": "/substance/10102003-1-1"
                }
            ],
            "link": "/pharmaceutical_product/08839535-1"
        }
    ],
    "link": "/pzn/18027927"
}
```

###  2. Get Products by Substance
- **URL:** /substance/<substance_name>
- **Method:** `GET`
- **Beschreibung:** Ruft alle pharmazeutischen Produkte ab, die eine bestimmte Substanz enthalten.
- **Parameter:**
  - **`page`:** (optional) Die Seite der Ergebnisse (Standard: 1).
  - **`per_page`:** (optional) Anzahl der Ergebnisse pro Seite (Standard: 10).
- **Beispiel:** `GET /substance/Cobicistat`
#### Antwortformat:
```json
{
    "items": [
        {
            "key": "08839535-1",
            "medicinal_product_key": 18027927,
            "number": 1,
            "put_short": "Tabl",
            "put_long": "Tablette",
            "name": "Tablette",
            "term_id": 2350000038,
            "description": "Tablette",
            "substances": [
                {
                    "key": "10102003-1-1",
                    "name": "Cobicistat",
                    "strength": "150 mg",
                    "substance_id": 39570,
                    "rank": 1,
                    "link": "/substance/10102003-1-1"
                }
            ],
            "link": "/pharmaceutical_product/08839535-1"
        }
    ],
    "total_items": 1,
    "total_pages": 1,
    "current_page": 1,
    "per_page": 10
}

```

###  3. List All Medicinal Products
- **URL:**  `/medicinal_products`
- **Method:** `GET`
- **Beschreibung:** Listet alle medizinischen Produkte mit Pagination.
- **Parameter:**
  - **`page`:** (optional) Die Seite der Ergebnisse (Standard: 1).
  - **`per_page`:** (optional) Anzahl der Ergebnisse pro Seite (Standard: 10).
- **Beispiel:**  `GET /medicinal_products?page=2&per_page=5`
#### Antwortformat:
```json
{
    "items": [
        {
            "key": 18027927,
            "pzn": 18027927,
            "count_substance": 2,
            "multiple_ppt": 1,
            "put_short": "KombiPg",
            "put_long": "Kombipackung",
            "name": "Filmtablette und Tablette",
            "term_id": 3000148042,
            "link": "/pzn/18027927"
        },
        ...
    ],
    "total_items": 100,
    "total_pages": 10,
    "current_page": 2,
    "per_page": 10
}
```
###  4. List All Pharmaceutical Products
- **URL:**  `/pharmaceutical_products`
- **Method:** `GET`
- **Beschreibung:** Listet alle pharmazeutischen Produkte mit Pagination.
- **Parameter:**
  - **`page`:** (optional) Die Seite der Ergebnisse (Standard: 1).
  - **`per_page`:** (optional) Anzahl der Ergebnisse pro Seite (Standard: 10).
- **Beispiel:**  `GET /pharmaceutical_products?page=1&`per_page=20
#### Antwortformat:
```json
{
    "items": [
        {
            "key": "08839535-1",
            "medicinal_product_key": 18027927,
            "number": 1,
            "put_short": "Tabl",
            "put_long": "Tablette",
            "name": "Tablette",
            "term_id": 2350000038,
            "description": "Tablette",
            "link": "/pharmaceutical_product/08839535-1"
        },
        ...
    ],
    "total_items": 200,
    "total_pages": 10,
    "current_page": 1,
    "per_page": 20
}
```
5. List All Substances
- **URL:**  `/substances`
- **Method:** `GET`
- **Beschreibung:** Listet alle Substanzen mit Pagination.
- **Parameter:**
  - **`page`:** (optional) Die Seite der Ergebnisse (Standard: 1).
  - **`per_page`:** (optional) Anzahl der Ergebnisse pro Seite (Standard: 10).
- **Beispiel:**  `GET /substances?page=3&per_page=15`
#### Antwortformat:
```json
{
    "items": [
        {
            "key": "10102003-1-1",
            "pharmaceutical_product_key": "08839535-1",
            "name": "Cobicistat",
            "strength": "150 mg",
            "substance_id": 39570,
            "rank": 1,
            "link": "/substance/10102003-1-1"
        },
        ...
    ],
    "total_items": 300,
    "total_pages": 20,
    "current_page": 3,
    "per_page": 15
}
```
6. Get Pharmaceutical Product by Key
- **URL:**  `/pharmaceutical_product/<key>`
- **Method:** `GET`
- **Beschreibung:** Ruft Informationen zu einem pharmazeutischen Produkt anhand seines Schlüssels ab.
- **Beispiel:**  `GET /pharmaceutical_product/08839535-1`
#### Antwortformat:
```json
{
    "key": "08839535-1",
    "medicinal_product_key": 18027927,
    "number": 1,
    "put_short": "Tabl",
    "put_long": "Tablette",
    "name": "Tablette",
    "term_id": 2350000038,
    "description": "Tablette",
    "substances": [
        {
            "key": "10102003-1-1",
            "name": "Cobicistat",
            "strength": "150 mg",
            "substance_id": 39570,
            "rank": 1,
            "link": "/substance/10102003-1-1"
        }
    ],
    "link": "/pharmaceutical_product/08839535-1"
}
```
7. Get Substance by Key
- **URL:**  `/substance/<key>`
- **Method:** `GET`
- **Beschreibung:**  Ruft Informationen zu einer Substanz anhand ihres Schlüssels ab.
- **Beispiel:**  `GET /substance/10102003-1-1`
#### Antwortformat:
```json
{
    "key": ...,
    "pharmaceutical_product_key": ...,
    "name": ...,
    "strength": ...,
    "substance_id": ...,
    "rank": ...,
    "link": ...
}
```

### Beispielanfragen
Medizinisches Produkt nach PZN abrufen:

```sh
curl http://127.0.0.1:5000/pzn/18027927

```
Produkte nach Substanz abrufen:

```sh
curl http://127.0.0.1:5000/substance/Cobicistat
```
Liste aller medizinischen Produkte (mit Pagination):

```sh
curl "http://127.0.0.1:5000/medicinal_products?page=1&per_page=5"
```