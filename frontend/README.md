# BfArM Data Explorer Frontend

This is a React-based frontend application for exploring the BfArM data using a Flask API. The application allows users to browse and search for medicinal products, pharmaceutical products, and substances.

## Project Structure
```
bfarm-frontend/
├── public/
│ └── index.html
├── src/
│ ├── components/
│ │ ├── MedicinalProductList.js
│ │ ├── PharmaceuticalProductList.js
│ │ ├── SubstanceList.js
│ │ ├── MedicinalProductDetail.js
│ │ ├── PharmaceuticalProductDetail.js
│ │ ├── SubstanceDetail.js
│ ├── App.js
│ ├── index.js
│ └── api.js
├── package.json
└── README.md
```


## Installation

1. **Navigate to your project directory:**

    ```sh
    cd bfarm-frontend
    ```

2. **Install dependencies:**

    ```sh
    npm install
    ```

3. **Start the React application:**

    ```sh
    npm start
    ```

The application will start and can be accessed at `http://localhost:3000`.

## Components

### MedicinalProductList

Displays a paginated list of medicinal products. Fetches data from the `/medicinal_products` endpoint.

### PharmaceuticalProductList

Displays a paginated list of pharmaceutical products. Fetches data from the `/pharmaceutical_products` endpoint.

### SubstanceList

Displays a paginated list of substances. Fetches data from the `/substances` endpoint.

### MedicinalProductDetail

Displays detailed information about a specific medicinal product. Fetches data from the `/pzn/:pzn` endpoint.

### PharmaceuticalProductDetail

Displays detailed information about a specific pharmaceutical product. Fetches data from the `/pharmaceutical_product/:key` endpoint.

### SubstanceDetail

Displays detailed information about a specific substance. Fetches data from the `/substance/:key` endpoint.

## API

The frontend interacts with the following API endpoints:

- **`/pzn/:pzn`**: Get Medicinal Product by PZN
- **`/substance/:substance_name`**: Get Products by Substance
- **`/medicinal_products`**: List All Medicinal Products
- **`/pharmaceutical_products`**: List All Pharmaceutical Products
- **`/substances`**: List All Substances
- **`/pharmaceutical_product/:key`**: Get Pharmaceutical Product by Key
- **`/substance/:key`**: Get Substance by Key

## License

This project is licensed under the MIT License.
