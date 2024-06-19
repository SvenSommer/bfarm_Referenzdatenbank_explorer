const API_BASE_URL = "http://127.0.0.1:5000";

export const fetchMedicinalProducts = async (page = 1, perPage = 10) => {
    const response = await fetch(`${API_BASE_URL}/medicinal_products?page=${page}&per_page=${perPage}`);
    if (!response.ok) {
        throw new Error('Failed to fetch medicinal products');
    }
    return response.json();
};

export const fetchPharmaceuticalProducts = async (page = 1, perPage = 10) => {
    const response = await fetch(`${API_BASE_URL}/pharmaceutical_products?page=${page}&per_page=${perPage}`);
    if (!response.ok) {
        throw new Error('Failed to fetch pharmaceutical products');
    }
    return response.json();
};

export const fetchSubstances = async (page = 1, perPage = 10) => {
    const response = await fetch(`${API_BASE_URL}/substances?page=${page}&per_page=${perPage}`);
    if (!response.ok) {
        throw new Error('Failed to fetch substances');
    }
    return response.json();
};

export const fetchMedicinalProductByPzn = async (pzn) => {
    const response = await fetch(`${API_BASE_URL}/pzn/${pzn}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch medicinal product with PZN ${pzn}`);
    }
    return response.json();
};

export const fetchPharmaceuticalProductByKey = async (key) => {
    const response = await fetch(`${API_BASE_URL}/pharmaceutical_product/${key}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch pharmaceutical product with key ${key}`);
    }
    return response.json();
};

export const fetchSubstanceByKey = async (key) => {
    const response = await fetch(`${API_BASE_URL}/substance/${key}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch substance with key ${key}`);
    }
    return response.json();
};
