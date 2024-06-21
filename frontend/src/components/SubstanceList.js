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

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchSubstances(page, perPage);
                setSubstances(data.items);
                setTotalPages(data.total_pages);
            } catch (error) {
                console.error('Error fetching substances:', error);
            }
        };
        fetchData();
    }, [page, perPage]);

    const handlePerPageChange = (event) => {
        setPerPage(parseInt(event.target.value, 10));
        setPage(1); // Reset to first page when perPage changes
    };

    return (
        <div className="substance-list">
            <div className="container">
                <h1>Wirkstoffe</h1>
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
                    onPerPageChange={setPerPage}
                />
            </div>
        </div>
    );
};

export default SubstanceList;
