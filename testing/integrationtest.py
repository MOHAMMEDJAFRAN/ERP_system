# integration_test.py
from data_processor import CRMStrategy, FinanceStrategy, SalesStrategy,HRStrategy, SupplyChainStrategy
from DataIngection import CSVDataIngestion


def test_integration():
    # Step 1: Ingest data
    csv_ingestion = CSVDataIngestion()
    data_frame = csv_ingestion.ingest_data('Data Set/sales_data.csv')

    if data_frame is None:
        print("Data ingestion failed.")
        return

    # Step 2: Process data
    sales_strategy = SalesStrategy()
    processed_data = sales_strategy.process_data(data_frame, period='monthly')

    if processed_data is None or processed_data[1].empty:
        print("Data processing failed.")
        return

    # Output processed data for visual inspection
    print("Processed Data:")
    print(processed_data[1])

    # Step 3: Generate reports (e.g., visualizations)
    fig = processed_data[0]
    if fig:
        fig.savefig('monthly_sales_report.png')
        print("Sales Report generated successfully.")
    else:
        print("Failed to generate report.")

# Sample integration testing
def test_HR_integration():
    # Data ingestion
    ingestion_context = CSVDataIngestion()
    data_frame = ingestion_context.ingest_data('Data Set/HRData.csv')

    if data_frame is None:
        print("Data ingestion failed.")
        return

    # Data processing
    hr_strategy = HRStrategy()
    processed_data = hr_strategy.process_data(data_frame)


    print("Processed Data:")
    print(processed_data)
    # Assume some form of reporting or output
    print("HR Data reporting successful with", processed_data.shape[0], "records processed.")

    print("Full integration test passed.")

def test_finance_integration():
    # Step 1: Ingest data
    csv_ingestion = CSVDataIngestion()
    data_frame = csv_ingestion.ingest_data('Data Set/finance_data.csv')

    if data_frame is None:
        print("Data ingestion failed.")
        return

    # Step 2: Process data using Finance Strategy
    finance_strategy = FinanceStrategy()


    processed_data = finance_strategy.process_data(data_frame)

    if processed_data.empty:
        print("Data processing failed.")
        return

    # Output processed data for visual inspection
    print("Processed Data:")
    print(processed_data)

    # Optional: Generate and save a simple report or visualization if needed
    processed_data.to_csv('finance_report.csv', index=False)
    print("Finance report generated successfully.")

def test_crm_integration():
    # Step 1: Ingest data
    csv_ingestion = CSVDataIngestion()
    data_frame = csv_ingestion.ingest_data('Data Set/CRM_data.csv')

    if data_frame is None:
        print("Data ingestion failed.")
        return

    # Step 2: Process data using CRM Strategy
    crm_strategy = CRMStrategy()
    # Define parameters for processing
    # Note: Adjust these columns to match those that your CRM data actually contains
    selected_columns = ['invoiceID', 'invoice_date', 'customerID', 'country', 'quantity', 'amount']
    country_filter = 'USA'  # Example filter; change or remove based on your data context

    if country_filter:
        data_frame = data_frame[data_frame['country'] == country_filter]  # Apply country filter

    processed_data = crm_strategy.process_data(data_frame, columns=selected_columns)

    if processed_data.empty:
        print("Data processing failed.")
        return

    # Output processed data for visual inspection
    print("Processed Data:")
    print(processed_data)

    # Optional: Save processed data to a CSV for reporting
    processed_data.to_csv('crm_report.csv', index=False)
    print("CRM report generated successfully.")

def test_supply_chain_integration():
    # Step 1: Ingest data
    csv_ingestion = CSVDataIngestion()
    data_frame = csv_ingestion.ingest_data('Data Set/supply_chain.csv')

    if data_frame is None:
        print("Data ingestion failed.")
        return

    # Step 2: Process data using Supply Chain Strategy
    supply_chain_strategy = SupplyChainStrategy()
    # Define parameters for processing


    processed_data = supply_chain_strategy.process_data(data_frame)

    if processed_data.empty:
        print("Data processing failed.")
        return

    # Output processed data for visual inspection
    print("Processed Data:")
    print(processed_data)

    # Optional: Save processed data to a CSV for reporting
    processed_data.to_csv('supply_chain_report.csv', index=False)
    print("Supply Chain report generated successfully.")

if __name__ == "__main__":
    test_integration()
