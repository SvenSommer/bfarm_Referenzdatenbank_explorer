import React from 'react';
import MedicinalProductList from './MedicinalProductList';
import PharmaceuticalProductList from './PharmaceuticalProductList';
import SubstanceList from './SubstanceList';

const Home = () => {
    return (
        <div className="container">
            <h1>BfArM Data Explorer</h1>
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