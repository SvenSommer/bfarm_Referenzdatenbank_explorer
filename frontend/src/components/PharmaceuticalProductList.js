import React, { useEffect, useState } from 'react';
import { Table, Form } from 'react-bootstrap';
import { fetchPharmaceuticalProducts } from '../api';
import { Link } from 'react-router-dom';
import Pagination from './Pagination';

const PharmaceuticalProductList = () => {
    const [pharmaceuticalProducts, setPharmaceuticalProducts] = useState([]);
    const [page, setPage] = useState(1);
    const [perPage, setPerPage] = useState(10);
    const [totalPages, setTotalPages] = useState(1);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchPharmaceuticalProducts(page, perPage);
                setPharmaceuticalProducts(data.items);
                setTotalPages(data.total_pages);
            } catch (error) {
                console.error('Error fetching pharmaceutical products:', error);
            }
        };
        fetchData();
    }, [page, perPage]);

    const handlePerPageChange = (event) => {
        setPerPage(parseInt(event.target.value, 10));
        setPage(1); // Reset to first page when perPage changes
    };

    return (
        <div>
            <h1>Pharmaceutical Products</h1>
            <Form.Group controlId="perPageSelect">
                <Form.Label>Items per page:</Form.Label>
                <Form.Control as="select" value={perPage} onChange={handlePerPageChange}>
                    <option value={10}>10</option>
                    <option value={25}>25</option>
                    <option value={50}>50</option>
                    <option value={100}>100</option>
                </Form.Control>
            </Form.Group>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Key</th>
                        <th>Name</th>
                        <th>Short Form</th>
                    </tr>
                </thead>
                <tbody>
                    {pharmaceuticalProducts.map(product => (
                        <tr key={product.key}>
                            <td><Link to={`/pharmaceutical_product/${product.key}`}>{product.key}</Link></td>
                            <td>{product.name}</td>
                            <td>{product.put_short}</td>

                        </tr>
                    ))}
                </tbody>
            </Table>
            <Pagination currentPage={page} totalPages={totalPages} onPageChange={setPage} />
        </div>
    );
};

export default PharmaceuticalProductList;
