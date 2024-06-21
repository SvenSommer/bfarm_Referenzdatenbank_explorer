# BfArM Data Explorer

BfArM Data Explorer ist eine Webanwendung zur Visualisierung der vom BfArM bereitgestellten Referenzdatenbank für Fertigarzneimittel gemäß § 31b SGB V. Diese Anwendung besteht aus einem Frontend, das mit React erstellt wurde, und einem Backend, das auf Flask basiert. Das Ziel dieser Anwendung ist es, Benutzern eine einfache Möglichkeit zu bieten, medizinische Produkte, pharmazeutische Produkte und Substanzen zu durchsuchen und anzuzeigen.

## Projektstruktur

Dieses Repository ist in zwei Hauptteile unterteilt:

- `frontend`: Enthält den Quellcode für das React-Frontend.
- `backend`: Enthält den Quellcode für das Flask-Backend.

## Installation und Ausführung

### Voraussetzungen

- Node.js und Yarn (für das Frontend)
- Python und pip (für das Backend)

### Installation

#### Frontend

Wechseln Sie in das `frontend`-Verzeichnis und folgen Sie den Anweisungen in der `README.md`-Datei.

```sh
cd frontend
yarn install
yarn start
```

Weitere Details finden Sie in der [frontend/README.md](frontend/README.md).

#### Backend

Wechseln Sie in das `backend`-Verzeichnis und folgen Sie den Anweisungen in der `README.md`-Datei.

```sh
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd explorer
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```
Weitere Details finden Sie in der [backend/README.md](backend/README.md).

## Verbesserungsvorschläge

Hast du einen Verbesserungsvorschlag? Schick einen Pull Request!

## Lizenz

Dieses Projekt ist lizenziert unter der MIT-Lizenz. Weitere Details finden Sie in der [LICENSE](LICENSE) Datei.

---

Weitere Informationen und detaillierte Anweisungen finden Sie in den entsprechenden `README.md`-Dateien in den `frontend`- und `backend`-Ordnern.