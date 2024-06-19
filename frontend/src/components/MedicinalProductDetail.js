import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Table } from 'react-bootstrap';
import { fetchMedicinalProductByPzn } from '../api';

const MedicinalProductDetail = () => {
    const [product, setProduct] = useState(null);
    const { pzn } = useParams();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchMedicinalProductByPzn(pzn);
                setProduct(data);
            } catch (error) {
                console.error('Error fetching medicinal product details:', error);
            }
        };
        fetchData();
    }, [pzn]);

    if (!product) return <div>Loading...</div>;

    return (
        <div>
            <h1>{product.name}</h1>
            <p>{product.put_long}</p>
            <h2>Pharmaceutical Products</h2>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Key</th>
                        <th>Name</th>
                        <th>Short Form</th>
                        <th>Description</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    {product.pharmaceutical_products.map(pp => (
                        <tr key={pp.key}>
                            <td>{pp.key}</td>
                            <td>{pp.name}</td>
                            <td>{pp.put_short}</td>
                            <td>{pp.description}</td>
                            <td>
                                <Link to={`/pharmaceutical_product/${pp.key}`}>Details</Link>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </div>
    );
};

export default MedicinalProductDetail;
