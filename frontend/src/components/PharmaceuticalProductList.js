import React, { useEffect, useState } from 'react';
import { Table, Form } from 'react-bootstrap';
import { fetchPharmaceuticalProducts } from '../api';
import { Link } from 'react-router-dom';
import PaginationContainer from './PaginationContainer';

const PharmaceuticalProductList = () => {
    const [pharmaceuticalProducts, setPharmaceuticalProducts] = useState([]);
    const [page, setPage] = useState(1);
    const [perPage, setPerPage] = useState(10);
    const [totalPages, setTotalPages] = useState(1);
    const [searchQuery, setSearchQuery] = useState('');
    const [totalFound, setTotalFound] = useState(0); // New state for total found items

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchPharmaceuticalProducts(page, perPage, searchQuery);
                setPharmaceuticalProducts(data.items);
                setTotalPages(data.total_pages);
                setTotalFound(data.total_found); // Set the total found items
            } catch (error) {
                console.error('Error fetching pharmaceutical products:', error);
            }
        };
        fetchData();
    }, [page, perPage, searchQuery]);

    const handlePerPageChange = (value) => {
        setPerPage(value);
        setPage(1); // Reset to first page when perPage changes
    };

    const handleSearchChange = (event) => {
        setSearchQuery(event.target.value);
        setPage(1); // Reset to first page when search query changes
    };

    return (
        <div className="pharmaceutical-product-list">
            <div className="container">
                <h1>Pharmazeutische Produkte</h1>
                <Form.Group controlId="searchQuery">
                    <Form.Control 
                        type="text" 
                        placeholder="Nach Pharmazeutischen Produkten suchen..." 
                        value={searchQuery} 
                        onChange={handleSearchChange} 
                    />
                </Form.Group>
                <p>{totalFound} Ergebnisse gefunden</p> {/* Display the total found items */}
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>Produktschlüssel</th>
                            <th>PZN</th>
                            <th>Darreichungsform (kurz)</th>
                            <th>Darreichungsform (lang)</th>
                            <th>Darreichungsform (BfArM)</th>
                            <th>Beschreibung</th>
                            <th>Anzahl der Wirkstoffe</th>
                        </tr>
                    </thead>
                    <tbody>
                        {pharmaceuticalProducts.map(product => (
                            <tr key={product.key}>
                                <td><Link to={`/pharmaceutical_product/${product.key}`}>{product.key}</Link></td>
                                <td><Link to={`/pzn/${product.medicinal_product_key}`}>{String(product.medicinal_product_key).padStart(8, '0')}</Link></td>
                                <td>{product.put_short}</td>
                                <td>{product.put_long}</td>
                                <td>{product.name}</td>
                                <td>{product.description}</td>
                                <td>{product.substances_count}</td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
                <PaginationContainer
                    currentPage={page}
                    totalPages={totalPages}
                    onPageChange={setPage}
                    perPage={perPage}
                    onPerPageChange={handlePerPageChange}
                />
            </div>
        </div>
    );
};

export default PharmaceuticalProductList;
