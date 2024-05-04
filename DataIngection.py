import pandas as pd
from abc import ABC, abstractmethod

# Interface
class DataIngestionStrategy(ABC):
    @abstractmethod
    def ingest_data(self, file_path):
        """Ingest data from a file and return a DataFrame."""
        pass

# Concrete class for CSV files
class CSVDataIngestion(DataIngestionStrategy):
    def ingest_data(self, file_path):
        """Read data from a CSV file into a DataFrame."""
        try:
            data = pd.read_csv(file_path)
            print("Data ingestion successful.")
            return data
        except Exception as e:
            print(f"Failed to ingest data: {e}")
            return None

class JSONDataIngestion(DataIngestionStrategy):
    def ingest_data(self, file_path):
        with open(file_path, 'r') as file:
            data = json.loads(file)
        return data


# Context class to utilize strategies
class DataIngestionContext:
    def _init_(self, strategy: DataIngestionStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: DataIngestionStrategy):
        self.strategy = strategy

    def ingest_data(self, file_path):
        return self.strategy.ingest_data(file_path)