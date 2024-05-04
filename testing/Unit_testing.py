import unittest
from data_processor import FinanceStrategy, HRStrategy, SalesStrategy, SupplyChainStrategy
import pytest
import pandas as pd
from io import StringIO
from DataIngection import CSVDataIngestion

# Mock data for testing
CSV_DATA = """name,age
Alice,30
Bob,25"""

@pytest.fixture
def csv_file(tmpdir):
    file = tmpdir.join("data.csv")
    file.write(CSV_DATA)
    return file.strpath

# Examples of how to setup test cases
def test_csv_data_ingestion(csv_file):
    # Instantiate CSVDataIngestion and ingest data
    csv_ingestor = CSVDataIngestion()
    data = csv_ingestor.ingest_data(csv_file)
    # Check if DataFrame is created correctly
    assert not data.empty
    assert data.equals(pd.read_csv(StringIO(CSV_DATA)))


class TestHRStrategy(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'employeeID': [1, 2],
            'name': ['Alice', 'Bob'],
            'department': ['HR', 'Finance']
        })
        self.hr = HRStrategy()

    def test_hr_strategy_select_columns(self):
        result = self.hr.process_data(self.data, columns=['name', 'department'])
        self.assertTrue('name' in result.columns and 'department' in result.columns)
        self.assertFalse('employeeID' in result.columns)

    def test_hr_strategy_sorting(self):
        result = self.hr.process_data(self.data, columns=['name'], sort_by='name')
        self.assertEqual(result.iloc[0]['name'], 'Alice')

    def test_invalid_column(self):
        # Expecting an error if the column doesn't exist in DataFrame
        with self.assertRaises(ValueError):
            self.hr.process_data(self.data, columns=['nonexistent_column'])

class TestFinanceStrategy(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'Brand': ['Apple', 'Samsung'],
            'Revenue': [1000, 1500],
            'Units Sold': [50, 75]
        })
        self.finance = FinanceStrategy()

    def test_finance_strategy_select_and_sort(self):
        result = self.finance.process_data(self.data, columns=['Brand', 'Revenue'], sort_by='Revenue')
        self.assertEqual(result.iloc[0]['Brand'], 'Apple')  # Apple should come first after sorting by Revenue

class TestSalesStrategy(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'Order Date': ['2023-01-01', '2023-01-07'],
            'Quantity Ordered': [10, 20],
            'Price Each': [100, 200]
        })
        self.sales = SalesStrategy()

    def test_sales_data_preparation(self):
        _, result = self.sales.process_data(self.data, period='monthly')
        self.assertTrue('month' in result.columns)
        self.assertEqual(result.iloc[0]['month'], 1)

class TestSupplyChainStrategy(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'Product': ['Widget', 'Gadget'],
            'Brand': ['BrandA', 'BrandB'],
            'Stock': [50, 75]
        })
        self.supply_chain = SupplyChainStrategy()

    def test_supply_chain_sorting(self):
        result = self.supply_chain.process_data(self.data, sort_by='Stock')
        self.assertEqual(result.iloc[0]['Brand'], 'BrandA')  # Expect BrandA to be first after sorting by stock

if __name__ == '__main__':
    unittest.main()