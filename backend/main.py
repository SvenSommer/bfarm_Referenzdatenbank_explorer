from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from models import BfarmData

app = Flask(__name__, static_folder='../static', template_folder='../templates')
CORS(app)
# Initialize BfarmData
data = BfarmData(zip_file_path='./data/20240617-REFERENCE.zip', extraction_dir='./data/20240617-REFERENCE')

@app.route('/pzn/<pzn>', methods=['GET'])
def get_medicinal_product(pzn):
    result = data.get_medicinal_product_by_pzn(pzn)
    if result:
        return jsonify({
            "key": result.key,
            "pzn": result.pzn,
            "count_substance": result.count_substance,
            "multiple_ppt": result.multiple_ppt,
            "put_short": result.put_short,
            "put_long": result.put_long,
            "name": result.name,
            "term_id": result.term_id,
            "pharmaceutical_products": [{
                "key": pp.key,
                "number": pp.number,
                "put_short": pp.put_short,
                "put_long": pp.put_long,
                "name": pp.name,
                "term_id": pp.term_id,
                "description": pp.description,
                "substances": [{
                    "key": sub.key,
                    "name": sub.name,
                    "strength": sub.strength,
                    "substance_id": sub.substance_id,
                    "rank": sub.rank,
                    "link": f"/substance/{sub.key}"
                } for sub in pp.substances],
                "link": f"/pharmaceutical_product/{pp.key}"
            } for pp in result.pharmaceutical_products],
            "link": f"/pzn/{result.pzn}"
        })
    else:
        return jsonify({"error": "PZN not found"}), 404


def paginate(queryset, page, per_page):
    total_items = len(queryset)
    total_pages = (total_items + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    return {
        "items": queryset[start:end],
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": page,
        "per_page": per_page
    }

@app.route('/medicinal_products', methods=['GET'])
def list_medicinal_products():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    products = [
        {
            "key": mp.key,
            "pzn": mp.pzn,
            "count_substance": mp.count_substance,
            "multiple_ppt": mp.multiple_ppt,
            "put_short": mp.put_short,
            "put_long": mp.put_long,
            "name": mp.name,
            "term_id": mp.term_id,
            "link": f"/pzn/{mp.pzn}"
        } for mp in data.medicinal_products.values()
    ]
    return jsonify(paginate(products, page, per_page))

@app.route('/pharmaceutical_products', methods=['GET'])
def list_pharmaceutical_products():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    products = [
        {
            "key": pp.key,
            "medicinal_product_key": pp.medicinal_product_key,
            "number": pp.number,
            "put_short": pp.put_short,
            "put_long": pp.put_long,
            "name": pp.name,
            "term_id": pp.term_id,
            "description": pp.description,
            "link": f"/pharmaceutical_product/{pp.key}"
        } for pp in data.pharmaceutical_products.values()
    ]
    return jsonify(paginate(products, page, per_page))

@app.route('/substances', methods=['GET'])
def list_substances():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    # Verwende ein Set, um doppelte Einträge zu vermeiden
    unique_substances = {}
    
    for sub in data.substances.values():
        if sub.substance_id not in unique_substances:
            unique_substances[sub.substance_id] = {
                "name": sub.name,
                "substance_id": sub.substance_id,
                "link": f"/substance_id/{sub.substance_id}"
            }

    substances_list = list(unique_substances.values())
    
    return jsonify(paginate(substances_list, page, per_page))


@app.route('/pharmaceutical_product/<key>', methods=['GET'])
def get_pharmaceutical_product(key):
    product = data.pharmaceutical_products.get(key)
    if product:
        return jsonify({
            "key": product.key,
            "medicinal_product_key": product.medicinal_product_key,
            "number": product.number,
            "put_short": product.put_short,
            "put_long": product.put_long,
            "name": product.name,
            "term_id": product.term_id,
            "description": product.description,
            "substances": [{
                "key": sub.key,
                "name": sub.name,
                "strength": sub.strength,
                "substance_id": sub.substance_id,
                "rank": sub.rank,
                "link": f"/substance/{sub.key}"
            } for sub in product.substances],
            "link": f"/pharmaceutical_product/{product.key}"
        })
    else:
        return jsonify({"error": "Pharmaceutical product not found"}), 404

@app.route('/substance_key/<key>', methods=['GET'])
def get_substance(key):
    substance = data.substances.get(key)
    if substance:
        return jsonify({
            "key": substance.key,
            "pharmaceutical_product_key": substance.pharmaceutical_product_key,
            "name": substance.name,
            "strength": substance.strength,
            "substance_id": substance.substance_id,
            "rank": substance.rank,
            "link": f"/substance/{substance.key}"
        })
    else:
        return jsonify({"error": "Substance not found"}), 404
    
@app.route('/substance_id/<substance_id>', methods=['GET'])
def get_pharmaceutical_products_by_substance_id(substance_id):
    substance_products = [
        {
            "pharmaceutical_product_key": sub.pharmaceutical_product_key,
            "description": data.pharmaceutical_products[sub.pharmaceutical_product_key].description,
            "strength": sub.strength,
            "link": f"/pharmaceutical_product/{sub.pharmaceutical_product_key}"
        }
        for sub in data.substances.values() if sub.substance_id == int(substance_id)
    ]
    
    if substance_products:
        # Der Name des Wirkstoffs wird aus dem ersten gefundenen Substanzdatensatz entnommen
        substance_name = next(sub.name for sub in data.substances.values() if sub.substance_id == int(substance_id))
        return jsonify({
            "substance_name": substance_name,
            "pharmaceutical_products": substance_products
        })
    else:
        return jsonify({"error": "Substance not found"}), 404


@app.route('/')
def index():
    return "Welcome to the Bfarm Data Explorer!"

if __name__ == '__main__':
    app.run(debug=True)
