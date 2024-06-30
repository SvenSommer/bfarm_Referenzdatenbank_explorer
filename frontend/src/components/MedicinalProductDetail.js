import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Table,  Dropdown,  ButtonGroup } from 'react-bootstrap';
import { fetchMedicinalProductByPzn, handleDownload, fetchSupportedFHIRProfiles } from '../api';

const MedicinalProductDetail = () => {
    const [product, setProduct] = useState(null);
    const { pzn } = useParams();
    const [supportedProfiles, setSupportedProfiles] = useState({});

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchMedicinalProductByPzn(pzn);
                setProduct(data);

                const profiles = await fetchSupportedFHIRProfiles();
                setSupportedProfiles(profiles);
            } catch (error) {
                console.error('Error fetching medicinal product details:', error);
            }
        };
        fetchData();
    }, [pzn]);

    if (!product) return <div className="container">Loading...</div>;

    return (
        <div className="container">
            <h1>BfArM Data Explorer</h1>
            <h6>Eine Visualisierung der <a href="https://www.bfarm.de/DE/Arzneimittel/Arzneimittelinformationen/Referenzdatenbank/_node.html" target="_blank" rel="noopener noreferrer">
                BfArM  Referenzdatenbank für Fertigarzneimittel gemäß § 31b SGB V
            </a> </h6><p></p>
            <div className="repo-notice">
                <p>
                    Hast du einen Verbesserungsvorschlag? Schick einen Pull Request! 👉
                    <a href="https://github.com/SvenSommer/bfarm_Referenzdatenbank_explorer" target="_blank" rel="noopener noreferrer">
                        GitHub
                    </a>
                </p>
            </div>
            <h2>Medizinisches Produkt mit PZN: {product.pzn}</h2>
            <Link to={`/`}>  zurück</Link>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>PZN</th>
                        <th>Anzahl aller Wirkstoffe</th>
                        <th>Kombipackung</th>
                        <th>Darreichungsform (kurz)</th>
                        <th>Darreichungsform (lang)</th>
                        <th>Darreichungsform (BfArM)</th>
                        <th>FHIR Profiles</th>
                    </tr>
                </thead>
                <tbody>

                    <tr key={product.key}>
                        <td>{product.pzn}</td>
                        <td>{product.count_substance}</td>
                        <td>{product.multiple_ppt === 1 ? "Ja" : "Nein"}</td>
                        <td>{product.put_short}</td>
                        <td>{product.put_long}</td>
                        <td>{product.name}</td>
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

                </tbody>
            </Table>
            <h2>enthält folgende Pharmazeutische Produkte</h2>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Produktschlüssel</th>
                        <th>Darreichungsform (kurz)</th>
                        <th>Darreichungsform (lang)</th>
                        <th>Darreichungsform (BfArM)</th>
                        <th>Beschreibung</th>
                        <th>Anzahl der Wirkstoffe</th>
                    </tr>
                </thead>
                <tbody>
                    {product.pharmaceutical_products.map(pp => (
                        <tr key={pp.key}>
                            <td>
                                <Link to={`/pharmaceutical_product/${pp.key}`}>{pp.key}</Link>
                            </td>
                            <td>{pp.put_short}</td>
                            <td>{pp.put_long}</td>
                            <td>{pp.name}</td>
                            <td>{pp.description}</td>
                            <td>
                                <Link to={`/pharmaceutical_product/${pp.key}`}>{pp.substances.length}</Link>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </div>
    );
};

export default MedicinalProductDetail;
