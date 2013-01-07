from flask import Flask, request, jsonify, render_template
from flask.views import MethodView
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///contacts.db"
db = SQLAlchemy(app)


class Contact(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    phone_number = db.Column(db.String(10))

    def __init__(self, **kwargs):
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.phone_number = kwargs.get('phone_number')

    def __repr__(self):
        return "<{0} {1}, {2}>".format(self.first_name, self.last_name, self.phone_number)

    def as_dict(self):
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "phone_number": self.phone_number}


@app.route("/")
def index():
    return render_template("index.html")


class ContactView(MethodView):
    """
    Simple CRUD view for contacts
    """

    def get(self, contact_id):
        if contact_id is None:
            # all contacts
            contacts = Contact.query.all()
            return jsonify(dict(contacts=[contact.as_dict() for contact in contacts]))
        else:
            contact = Contact.query.get(contact_id)
            if not contact:
                result = {}
            else:
                result = contact.as_dict()
            return jsonify(result)

    def post(self):
        contact = Contact(first_name=request.json['first_name'],
                          last_name=request.json['last_name'],
                          phone_number=request.json['phone_number']
                          )
        db.session.add(contact)
        db.session.commit()
        return jsonify({}, status=200)

    def put(self, contact_id):
        contact = Contact.query.get(contact_id)
        contact.first_name = request.json['first_name']
        contact.last_name = request.json['last_name']
        contact.phone_number = request.json['phone_number']
        db.session.commit()
        return jsonify({}, status=200)

    def delete(self, contact_id):
        contact = Contact.query.get(contact_id)
        db.session.delete(contact)
        db.session.commit()
        return jsonify({}, status=200)


contact_view = ContactView.as_view('contacts')
app.add_url_rule('/contacts/', defaults={'contact_id': None},
                 view_func=contact_view, methods=['GET',])
app.add_url_rule('/contacts/', view_func=contact_view, methods=['POST',])
app.add_url_rule('/contacts/<int:contact_id>', view_func=contact_view, methods=['GET', 'PUT', 'DELETE'])


if __name__ == '__main__':
    app.run(debug=True)
