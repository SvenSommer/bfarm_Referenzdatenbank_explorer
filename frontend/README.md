
# Frontend für BfArM Data Explorer

Dieses Verzeichnis enthält den Quellcode für das Frontend des BfArM Data Explorer. Das Frontend wurde mit React erstellt und bietet eine Benutzeroberfläche zur Visualisierung und Erkundung der vom BfArM bereitgestellten Referenzdatenbank für Fertigarzneimittel gemäß § 31b SGB V.

## Installation und Ausführung

### Voraussetzungen

- Node.js
- Yarn

### Schritte zur Installation

1. **Repository klonen:**

    ```sh
    git clone https://github.com/SvenSommer/bfarm_Referenzdatenbank_explorer.git
    cd bfarm_Referenzdatenbank_explorer/frontend
    ```

2. **Abhängigkeiten installieren:**

    ```sh
    yarn install
    ```

3. **Entwicklungsserver starten:**

    ```sh
    yarn start
    ```

    Die Anwendung wird standardmäßig auf `http://localhost:3000` ausgeführt.

### Produktions-Build

Um eine Produktionsversion des Projekts zu erstellen, führen Sie den folgenden Befehl aus:

```sh
yarn build
```

Dadurch wird ein `build`-Verzeichnis erstellt, das die optimierten Produktionsdateien enthält.


### Verbesserungsvorschläge

Hast du einen Verbesserungsvorschlag? Schick einen Pull Request!

## Lizenz

Dieses Projekt ist lizenziert unter der MIT-Lizenz. Weitere Details finden Sie in der [LICENSE](../LICENSE) Datei.
