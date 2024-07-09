import requests
import xml.etree.ElementTree as ET
import sys

# URL des Backends
BASE_URL = 'http://0.0.0.0:8000'

# Funktion zum Abrufen aller pharmazeutischen Produkte
def get_pharmaceutical_products(page=1, per_page=100):
    response = requests.get(f"{BASE_URL}/pharmaceutical_products", params={'page': page, 'per_page': per_page})
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError as e:
            print(f"Fehler beim Parsen der JSON-Antwort: {e}")
            print(f"Response Text: {response.text}")
            return None
    else:
        print(f"Fehler beim Abrufen der pharmazeutischen Produkte: {response.status_code}, Response: {response.text}")
        return None

# Funktion zum Abrufen der Medikationsdaten für eine bestimmte PZN
def get_medication(pzn):
    response = requests.get(f"{BASE_URL}/fhir/medication/{pzn}", params={'profile': 'epa-medication', 'version': '1.0', 'format': 'xml', 'action': 'view'})
    return response

# Funktion zum Überprüfen einer einzelnen PZN und Protokollierung der Fehler
def check_single_pzn(pzn):
    errors = []
    print(f"Überprüfen der PZN {pzn}")
    response = get_medication(pzn)
    if response.status_code != 200:
        try:
            error_message = response.json().get('error', 'Unbekannter Fehler')
        except ValueError:
            error_message = f"Fehler beim Abrufen der Medikationsdaten: {response.text}"
        errors.append({'pzn': pzn, 'error': error_message})
        print(f"Fehler bei PZN {pzn}: {error_message}")
    else:
        print(f"PZN {pzn} erfolgreich überprüft.")

    # Fehler in eine XML-Datei schreiben
    if errors:
        write_errors_to_xml(errors)

# Funktion zum Schreiben von Fehlern in eine XML-Datei
def write_errors_to_xml(errors):
    root = ET.Element("Errors")

    for error in errors:
        error_element = ET.SubElement(root, "Error")
        pzn_element = ET.SubElement(error_element, "PZN")
        pzn_element.text = str(error['pzn'])
        message_element = ET.SubElement(error_element, "Message")
        message_element.text = error['error']
        detail_url1 = ET.SubElement(error_element, 'Detail-URL')
        detail_url1.text = f"https://bfarm-referenzdatenbank-explorer-frontend.onrender.com/pzn/{error['pzn']}"
        detail_url2 = ET.SubElement(error_element, 'Rawdata-URL')
        detail_url2.text = f"https://bfarm-referenzdatenbank-explorer.onrender.com/pzn/{error['pzn']}"

    tree = ET.ElementTree(root)
    tree.write("pzn_errors.xml", encoding='utf-8', xml_declaration=True)
    print(f"Fehlerhafte PZN und deren Fehler wurden in pzn_errors.xml protokolliert.")

# Hauptfunktion zum Überprüfen aller PZN und Protokollierung der Fehler
def check_all_pzn_errors():
    page = 1
    per_page = 10  # Kleinere Seitengröße für schnellere Tests
    total_pages = 7925  # Beispielwert, bitte anpassen wenn anders
    errors = []

    while page <= total_pages:
        print(f"Abrufen der pharmazeutischen Produkte, Seite {page}/{total_pages}")
        products = get_pharmaceutical_products(page, per_page)
        if not products or 'total_found' not in products or len(products.get('items', [])) == 0:
            print("Keine weiteren Produkte gefunden oder Fehler beim Abrufen der Produkte.")
            break

        for product in products['items']:
            pzn = product['medicinal_product_key']
            response = get_medication(pzn)
            if response.status_code != 200:
                try:
                    error_message = response.json().get('error', 'Unbekannter Fehler')
                except ValueError:
                    error_message = f"Fehler beim Abrufen der Medikationsdaten: {response.text}"
                errors.append({'pzn': pzn, 'error': error_message})
                print(f"Fehler bei PZN {pzn}: {error_message}")
            else:
                print(f"PZN {pzn} erfolgreich überprüft.")

        page += 1

    # Fehler in eine XML-Datei schreiben
    if errors:
        write_errors_to_xml(errors)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pzn = sys.argv[1]
        check_single_pzn(pzn)
    else:
        check_all_pzn_errors()