import React, { useEffect, useState } from 'react';
import { Table, Form } from 'react-bootstrap';
import { fetchMedicinalProducts } from '../api';
import { Link } from 'react-router-dom';
import Pagination from './Pagination';

const MedicinalProductList = () => {
    const [medicinalProducts, setMedicinalProducts] = useState([]);
    const [page, setPage] = useState(1);
    const [perPage, setPerPage] = useState(10);
    const [totalPages, setTotalPages] = useState(1);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchMedicinalProducts(page, perPage);
                setMedicinalProducts(data.items);
                setTotalPages(data.total_pages);
            } catch (error) {
                console.error('Error fetching medicinal products:', error);
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
            <h1>Medicinal Products</h1>
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
                        <th>PZN</th>
                        <th>Name</th>
                        <th>Short Form</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    {medicinalProducts.map(product => (
                        <tr key={product.key}>
                            <td>{product.pzn}</td>
                            <td>{product.name}</td>
                            <td>{product.put_short}</td>
                            <td>
                                <Link to={`/pzn/${product.pzn}`}>Details</Link>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>
            <Pagination currentPage={page} totalPages={totalPages} onPageChange={setPage} />
        </div>
    );
};

export default MedicinalProductList;
