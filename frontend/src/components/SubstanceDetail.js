import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Table } from 'react-bootstrap';
import { fetchSubstanceById } from '../api';

const SubstanceDetail = () => {
    const [substance, setSubstance] = useState(null);
    const { key } = useParams();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchSubstanceById(key);
                setSubstance(data);
            } catch (error) {
                console.error('Error fetching substance details:', error);
            }
        };
        fetchData();
    }, [key]);

    if (!substance) return <div className="container">Loading...</div>;

    return (
        <div className="container">
            <h1>BfArM Data Explorer</h1>
            <h6>Eine Visualisierung der <a href="https://www.bfarm.de/DE/Arzneimittel/Arzneimittelinformationen/Referenzdatenbank/_node.html" target="_blank" rel="noopener noreferrer">
                BfArM  Referenzdatenbank für Fertigarzneimittel gemäß § 31b SGB V
            </a> </h6><p></p>
            <h2>Wirkstoff: {substance.substance_name}</h2>
            <Link to={`/`}>  zurück</Link>
            <h3>{substance.substance_name} wird in folgenden pharmazeutischen Produkten verwendet</h3>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Pharmazeutisches Produkt</th>
                        <th>Beschreibung</th>
                        <th>Wirkstärke</th>
                    </tr>
                </thead>
                <tbody>
                    {substance.pharmaceutical_products.map(product => (
                        <tr key={product.pharmaceutical_product_key}>
                            <td><Link to={`/pharmaceutical_product/${product.pharmaceutical_product_key}`}>{product.pharmaceutical_product_key}</Link></td>
                            <td>{product.description}</td>
                            <td>{product.strength}</td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </div>
    );
};

export default SubstanceDetail;
