import streamlit as st
from data_processor import HRStrategy, FinanceStrategy, SalesStrategy, SupplyChainStrategy, CRMStrategy
from DataIngection import CSVDataIngestion

def load_strategy(module):
    """ Load the appropriate strategy based on the selected module. """
    strategy_map = {
        'HR': HRStrategy(),
        'Finance': FinanceStrategy(),
        'Sales': SalesStrategy(),
        'Supply Chain': SupplyChainStrategy(),
        'CRM': CRMStrategy(),
    }
    return strategy_map[module]

def main():
    st.title('Data Processing Application')
    module = st.sidebar.selectbox('Select a Module', ['HR', 'Finance', 'Sales', 'Supply Chain', 'CRM'])
    data_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

    if data_file is not None:
        ingestion_context = CSVDataIngestion()
        # Ingest data using the strategy
        df = ingestion_context.ingest_data(data_file)

        if df is not None:
            strategy = load_strategy(module)
            if module == 'Supply Chain':
                # Specific handling for Supply Chain data
                selected_columns = st.multiselect('Select Columns', df.columns.tolist(), default=df.columns.tolist())
                sort_by = st.selectbox('Sort by', selected_columns)
                if st.button('Analyze Supply Chain Data'):
                    processed_data = strategy.process_data(df, columns=selected_columns, sort_by=sort_by)
                    st.dataframe(processed_data)

            elif module == 'Sales':
                period = st.sidebar.selectbox('Choose the analysis period', ['weekly', 'monthly'])
                if st.button('Analyze Sales'):
                    fig, processed_data = strategy.process_data(df, period=period)
                    if fig:
                        st.pyplot(fig)
                    if not processed_data.empty:
                        st.write(f'{period.capitalize()} Sales Data:', processed_data)
                    else:
                        st.error("No data available for this period.")


            elif module == 'CRM':

                # Handling for CRM with specific column selections

                columns = st.multiselect('Select Columns', df.columns.tolist(),
                                         default=['invoiceID', 'invoice_date', 'customerID', 'country', 'quantity',
                                                  'amount'])

                country = st.selectbox('Filter by Country (Optional):',
                                       ['All'] + sorted(df['country'].dropna().unique().tolist()))

                if country != 'All':
                    df = df[df['country'] == country]  # Apply country filter before passing to strategy

                if st.button('Analyze CRM Data'):

                    processed_data = strategy.process_data(df, columns=columns)

                    if not processed_data.empty:

                        st.write("Aggregated CRM Data:", processed_data)

                    else:

                        st.error("No data available after filtering. Please adjust your selections.")

            elif module == 'Finance':
                selected_columns = st.multiselect('Select Columns', df.columns.tolist(), default=df.columns.tolist())
                sort_by = st.selectbox('Sort by', selected_columns)
                if st.button('Analyze Finance Data'):
                    # Process and display finance data
                    processed_data = strategy.process_data(df, columns=selected_columns, sort_by=sort_by)
                    st.dataframe(processed_data)

            else:
                # General handling for other modules
                columns = st.multiselect('Select Columns', df.columns.tolist(), default=df.columns.tolist())
                if st.button('Process Data'):
                    processed_data = strategy.process_data(df, columns=columns)
                    if not processed_data.empty:
                        st.table(processed_data)
                    else:
                        st.error("No data available after processing.")


if __name__ == "__main__":
    main()
