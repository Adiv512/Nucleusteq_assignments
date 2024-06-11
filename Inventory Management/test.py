import pytest
from unittest.mock import patch, Mock
from flask import Flask
from app import app as flask_app ,is_valid_email # Adjust the import according to your actual app instance

class MockCursor:
    def __init__(self):
        self.results = []
        self.queries = []
        self.values = []

    def execute(self, query, params=None):
        self.queries.append(query)
        self.values.append(params)
        if "from assign where email=%s and type=%s" in query:
            if params == ('user@example.com', 'Laptop'):
                self.results = [('user@example.com', 'Laptop')]
            else:
                self.results = []
        elif "from inventory where mname=%s" in query:
            if params == ('Laptop',):
                self.results = [('Laptop', 'Details', 10)]
            else:
                self.results = []
        elif "insert into assign" in query:
            self.results = []

    def fetchall(self):
        return self.results

    def close(self):
        pass

class MockDBConnection:
    def cursor(self):
        return MockCursor()

    def commit(self):
        pass

    def close(self):
        pass

@pytest.fixture
def mock_db():
    with patch('app.pymysql.connect', return_value=MockDBConnection()):
        yield

@pytest.fixture
def client():
    flask_app.secret_key = 'many_random_bytes'
    with flask_app.test_client() as client:
        yield client


def test_landing_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Landing page accessed" in response.data

def test_user_login_page(client):
    response = client.get('/userlogin')
    assert response.status_code == 200
    assert b"User login Here" in response.data

def test_user_login_success(client, mock_db):
    response = client.post('/userlogin', data={'email': 'test@nucleusteq.com', 'phone': '12345'})
    assert response.status_code == 200
    assert b"user dashboard accessed" in response.data

def test_user_login_failure(client, mock_db):
    response = client.post('/userlogin', data={'email': 'invalid@nucleusteq.com', 'phone': '12345'})
    assert response.status_code == 200
    assert b"Invalid Login Credentials" in response.data

def test_registration_page(client):
    response = client.get('/registration')
    assert response.status_code == 200
    assert b"user registration dashboard" in response.data

def test_registration_success(client, mock_db):
    response = client.post('/registration', data={
        'id': '1', 'name': 'Test User', 'email': 'test@nucleusteq.com', 'phone': '12345', 'designation': 'Tester'
    })
    assert response.status_code == 302  # Redirect after successful registration

def test_registration_failure(client, mock_db):
    response = client.post('/registration', data={
        'id': '1', 'name': 'Test User', 'email': 'invalid_email', 'phone': '12345', 'designation': 'Tester'
    })
    assert response.status_code == 200
    assert b"Invalid Email Domain" in response.data

def test_admin_login_success(client, mock_db):
    response = client.post('/admin', data={'email': 'admin@nucleusteq.com', 'password': 'admin123'})
    assert response.status_code == 302  # Redirect after successful admin login

def test_admin_login_failure(client):
    response = client.post('/admin', data={'email': 'wrong@nucleusteq.com', 'password': 'wrongpassword'})
    assert response.status_code == 200
    assert b"Invalid Login Credentials" in response.data

def test_inventory_page(client):
    response = client.get('/index1')
    assert response.status_code == 200
    assert b"Inventory dashboard" in response.data

def test_add_inventory_item_success(client, mock_db):
    response = client.post('/insert1', data={
        'id': '1', 'name': 'Item 1', 'dop': '2023-01-01', 'bno': 'B123', 'warranty': '1 year', 'quantity': '10'
    })
    assert response.status_code == 302  # Redirect after successful inventory addition

def test_add_inventory_item_failure(client, mock_db):
    response = client.post('/insert1', data={
        'id': '1', 'name': 'Item 1', 'dop': '2023-01-01', 'bno': 'B123', 'warranty': '1 year', 'quantity': '10'
    })
    assert response.status_code == 200
    assert b"Already product ID Avaliable" in response.data

def test_is_valid_email():
    assert is_valid_email('test@nucleusteq.com')
    assert is_valid_email('test@nucleusteq.in')
    assert not is_valid_email('test@gmail.com')
    assert not is_valid_email('test@xyz.com')
    
def test_edit_inventory_item_success(client, mock_db):
    response = client.post('/edit1', data={
        'id': '1', 'name': 'Updated Item', 'dop': '2023-01-01', 'bno': 'B123', 'warranty': '2 years', 'quantity': '20'
    })
    assert response.status_code == 302  # Redirect after successful inventory edit

def test_edit_inventory_item_failure(client, mock_db):
    response = client.post('/edit1', data={
        'id': '2', 'name': 'Updated Item', 'dop': '2023-01-01', 'bno': 'B123', 'warranty': '2 years', 'quantity': '20'
    })
    assert response.status_code == 200
    assert b"Product ID not found" in response.data
    
def test_delete_inventory_item_success(client, mock_db):
    response = client.post('/delete1', data={'id': '1'})
    assert response.status_code == 302  # Redirect after successful inventory deletion

def test_delete_inventory_item_failure(client, mock_db):
    response = client.post('/delete1', data={'id': '2'})
    assert response.status_code == 200
    assert b"Product ID not found" in response.data
    
def test_add_employee_success(client, mock_db):
    response = client.post('/insert', data={
        'id': '1', 'name': 'John Doe', 'email': 'john.doe@nucleusteq.com', 'phone': '1234567890', 'designation': 'Engineer'
    })
    assert response.status_code == 302  # Redirect after successful employee addition

def test_add_employee_duplicate_email(client, mock_db):
    response = client.post('/insert', data={
        'id': '2', 'name': 'Jane Smith', 'email': 'jane.smith@nucleusteq.com', 'phone': '0987654321', 'designation': 'Manager'
    })
    assert response.status_code == 200
    assert b"Email Already Available" in response.data

def test_add_employee_invalid_email(client, mock_db):
    response = client.post('/insert', data={
        'id': '3', 'name': 'Mark Taylor', 'email': 'mark.taylor@invalid.com', 'phone': '1122334455', 'designation': 'Analyst'
    })
    assert response.status_code == 200
    assert b"Invalid Email Domain" in response.data
    
def test_delete_employee_success(client, mock_db):
    response = client.get('/delete', query_string={'id': '1'})
    assert response.status_code == 302  # Redirect after successful employee deletion

def test_delete_employee_failure(client, mock_db):
    response = client.get('/delete', query_string={'id': '9999'})
    assert response.status_code == 200
    assert b"Employee ID not found" in response.data
    
def test_edit_employee_success(client, mock_db):
    response = client.post('/update', data={
        't1': '1', 't2': 'John Doe Updated', 't3': 'john.updated@nucleusteq.com', 't4': '1234567890', 't5': 'Senior Engineer'
    })
    assert response.status_code == 302  # Redirect after successful employee edit

def test_edit_employee_failure(client, mock_db):
    response = client.post('/update', data={
        't1': '9999', 't2': 'Non Existent', 't3': 'non.existent@nucleusteq.com', 't4': '0000000000', 't5': 'Unknown'
    })
    assert response.status_code == 200
    assert b"Employee ID not found" in response.data
    
def test_allocate_inventory_success(client, mock_db):
    response = client.post('/allocateinventory', data={
        't1': 'user@example.com', 't2': 'Laptop'
    })
    assert response.status_code == 302  # Redirect after successful inventory allotment

def test_allocate_inventory_already_allotted(client, mock_db):
    response = client.post('/allocateinventory', data={
        't1': 'user@example.com', 't2': 'Laptop'
    })
    assert response.status_code == 200
    assert b"Already Allot" in response.data

def test_allocate_inventory_no_inventory(client, mock_db):
    response = client.post('/allocateinventory', data={
        't1': 'user@example.com', 't2': 'NonExistentItem'
    })
    assert response.status_code == 200
    assert b"No such inventory item" in response.data
    
def test_return_inventory_success(client, mock_db):
    response = client.get('/returnproduct', query_string={'id': 'user@example.com', 'product': 'Laptop'})
    assert response.status_code == 302  # Redirect after successful inventory return

def test_return_inventory_not_allotted(client, mock_db):
    response = client.get('/returnproduct', query_string={'id': 'user@example.com', 'product': 'NonExistentItem'})
    assert response.status_code == 200
    assert b"Inventory item not allotted to user" in response.data




if __name__ == "__main__":
    pytest.main()
