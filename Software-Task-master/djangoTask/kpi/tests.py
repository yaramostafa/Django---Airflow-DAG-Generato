from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APIClient
from .models import KPI, AssetKPI
from django.db import IntegrityError
import sqlite3

class KPIModelTest(TestCase):
    def setUp(self):
        """Setup test data for KPI model."""
        self.kpi_data = {
            'name': 'Test KPI',
            'expression': 'ATTR * 2',
            'description': 'A test KPI'
        }
        self.kpi = KPI.objects.create(**self.kpi_data)

    def test_kpi_creation(self):
        """Test KPI model creation."""
        kpi = KPI.objects.get(id=self.kpi.id)
        self.assertEqual(kpi.name, self.kpi_data['name'])
        self.assertEqual(kpi.expression, self.kpi_data['expression'])
        self.assertEqual(kpi.description, self.kpi_data['description'])

    def test_kpi_str(self):
        """Test the string representation of the KPI model."""
        self.assertEqual(str(self.kpi), 'Test KPI')


class AssetKPIModelTest(TestCase):
    def setUp(self):
        """Setup test data for AssetKPI model."""
        self.kpi = KPI.objects.create(name='Test KPI', expression='ATTR * 2', description='A test KPI')
        self.asset_id = 'asset123'
        self.asset_kpi = AssetKPI.objects.create(asset_id=self.asset_id, kpi=self.kpi)

    def test_asset_kpi_creation(self):
        """Test AssetKPI model creation and relation."""
        asset_kpi = AssetKPI.objects.get(id=self.asset_kpi.id)
        self.assertEqual(asset_kpi.asset_id, self.asset_id)
        self.assertEqual(asset_kpi.kpi, self.kpi)

    def test_asset_kpi_str(self):
        """Test the string representation of the AssetKPI model."""
        self.assertEqual(str(self.asset_kpi), f"Asset {self.asset_id} linked to Test KPI")


class APIEndpointsTest(TestCase):
    def setUp(self):
        """Setup test client."""
        self.client = APIClient()

    def test_kpi_list_create_endpoint(self):
        """Test the KPI list and create endpoint."""
        response = self.client.get('/api/kpi/kpis/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_kpi_data = {
            'name': 'New EQ',
            'expression': 'ATTR * 4',
            'description': 'A newly created Mathematical equation'
        }
        response = self.client.post('/api/kpi/kpis/', new_kpi_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], new_kpi_data['name'])
