import React, { useEffect, useState } from 'react';
import { Table, Form, Dropdown, ButtonGroup } from 'react-bootstrap';
import { fetchMedicinalProducts, fetchSupportedFHIRProfiles, handleDownload } from '../api';
import { Link } from 'react-router-dom';
import PaginationContainer from './PaginationContainer';

const MedicinalProductList = () => {
    const [medicinalProducts, setMedicinalProducts] = useState([]);
    const [page, setPage] = useState(1);
    const [perPage, setPerPage] = useState(10);
    const [totalPages, setTotalPages] = useState(1);
    const [totalFound, setTotalFound] = useState(0); // New state for total found items
    const [searchQuery, setSearchQuery] = useState('');
    const [supportedProfiles, setSupportedProfiles] = useState({});

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchMedicinalProducts(page, perPage, searchQuery);
                setMedicinalProducts(data.items);
                setTotalPages(data.total_pages);
                setTotalFound(data.total_found); // Set the total found items
                
                const profiles = await fetchSupportedFHIRProfiles();
                setSupportedProfiles(profiles);
            } catch (error) {
                console.error('Error fetching medicinal products:', error);
            }
        };
        fetchData();
    }, [page, perPage, searchQuery]);

    const handlePerPageChange = (perPageValue) => {
        setPerPage(perPageValue);
        setPage(1); // Reset to first page when perPage changes
    };

    const handleSearchChange = (event) => {
        setSearchQuery(event.target.value);
        setPage(1); // Reset to first page when search query changes
    };

    return (
        <div className="medicinal-product-list">
            <div className="container">
                <h1>Medizinische Produkte</h1>
                <Form.Group controlId="searchQuery">
                    <Form.Control 
                        type="text" 
                        placeholder="Nach Medizinischen Produkten suchen..." 
                        value={searchQuery} 
                        onChange={handleSearchChange} 
                    />
                </Form.Group>
                <p>{totalFound} Ergebnisse gefunden</p> {/* Display the total found items */}
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>PZN</th>
                            <th>Kombipackung</th>
                            <th>Darreichungsform (kurz)</th>
                            <th>Darreichungsform (lang)</th>
                            <th>Darreichungsform (BfArM)</th>
                            <th>Anzahl aller Wirkstoffe</th>
                            <th>FHIR Profiles</th>
                        </tr>
                    </thead>
                    <tbody>
                        {medicinalProducts.map(product => (
                            <tr key={product.key}>
                                <td><Link to={`/pzn/${product.pzn}`}>{String(product.pzn).padStart(8, '0')}</Link></td>
                                <td>{product.multiple_ppt === 1 ? "Ja" : "Nein"}</td>
                                <td>{product.put_short}</td>
                                <td>{product.put_long}</td>
                                <td>{product.name}</td>
                                <td>{product.count_substance}</td>
                                <td>
                                    <Dropdown as={ButtonGroup} className="icon-space">
                                        <Dropdown.Toggle as="a" id="dropdown-download">
                                            <i className="fas fa-download"></i>
                                        </Dropdown.Toggle>
                                        <Dropdown.Menu>
                                            <table className="dropdown-table">
                                                <tbody>
                                                    {Object.keys(supportedProfiles).map(profile => (
                                                        supportedProfiles[profile].map(version => (
                                                            <tr className="dropdown-table-row" key={`${profile}-${version}`}>
                                                                <td>{profile} {version}</td>
                                                                <td>
                                                                    <a href="#" onClick={() => handleDownload(product.pzn, profile, version, 'json', 'download')}>JSON</a>
                                                                </td>
                                                                <td>
                                                                    <a href="#" onClick={() => handleDownload(product.pzn, profile, version, 'xml', 'download')}>XML</a>
                                                                </td>
                                                            </tr>
                                                        ))
                                                    ))}
                                                </tbody>
                                            </table>
                                        </Dropdown.Menu>
                                    </Dropdown>
                                    <Dropdown as={ButtonGroup} className="icon-space">
                                        <Dropdown.Toggle as="a" id="dropdown-view">
                                            <i className="fas fa-eye"></i>
                                        </Dropdown.Toggle>
                                        <Dropdown.Menu>
                                            <table className="dropdown-table">
                                                <tbody>
                                                    {Object.keys(supportedProfiles).map(profile => (
                                                        supportedProfiles[profile].map(version => (
                                                            <tr className="dropdown-table-row" key={`${profile}-${version}`}>
                                                                <td>{profile} {version}</td>
                                                                <td>
                                                                    <a href="#" onClick={() => handleDownload(product.pzn, profile, version, 'json', 'view')}>JSON</a>
                                                                </td>
                                                                <td>
                                                                    <a href="#" onClick={() => handleDownload(product.pzn, profile, version, 'xml', 'view')}>XML</a>
                                                                </td>
                                                            </tr>
                                                        ))
                                                    ))}
                                                </tbody>
                                            </table>
                                        </Dropdown.Menu>
                                    </Dropdown>
                                </td>
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

export default MedicinalProductList;
