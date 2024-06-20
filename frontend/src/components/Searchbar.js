import React from 'react';
import { Form, FormControl, Button } from 'react-bootstrap';

const SearchBar = ({ value, onChange, onSearch }) => {
    return (
        <Form inline>
            <FormControl
                type="text"
                placeholder="Search"
                className="mr-sm-2"
                value={value}
                onChange={onChange}
            />
            <Button variant="outline-success" onClick={onSearch}>Search</Button>
        </Form>
    );
};

export default SearchBar;