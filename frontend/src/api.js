const API_BASE_URL_prod = "https://bfarm-referenzdatenbank-explorer.onrender.com";
const API_BASE_URL = "http://0.0.0.0:8000";

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

export const fetchSubstanceById = async (key) => {
    console.log(key);
    const response = await fetch(`${API_BASE_URL}/substance_id/${key}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch substance with id ${key}`);
    }
    return response.json();
};

export const fetchSupportedFHIRProfiles = async () => {
    const response = await fetch(`${API_BASE_URL}/fhir/profiles`);
    if (!response.ok) {
        throw new Error('Failed to fetch supported FHIR profiles');
    }
    return response.json();
};


export const handleDownload = (pzn, profile, version, format, action) => {
    const url = `${API_BASE_URL}/fhir/medication/${pzn}?profile=${profile}&version=${version}&format=${format}&action=${action}`;
    if (action === 'view') {
        window.open(url, '_blank');
    } else {
        // Create a temporary link to trigger download
        const link = document.createElement('a');
        link.href = url;
        link.download = `${pzn}_${profile}_${version}.${format}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
};