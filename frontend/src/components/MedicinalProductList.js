import React, { useEffect, useState } from 'react';
import { Table, Form, Dropdown, DropdownButton, ButtonGroup } from 'react-bootstrap';
import { fetchMedicinalProducts, fetchSupportedFHIRProfiles, handleDownload } from '../api';
import { Link } from 'react-router-dom';
import PaginationContainer from './PaginationContainer';

const MedicinalProductList = () => {
    const [medicinalProducts, setMedicinalProducts] = useState([]);
    const [page, setPage] = useState(1);
    const [perPage, setPerPage] = useState(10);
    const [totalPages, setTotalPages] = useState(1);
    const [supportedProfiles, setSupportedProfiles] = useState({});

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchMedicinalProducts(page, perPage);
                setMedicinalProducts(data.items);
                setTotalPages(data.total_pages);
                
                const profiles = await fetchSupportedFHIRProfiles();
                setSupportedProfiles(profiles);
            } catch (error) {
                console.error('Error fetching medicinal products:', error);
            }
        };
        fetchData();
    }, [page, perPage]);

    const handlePerPageChange = (event) => {
        setPerPage(parseInt(event.target.value, 10));
        setPage(1); // Reset to first page when perPage changes
    };

    return (
        <div className="medicinal-product-list">
            <div className="container">
                <h1>Medizinische Produkte</h1>
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
                                <td><Link to={`/pzn/${product.pzn}`}>{product.pzn}</Link></td>
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
                    onPerPageChange={setPerPage} 
                />
            </div>
        </div>
    );
};

export default MedicinalProductList;