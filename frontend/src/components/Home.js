import React from 'react';
import MedicinalProductList from './MedicinalProductList';
import PharmaceuticalProductList from './PharmaceuticalProductList';
import SubstanceList from './SubstanceList';

const Home = () => {
    return (
        <div className="container">
            <h1>Welcome to BfArM Data Explorer</h1>
            <section>
                <h2>Medizinisches Produkt</h2>
                <MedicinalProductList />
            </section>
            <section>
                <h2>Pharmaceutical Products</h2>
                <PharmaceuticalProductList />
            </section>
            <section>
                <h2>Substances</h2>
                <SubstanceList />
            </section>
        </div>
    );
};

export default Home;