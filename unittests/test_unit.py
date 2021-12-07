import base64
import unittest
from unittest import TestCase
from unittest.mock import patch, Mock, ANY
from base64 import b64encode
from flask import url_for
from flask_bcrypt import generate_password_hash
from flask_testing import TestCase
from sqlalchemy.testing import db

from lab_8.api_methods import app
from lab_8.api_methods import auth, Session, jsonify
from lab_8.models import User, Location, Ad, Base, engine
from lab_8.app import app as api


class TestGreeting(unittest.TestCase):
    def test_hello(self):
        client = api.test_client()
        response = client.get('/api/v1/hello-world-3')
        self.assertEqual(response.status_code, 200)


class TestBaseCase(unittest.TestCase):
    def setUp(self):
        #self.create_tables()

        self.location_1_data = {
            "name": "Town"
        }

        self.location_2_data = {
            "name": "City"
        }

        self.location_new_json = "{\n \"name\":\"Kyiv\" \n}"
        self.location_invalid_json = "{\n \"name\":\"Kyiv\", \"city\":\"ABC\" \n}"
        self.location_existing_json = "{\n \"name\":\"Town\" \n}"
        self.location_wrong_json = "{\n \n}"
        self.location_with_id_json = "{\n \"id\":30, \"name\":\"Kyiv\" \n}"

        self.ad_without_name_json = "{\n \"text\":\"Sell smth\", \"price\": \"123.56\", \"currency\":\"USD\", \"date\":\"2019-05-17\" \n}"
        self.ad_without_price_json = "{\n \"name\":\"Sell shoes\", \"text\":\"Sell smth\", \"currency\":\"USD\", \"date\":\"2019-05-17\" \n}"
        self.ad_without_currency_json = "{\n \"name\":\"Sell shoes\", \"text\":\"Sell smth\", \"price\": \"123.56\", \"date\":\"2019-05-17\" \n}"
        self.ad_without_date_json = "{\n \"name\":\"Sell shoes\", \"text\":\"Sell smth\", \"price\": \"123.56\", \"currency\":\"USD\" \n}"
        self.ad_with_id_json = "{\n \"id\":\"4\", \"name\":\"Sell shoes\", \"text\":\"Sell smth\", \"price\": \"123.56\", \"currency\":\"USD\", \"date\":\"2019-05-17\" \n}"
        self.ad_with_invalid_location_json = "{\n \"name\":\"Sell shoes\", \"text\":\"Sell smth\", \"price\": \"123.56\", \"currency\":\"USD\", \"date\":\"2019-05-17\", \"locationId\": \"1000\" \n}"
        self.ad_json = "{\n \"name\":\"Sell shoes\", \"text\":\"Sell smth\", \"price\": \"123.56\", \"currency\":\"USD\", \"date\":\"2019-05-17\" \n}"

        self.user_existing_username_json = "{\n \"username\": \"Yaryna\", \"email\": \"qwer5ty@gmail.com\", \"password\": \"12345\", \"locationId\": 1 \n}"
        self.user_existing_email_json = "{\n \"username\": \"Yaryn\", \"email\": \"qwerty@gmail.com\", \"password\": \"12345\", \"locationId\": 1 \n}"
        self.user_invalid_location_json = "{\n \"username\": \"Yaryna\", \"email\": \"qwerty@gmail.com\", \"password\": \"12345\", \"locationId\": 90 \n}"
        self.user_without_password_json = "{\n \"username\": \"Ana\", \"email\": \"qwer324ty@gmail.com\", \"password\": \"\",\"locationId\": 1 \n}"
        self.user_invalid_json = "{\n \"username\": 1, \"email\": 1, \"password\": \"12345678\",\"locationId\": 1 \n}"
        self.user_json = "{\n \"username\": \"Ana\", \"email\": \"qwer324ty@gmail.com\", \"password\": \"12345678\",\"locationId\": 1 \n}"
        self.user_update_json = "{\n \"username\":\"Yaryna123\", \"email\":\"123qwerty@gmail.com\" \n}"

        session = Session()
        location_1 = Location(**self.location_1_data)
        session.add(location_1)
        location_2 = Location(**self.location_2_data)
        session.add(location_2)
        session.commit()

        self.user_1_data = {
            "username": "Yaryna",
            "email": "qwerty@gmail.com",
            "password": "12345",
            "locationId": 1
        }

        self.user_1_data_hashed = {
            **self.user_1_data,
            "password": generate_password_hash(self.user_1_data["password"])
        }
        self.user_1_credentials = base64.b64encode(b'Yaryna:12345').decode("utf-8")
        self.user_wrong_credentials = base64.b64encode(b'Mary:123345').decode("utf-8")

        self.user_2_data = {
            "username": "Mia",
            "email": "a@gmail.com",
            "password": "1233",
            "locationId": 1
        }
        self.user_2_data_hashed = {
            **self.user_2_data,
            "password": generate_password_hash(self.user_2_data["password"])
        }

        self.user_2_credentials = base64.b64encode(b'Mia:1233').decode("utf-8")

        self.ad_1_data = {
            "name": "Sell shoes",
            "text": "Sell smth",
            "price": "123.56",
            "currency": "USD",
            "date": "2019-05-17",
            "userId": 1
        }

    def tearDown(self):
        self.close_session()
        # Base.metadata.drop_all(engine)

    # def create_tables(self):
    #     Base.metadata.create_all(bind=engine)

    def close_session(self):
        Session().close()
    #
    # def create_app(self):
    #     return app
    #
    # def get_auth_headers(self, credentials):
    #     response = self.client.post(url_for("auth"), json=credentials)


class TestUser(TestBaseCase):
    def test_create_user(self):
        client = app.test_client()
        session = Session()
        first_user = User(**self.user_1_data_hashed)
        session.add(first_user)
        session.commit()

        first_headers = {
            'Authorization': 'Basic ' + self.user_1_credentials
        }
        headers = {'Content-Type': 'application/json'}
        response = client.post('/api/v1/user')
        self.assertEqual(response.status_code, 400)

        response = client.post('/api/v1/user', headers=headers, data=self.user_existing_username_json)
        self.assertEqual(response.status_code, 400)

        response = client.post('/api/v1/user', headers=headers, data=self.user_existing_email_json)
        self.assertEqual(response.status_code, 400)

        response = client.post('/api/v1/user', headers=headers, data=self.user_invalid_location_json)
        self.assertEqual(response.status_code, 400)

        response = client.post('/api/v1/user', headers=headers, data=self.user_without_password_json)
        self.assertEqual(response.status_code, 400)

        response = client.post('/api/v1/user', headers=headers, data=self.user_invalid_json)
        self.assertEqual(response.status_code, 422)

        response = client.post('/api/v1/user', headers=headers, data=self.user_json)
        self.assertEqual(response.status_code, 200)

        session.delete(first_user)
        session.commit()

    def test_get_user(self):
        client = app.test_client()
        session = Session()
        first_user = User(**self.user_1_data_hashed)
        session.add(first_user)
        second_user = User(**self.user_2_data_hashed)
        session.add(second_user)
        session.commit()

        first_headers = {
            'Authorization': 'Basic ' + self.user_1_credentials
        }
        second_headers = {
            'Authorization': 'Basic ' + self.user_2_credentials
        }

        response = client.get('/api/v1/user/Yar', headers=first_headers)
        self.assertEqual(response.status_code, 404)

        response = client.get('/api/v1/user/Mia', headers=first_headers)
        self.assertEqual(response.status_code, 403)

        response = client.get('/api/v1/user/Yaryna', headers=first_headers)
        self.assertEqual(response.status_code, 200)

        session.delete(first_user)
        session.delete(second_user)
        session.commit()

    def test_update_user(self):
        client = app.test_client()
        session = Session()
        first_user = User(**self.user_1_data_hashed)
        session.add(first_user)
        session.commit()
        first_headers = {
            'Authorization': 'Basic ' + self.user_1_credentials
        }
        wrong_headers = {
            'Authorization': 'Basic ' + self.user_wrong_credentials
        }
        headers = {'Content-Type': 'application/json'}

        response = client.put('/api/v1/user/Ana', headers=first_headers, data=None)
        self.assertEqual(response.status_code, 400)

        response = client.put('/api/v1/user/Ana', headers=first_headers, json=self.user_update_json)
        self.assertEqual(response.status_code, 403)

        response = client.put(f'/api/v1/user/Yaryna', headers=first_headers, data=self.user_update_json)
        self.assertEqual(response.status_code, 400)
        #
        # response = client.put(f'/api/v1/user/Yaryna', headers=first_headers, json=self.user_update_json)
        # self.assertEqual(response.status_code, 400)

        session.delete(first_user)
        session.commit()

    def test_delete_user(self):
        client = app.test_client()
        session = Session()
        first_user = User(**self.user_1_data_hashed)
        session.add(first_user)
        session.commit()

        first_headers = {
            'Authorization': 'Basic ' + self.user_1_credentials
        }

        response = client.delete('/api/v1/user/Kate', headers=first_headers)
        self.assertEqual(response.status_code, 404)

        response = client.delete('/api/v1/user/Ana', headers=first_headers)
        self.assertEqual(response.status_code, 403)

        response = client.delete('/api/v1/user/Yaryna', headers=first_headers)
        self.assertEqual(response.status_code, 200)

        session.delete(first_user)
        session.commit()


class TestAd(TestBaseCase):
    def test_create_ad(self):
        client = app.test_client()
        session = Session()
        first_user = User(**self.user_1_data_hashed)
        session.add(first_user)
        session.commit()

        first_headers = {
            'Authorization': 'Basic ' + self.user_1_credentials
        }

        response = client.post('/api/v1/ad', headers=first_headers)
        self.assertEqual(response.status_code, 400)

        response = client.post('/api/v1/ad', headers=first_headers, json=self.ad_without_name_json)
        self.assertEqual(response.status_code, 400)

        response = client.post('/api/v1/ad', headers=first_headers, json=self.ad_without_price_json)
        self.assertEqual(response.status_code, 400)

        response = client.post('/api/v1/ad', headers=first_headers, json=self.ad_without_currency_json)
        self.assertEqual(response.status_code, 400)

        response = client.post('/api/v1/ad', headers=first_headers, json=self.ad_without_date_json)
        self.assertEqual(response.status_code, 400)

        response = client.post('/api/v1/ad', headers=first_headers, json=self.ad_with_id_json)
        self.assertEqual(response.status_code, 401)
        # ##
        # response = client.post('/api/v1/ad', headers=first_headers, data=self.ad_with_invalid_location_json)
        # self.assertEqual(response.status_code, 404)
        # ##
        response = client.post('/api/v1/ad', headers=first_headers, json=self.ad_json)
        self.assertEqual(response.status_code, 422)

        session.delete(first_user)
        session.commit()

    def test_get_ad(self):
        client = app.test_client()
        session = Session()
        first_user = User(**self.user_1_data_hashed)
        session.add(first_user)
        # first_ad = Ad(**self.ad_1_data)
        # session.add(first_ad)
        session.commit()

        first_headers = {
            'Authorization': 'Basic ' + self.user_1_credentials
        }

        response = client.get('/api/v1/ad/90')
        self.assertEqual(response.status_code, 404)

        # session.delete(first_ad)
        session.delete(first_user)
        session.commit()

    def test_update_ad(self):
        client = app.test_client()
        session = Session()
        first_user = User(**self.user_1_data_hashed)
        session.add(first_user)
        session.commit()

        first_headers = {
            'Authorization': 'Basic ' + self.user_1_credentials
        }

        response = client.put('/api/v1/ad/1', headers=first_headers)
        self.assertEqual(response.status_code, 400)

        response = client.put('/api/v1/ad/1', headers=first_headers, data=self.ad_json)
        self.assertEqual(response.status_code, 400)

        session.delete(first_user)
        session.commit()

    def test_delete_ad(self):
        client = app.test_client()
        session = Session()
        first_user = User(**self.user_1_data_hashed)
        session.add(first_user)
        # ad = Ad(**self.ad_1_data)
        # session.add(ad)
        session.commit()

        first_headers = {
            'Authorization': 'Basic ' + self.user_1_credentials
        }

        response = client.delete('/api/v1/ad/8', headers=first_headers)
        self.assertEqual(response.status_code, 404)

        # response = client.delete('/api/v1/ad/2', headers=first_headers)
        # self.assertEqual(response.status_code, 403)

        session.delete(first_user)
        session.commit()


class TestService(TestBaseCase):
    def test_get_public_ads(self):
        client = app.test_client()
        response = client.get('/api/v1/service/ads')
        self.assertEqual(response.status_code, 200)

    def test_get_ads_for_user(self):
        client = app.test_client()
        session = Session()
        first_user = User(**self.user_1_data_hashed)
        session.add(first_user)
        second_user = User(**self.user_2_data_hashed)
        session.add(second_user)
        session.commit()

        first_headers = {
            'Authorization': 'Basic ' + self.user_1_credentials
        }

        second_headers = {
            'Authorization': 'Basic ' + self.user_2_credentials
        }

        response = client.get('/api/v1/service/user/1000', headers=first_headers)
        self.assertEqual(response.status_code, 404)
        #
        # response = client.get(f'/api/v1/service/user/{second_user.id}', headers=first_headers)
        # self.assertEqual(response.status_code, 403)

        response = client.get('/api/v1/service/user/1', headers=first_headers)
        self.assertEqual(response.status_code, 200)


        session.delete(first_user)
        session.delete(second_user)
        session.commit()

    def test_get_locations(self):
        client = app.test_client()
        response = client.get('/api/v1/service/locations')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {
                "id": ANY,
                "name": "Town"
            },
            {
                "id": ANY,
                "name": "Town"
            },
            {
                "id": ANY,
                "name": "City"
            }
        ])


class TestLocation(TestBaseCase):
    def test_create_location(self):
        client = app.test_client()
        session = Session()
        first_user = User(**self.user_1_data_hashed)
        session.add(first_user)
        session.commit()

        first_headers = {
            'Authorization': 'Basic ' + self.user_1_credentials
        }
        headers = {'Content-Type': 'application/json'}

        wrong_headers = {
            'Authorization': 'Basic ' + self.user_wrong_credentials
        }

        response = client.post('/api/v1/location', headers=first_headers)
        self.assertEqual(response.status_code, 400)

        response = client.post('/api/v1/location', headers=first_headers, json=self.location_wrong_json)
        self.assertEqual(response.status_code, 400)

        response = client.post('/api/v1/location', headers=first_headers, json=self.location_with_id_json)
        self.assertEqual(response.status_code, 401)

        response = client.post('/api/v1/location', headers=first_headers, data=self.location_existing_json)
        self.assertEqual(response.status_code, 400)

        # response = client.post('/api/v1/location', headers=first_headers, data=self.location_invalid_json)
        # self.assertEqual(response.status_code, 422)
        #
        response = client.post('/api/v1/location', headers=first_headers, data=self.location_new_json)
        self.assertEqual(response.status_code, 400)

        session.delete(first_user)
        session.commit()
