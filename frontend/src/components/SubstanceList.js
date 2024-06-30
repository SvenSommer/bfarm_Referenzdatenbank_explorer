import React, { useEffect, useState } from 'react';
import { Table, Form } from 'react-bootstrap';
import { fetchSubstances } from '../api';
import { Link } from 'react-router-dom';
import PaginationContainer from './PaginationContainer';

const SubstanceList = () => {
    const [substances, setSubstances] = useState([]);
    const [page, setPage] = useState(1);
    const [perPage, setPerPage] = useState(10);
    const [totalPages, setTotalPages] = useState(1);
    const [searchQuery, setSearchQuery] = useState('');
    const [totalFound, setTotalFound] = useState(0); // New state for total found items

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchSubstances(page, perPage, searchQuery);
                setSubstances(data.items);
                setTotalPages(data.total_pages);
                setTotalFound(data.total_found); // Set the total found items
            } catch (error) {
                console.error('Error fetching substances:', error);
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
        <div className="substance-list">
            <div className="container">
                <h1>Wirkstoffe</h1>
                <Form.Group controlId="searchQuery">
                    <Form.Label>Suche</Form.Label>
                    <Form.Control 
                        type="text" 
                        placeholder="Nach Wirkstoffen suchen..." 
                        value={searchQuery} 
                        onChange={handleSearchChange} 
                    />
                </Form.Group>
                <p>{totalFound} Ergebnisse gefunden</p> {/* Display the total found items */}
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>Bezeichnung des Wirkstoffs</th>
                            <th>ASK-Nr. BfArM</th>
                        </tr>
                    </thead>
                    <tbody>
                        {substances.map(substance => (
                            <tr key={substance.key}>
                                <td>
                                    <Link to={`/substance_id/${substance.substance_id}`}>{substance.name}</Link>
                                </td>
                                <td>{substance.substance_id}</td>
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

export default SubstanceList;
