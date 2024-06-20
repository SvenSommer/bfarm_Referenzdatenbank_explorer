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

    if (!product) return  <div className="container">Loading...</div>;

    return (
        <div className="container">
            <h1>Pharmazeutische Produkt mit Produktschlüssel: {product.key}</h1>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Produktschlüssel</th>
                        <th>PZN</th>
                        <th>Darreichungsform (kurz)</th>
                        <th>Darreichungsform (lang)</th>
                        <th>Darreichungsform (BfArM)</th>
                        <th>Anzahl der Wirkstoffe</th>
                        <th>Beschreibung</th>
                    </tr>
                </thead>
                <tbody>
     
                        <tr key={product.key}>
                            <td>{product.key}</td>
                            <td><Link to={`/pzn/${product.medicinal_product_key}`}>{product.medicinal_product_key}</Link></td>
                            <td>{product.put_short}</td>
                            <td>{product.put_long}</td>
                            <td>{product.name}</td>
                            <td>{product.substances.length}</td>
                            <td>{product.description}</td>
                        </tr>
                    
                </tbody>
            </Table>
            <h2>enthält folgende Wirkstoffe</h2>
            <Table striped bordered hover>
                <thead>
                    <tr>
                    <th>Rang</th>
                        <th>Bezeichnung des Wirkstoffs</th>
                        <th>Wirkstärke</th>
                    </tr>
                </thead>
                <tbody>
                    {product.substances.map(substance => (
                        <tr key={substance.key}>
                            <td>{substance.rank}</td>
                            <td><Link to={`/substance_id/${substance.substance_id}`}>{substance.name}</Link></td>
                            <td>{substance.strength}</td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </div>
    );
};

export default PharmaceuticalProductDetail;
