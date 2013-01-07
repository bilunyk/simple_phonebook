import app as myapp
from unittest import TestCase
from flask import json


class ContactTest(TestCase):

    def setUp(self):
        myapp.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = myapp.app.test_client()
        myapp.db.create_all()

    def test_index(self):
        resp = self.app.get('/')
        self.assertEquals(resp.status_code, 200)

    def _create_contact(self, data):
        resp = self.app.post('/contacts/',
                             content_type='application/json',
                             data=json.dumps(data),
                             headers=[('X-Requested-With', 'XMLHttpRequest')])
        return resp

    def test_create_contact(self):
        resp = self._create_contact({'first_name': 'john', 'last_name': 'dou', 'phone_number': '050'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(json.loads(resp.data).get('status'), 200)
        resp = self.app.get('/contacts/',
                            content_type='application/json',
                            headers=[('X-Requested-With', 'XMLHttpRequest')])
        self.assertEquals(resp.status_code, 200)
        contacts = json.loads(resp.data).get('contacts')
        self.assertEquals(len(contacts), 1)
        self.assertEquals(contacts[0]['first_name'], 'john')
        self.assertEquals(contacts[0]['last_name'], 'dou')
        self.assertEquals(contacts[0]['phone_number'], '050')

    def test_update_contact(self):
        self._create_contact({'first_name': 'john', 'last_name': 'dou', 'phone_number': '050'})
        resp = self.app.put('/contacts/1',
                            content_type='application/json',
                            data=json.dumps({'first_name': 'eric', 'last_name': 'dowson', 'phone_number': '072'}),
                            headers=[('X-Requested-With', 'XMLHttpRequest')])
        self.assertEquals(resp.status_code, 200)
        resp = self.app.get('/contacts/',
                            content_type='application/json',
                            headers=[('X-Requested-With', 'XMLHttpRequest')])
        contacts = json.loads(resp.data).get('contacts')
        self.assertEquals(len(contacts), 1)
        self.assertEquals(contacts[0]['first_name'], 'eric')
        self.assertEquals(contacts[0]['last_name'], 'dowson')
        self.assertEquals(contacts[0]['phone_number'], '072')

    def test_delete_contact(self):
        self._create_contact({'first_name': 'john', 'last_name': 'dou', 'phone_number': '050'})
        resp = self.app.delete('/contacts/1',
                            content_type='application/json',
                            headers=[('X-Requested-With', 'XMLHttpRequest')])
        self.assertEquals(resp.status_code, 200)
        resp = self.app.get('/contacts/',
                            content_type='application/json',
                            headers=[('X-Requested-With', 'XMLHttpRequest')])
        contacts = json.loads(resp.data).get('contacts')
        self.assertEquals(len(contacts), 0)

    def tearDown(self):
        myapp.db.drop_all()
