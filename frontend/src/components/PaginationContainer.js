import React from 'react';
import { Form } from 'react-bootstrap';
import Pagination from './Pagination';

const PaginationContainer = ({ currentPage, totalPages, onPageChange, perPage, onPerPageChange }) => {
    const handlePerPageChange = (event) => {
        const value = event.target.value;
        onPerPageChange(parseInt(value, 10));
        onPageChange(1); // Reset to first page when perPage changes
    };

    return (
        <div className="pagination-container">
            <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={onPageChange} />
            <div className="items-per-page">
                <Form.Label>Items per page:</Form.Label>
                <Form.Control as="select" value={perPage} onChange={handlePerPageChange}>
                    <option value={10}>10</option>
                    <option value={25}>25</option>
                    <option value={50}>50</option>
                    <option value={100}>100</option>
                </Form.Control>
            </div>
        </div>
    );
};

export default PaginationContainer;
