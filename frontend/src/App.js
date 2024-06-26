import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import MedicinalProductList from './components/MedicinalProductList';
import PharmaceuticalProductList from './components/PharmaceuticalProductList';
import SubstanceList from './components/SubstanceList';
import MedicinalProductDetail from './components/MedicinalProductDetail';
import PharmaceuticalProductDetail from './components/PharmaceuticalProductDetail';
import SubstanceDetail from './components/SubstanceDetail';
import '@fortawesome/fontawesome-free/css/all.min.css';

const App = () => {
    return (
        <Router>
            <div>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/medicinal_products" element={<MedicinalProductList />} />
                    <Route path="/pharmaceutical_products" element={<PharmaceuticalProductList />} />
                    <Route path="/substances" element={<SubstanceList />} />
                    <Route path="/pzn/:pzn" element={<MedicinalProductDetail />} />
                    <Route path="/pharmaceutical_product/:key" element={<PharmaceuticalProductDetail />} />
                    <Route path="/substance_id/:key" element={<SubstanceDetail />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;
