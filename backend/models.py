import pandas as pd
import os
import zipfile
from typing import List, Optional

class MedicinalProduct:
    def __init__(self, key: int, pzn: int, count_substance: int, multiple_ppt: int, 
                 put_short: str, put_long: str, name: str, term_id: int):
        self.key = key
        self.pzn = pzn
        self.count_substance = count_substance
        self.multiple_ppt = multiple_ppt
        self.put_short = put_short
        self.put_long = put_long
        self.name = name
        self.term_id = term_id
        self.pharmaceutical_products = []  # List of PharmaceuticalProduct objects

    def add_pharmaceutical_product(self, product):
        self.pharmaceutical_products.append(product)


class PharmaceuticalProduct:
    def __init__(self, key: str, medicinal_product_key: int, number: int, put_short: str, 
                 put_long: str, name: str, term_id: int, description: str):
        self.key = key
        self.medicinal_product_key = medicinal_product_key
        self.number = number
        self.put_short = put_short
        self.put_long = put_long
        self.name = name
        self.term_id = term_id
        self.description = description
        self.substances = []  # List of Substance objects

    def add_substance(self, substance):
        self.substances.append(substance)


class Substance:
    def __init__(self, key: str, pharmaceutical_product_key: str, name: str, 
                 strength: str, substance_id: int, rank: int):
        self.key = key
        self.pharmaceutical_product_key = pharmaceutical_product_key
        self.name = name
        self.strength = strength
        self.substance_id = substance_id
        self.rank = rank


class BfarmData:
    def __init__(self, zip_file_path, extraction_dir):
        self.zip_file_path = zip_file_path
        self.extraction_dir = extraction_dir
        self.medicinal_products = {}
        self.pharmaceutical_products = {}
        self.substances = {}
        self.load_data()

    def load_data(self):
        # Define the paths to the extracted files
        medicinal_product_path = os.path.join(self.extraction_dir, '20240617-REFERENCE_MEDICINAL_PRODUCT.dsv')
        pharmaceutical_product_path = os.path.join(self.extraction_dir, '20240617-REFERENCE_PHARMACEUTICAL_PRODUCT.dsv')
        substance_path = os.path.join(self.extraction_dir, '20240617-REFERENCE_SUBSTANCE.dsv')

        # Extract the contents of the zip file if not already extracted
        if not all(os.path.exists(path) for path in [medicinal_product_path, pharmaceutical_product_path, substance_path]):
            with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(self.extraction_dir)

        # Load the data into pandas dataframes
        medicinal_product_df = pd.read_csv(medicinal_product_path, sep='|')
        pharmaceutical_product_df = pd.read_csv(pharmaceutical_product_path, sep='|')
        substance_df = pd.read_csv(substance_path, sep='|')

        # Populate the MedicinalProduct data
        for _, row in medicinal_product_df.iterrows():
            mp = MedicinalProduct(
                key=row['RMP_KEY'],
                pzn=row['RMP_PZN'],
                count_substance=row['RMP_COUNT_SUBSTANCE'],
                multiple_ppt=row['RMP_MULTIPLE_PPT'],
                put_short=row['RMP_PFM_PUT_SHORT'],
                put_long=row['RMP_PFM_PUT_LONG'],
                name=row['RMP_PFM_NAME'],
                term_id=row['RMP_PFM_TERM_ID']
            )
            self.medicinal_products[mp.key] = mp

        # Populate the PharmaceuticalProduct data
        for _, row in pharmaceutical_product_df.iterrows():
            pp = PharmaceuticalProduct(
                key=row['RPP_KEY'],
                medicinal_product_key=row['RMP_KEY'],
                number=row['RPP_NUMBER'],
                put_short=row['RPP_PFM_PUT_SHORT'],
                put_long=row['RPP_PFM_PUT_LONG'],
                name=row['RPP_PFM_NAME'],
                term_id=row['RPP_PFM_TERM_ID'],
                description=row['RPP_DESCRIPTION']
            )
            self.pharmaceutical_products[pp.key] = pp
            if pp.medicinal_product_key in self.medicinal_products:
                self.medicinal_products[pp.medicinal_product_key].add_pharmaceutical_product(pp)

        # Populate the Substance data
        for _, row in substance_df.iterrows():
            sub = Substance(
                key=row['RSE_KEY'],
                pharmaceutical_product_key=row['RPP_KEY'],
                name=row['RSE_SUBSTANCE_NAME'],
                strength=row['RSE_SUBSTANCE_STRENGTH'],
                substance_id=row['RSE_SUBSTANCE_ID'],
                rank=row['RSE_SUBSTANCE_RANK']
            )
            self.substances[sub.key] = sub
            if sub.pharmaceutical_product_key in self.pharmaceutical_products:
                self.pharmaceutical_products[sub.pharmaceutical_product_key].add_substance(sub)

    def get_medicinal_product_by_pzn(self, pzn):
        for mp in self.medicinal_products.values():
            if str(mp.pzn) == str(pzn):
                return mp
        return None

    def get_products_by_substance(self, substance_name):
        results = []
        for sub in self.substances.values():
            if substance_name.lower() in sub.name.lower():
                product = self.pharmaceutical_products.get(sub.pharmaceutical_product_key)
                if product and product not in results:
                    results.append(product)
        return results
