import React from 'react';
import { Form } from 'react-bootstrap';

const SortDropdown = ({ options, value, onChange }) => {
    return (
        <Form.Group controlId="sortSelect">
            <Form.Label>Sort by:</Form.Label>
            <Form.Control as="select" value={value} onChange={onChange}>
                {options.map((option) => (
                    <option key={option.value} value={option.value}>
                        {option.label}
                    </option>
                ))}
            </Form.Control>
        </Form.Group>
    );
};

export default SortDropdown;