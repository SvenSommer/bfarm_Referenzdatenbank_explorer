import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Table } from 'react-bootstrap';
import { fetchPharmaceuticalProductByKey } from '../api';

const PharmaceuticalProductDetail = () => {
    const [product, setProduct] = useState(null);
    const { key } = useParams();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchPharmaceuticalProductByKey(key);
                setProduct(data);
            } catch (error) {
                console.error('Error fetching pharmaceutical product details:', error);
            }
        };
        fetchData();
    }, [key]);

    if (!product) return <div>Loading...</div>;

    return (
        <div>
            <h1>{product.name}</h1>
            <p>{product.description}</p>
            <h2>Substances</h2>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Key</th>
                        <th>Name</th>
                        <th>Strength</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    {product.substances.map(substance => (
                        <tr key={substance.key}>
                            <td>{substance.key}</td>
                            <td>{substance.name}</td>
                            <td>{substance.strength}</td>
                            <td>
                                <Link to={`/substance/${substance.key}`}>Details</Link>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </div>
    );
};

export default PharmaceuticalProductDetail;
