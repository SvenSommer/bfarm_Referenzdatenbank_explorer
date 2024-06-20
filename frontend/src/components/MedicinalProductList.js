import React, { useEffect, useState } from 'react';
import { Table, Form } from 'react-bootstrap';
import { fetchMedicinalProducts } from '../api';
import { Link } from 'react-router-dom';
import PaginationContainer from './PaginationContainer';

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
        <div className="medicinal-product-list">
            <div className="container">
                <h1>Medizinische Produkte</h1>
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>PZN</th>
                            <th>Anzahl aller Wirkstoffe</th>
                            <th>Kombipackung</th>
                            <th>Darreichungsform (kurz)</th>
                            <th>Darreichungsform (lang)</th>
                            <th>Darreichungsform (BfArM)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {medicinalProducts.map(product => (
                            <tr key={product.key}>
                                <td><Link to={`/pzn/${product.pzn}`}>{product.pzn}</Link></td>
                                <td>{product.count_substance}</td>
                                <td>{product.multiple_ppt === 1 ? "Ja" : "Nein"}</td>
                                <td>{product.put_short}</td>
                                <td>{product.put_long}</td>
                                <td>{product.name}</td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
                <PaginationContainer 
                currentPage={page} 
                totalPages={totalPages} 
                onPageChange={setPage} 
                perPage={perPage} 
                onPerPageChange={setPerPage} 
            />
            </div>
        </div>
    );
};

export default MedicinalProductList;