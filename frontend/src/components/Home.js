import React from 'react';
import MedicinalProductList from './MedicinalProductList';
import PharmaceuticalProductList from './PharmaceuticalProductList';
import SubstanceList from './SubstanceList';

const Home = () => {
    return (
        <div className="container">
            <h1>BfArM Data Explorer</h1>
            <h6>Eine Visualisierung der <a href="https://www.bfarm.de/DE/Arzneimittel/Arzneimittelinformationen/Referenzdatenbank/_node.html" target="_blank" rel="noopener noreferrer">
                BfArM  Referenzdatenbank für Fertigarzneimittel gemäß § 31b SGB V
            </a> </h6><p></p>
            <section>
                <MedicinalProductList />
            </section>
            <section>
                <PharmaceuticalProductList />
            </section>
            <section>
                <SubstanceList />
            </section>
        </div>
    );
};

export default Home;