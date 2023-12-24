from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/your_database_name'
db = SQLAlchemy(app)

# Define Location model
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    province_id = db.Column(db.Integer, db.ForeignKey('province.id'), nullable=True)
    province = db.relationship('Province', backref=db.backref('locations', lazy=True))

# Define Province model
class Province(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    headquarters = db.Column(db.String(100), nullable=True)

# Routes for CRUD operations
@app.route('/provinces', methods=['GET'])
def get_provinces():
    provinces = Province.query.all()
    province_list = [
        {'id': province.id, 'name': province.name, 'headquarters': province.headquarters}
        for province in provinces
    ]
    return jsonify(province_list)

@app.route('/provinces/<int:province_id>', methods=['GET'])
def get_province(province_id):
    province = Province.query.get_or_404(province_id)
    return jsonify({'id': province.id, 'name': province.name, 'headquarters': province.headquarters})

@app.route('/provinces', methods=['POST'])
def create_province():
    data = request.json
    new_province = Province(
        name=data['name'],
        headquarters=data.get('headquarters', '')
    )
    db.session.add(new_province)
    db.session.commit()
    return jsonify({'message': 'Province created successfully!'})

@app.route('/provinces/<int:province_id>', methods=['PUT'])
def update_province(province_id):
    province = Province.query.get_or_404(province_id)
    data = request.json
    province.name = data['name']
    province.headquarters = data.get('headquarters', '')
    db.session.commit()
    return jsonify({'message': 'Province updated successfully!'})

@app.route('/provinces/<int:province_id>', methods=['DELETE'])
def delete_province(province_id):
    province = Province.query.get_or_404(province_id)
    db.session.delete(province)
    db.session.commit()
    return jsonify({'message': 'Province deleted successfully!'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
