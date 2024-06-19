import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Table } from 'react-bootstrap';
import { fetchSubstanceByKey } from '../api';

const SubstanceDetail = () => {
    const [substance, setSubstance] = useState(null);
    const { key } = useParams();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchSubstanceByKey(key);
                setSubstance(data);
            } catch (error) {
                console.error('Error fetching substance details:', error);
            }
        };
        fetchData();
    }, [key]);

    if (!substance) return <div>Loading...</div>;

    return (
        <div>
            <h1>{substance.name}</h1>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Attribute</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Strength</td>
                        <td>{substance.strength}</td>
                    </tr>
                    <tr>
                        <td>Substance ID</td>
                        <td>{substance.substance_id}</td>
                    </tr>
                    <tr>
                        <td>Rank</td>
                        <td>{substance.rank}</td>
                    </tr>
                    <tr>
                        <td>Key</td>
                        <td>{substance.key}</td>
                    </tr>
                </tbody>
            </Table>
        </div>
    );
};

export default SubstanceDetail;
