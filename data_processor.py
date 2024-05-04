from abc import ABC, abstractmethod
import pandas as pd
import matplotlib.pyplot as plt
class DataProcessor(ABC):
    @abstractmethod
    def process_data(self, data, **kwargs):

        pass
class CRMStrategy(DataProcessor):
    def process_data(self, data, **kwargs):
        # Ensure data is a DataFrame or load it from a CSV file path
        if isinstance(data, pd.DataFrame):
            df = data
        else:
            df = pd.read_csv(data)

        # Validate required columns
        required_columns = {'invoiceID', 'invoice_date', 'customerID', 'country', 'quantity', 'amount'}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing columns: {', '.join(missing_columns)} in DataFrame")

        # Convert 'invoice_date' to datetime and ensure 'year' column
        df['invoice_date'] = pd.to_datetime(df['invoice_date'])

        # Check if 'year' column already exists to avoid duplicate insertion
        if 'year' not in df.columns:
            df['year'] = df['invoice_date'].dt.year

        # Optional filtering based on given parameters
        if 'country' in kwargs:
            df = df[df['country'] == kwargs['country']]
        # Define aggregation logic for numeric fields
        aggregation_rules = {
            'quantity': 'sum',
            'amount': 'sum'
        }

        # Determine which columns to display, default to displaying required columns
        selected_columns = kwargs.get('columns', list(required_columns) + ['year'])

        # Apply aggregation if 'year' is selected, otherwise use raw data
        if 'year' in selected_columns:
            # Group by year and other selected columns, applying aggregation rules
            df = df.groupby(['year'] + [col for col in selected_columns if col not in aggregation_rules]).agg(
                aggregation_rules).reset_index()
        else:
            # Display without aggregation if 'year' is not selected
            df = df[selected_columns]

        return df

class FinanceStrategy(DataProcessor):
    def process_data(self, data, **kwargs):
        if isinstance(data, pd.DataFrame):
            df = data
        else:
            df = pd.read_csv(data)

        selected_columns = kwargs.get('columns', df.columns.tolist())
        sort_by = kwargs.get('sort_by', selected_columns[0] if selected_columns else 'Brand')

        if selected_columns:
            df = df[selected_columns]

        return df.sort_values(by=sort_by, ascending=True)

class HRStrategy(DataProcessor):
    def process_data(self, data, **kwargs):
        # Assume 'data' is already a DataFrame
        selected_columns = kwargs.get('columns', data.columns.tolist())
        if 'columns' in kwargs and any(col not in data.columns for col in kwargs['columns']):
            raise ValueError("One or more selected columns are not in the DataFrame")
        return data[selected_columns].sort_values(by=selected_columns[0], ascending=True)

class SalesStrategy(DataProcessor):
    def process_data(self, data, period='monthly'):
        if 'Order Date' not in data.columns:
            raise ValueError("DataFrame must contain an 'Order Date' column")
        data['Order Date'] = pd.to_datetime(data['Order Date'])

        data['week'] = data['Order Date'].dt.isocalendar().week
        data['month'] = data['Order Date'].dt.month
        data['year'] = data['Order Date'].dt.year

        if period == 'weekly':
            return self.plot_weekly(data), data
        elif period == 'monthly':
            return self.plot_monthly(data), data

    def plot_weekly(self, data):
        # Group data by week and aggregate quantities and revenue
        weekly_sales = data.groupby(['year', 'week']).agg({
            'Quantity Ordered': 'sum',
            'Price Each': lambda x: (x * data.loc[x.index, 'Quantity Ordered']).sum()
        }).reset_index()

        # Creating a period column for better x-axis labeling
        weekly_sales['period'] = weekly_sales['year'].astype(str) + '-W' + weekly_sales['week'].astype(str)

        # Plot configuration
        fig, ax = plt.subplots(figsize=(12, 6))  # Specify the figure size

        # Check if data is not empty
        if not weekly_sales.empty:
            # Creating bar plots
            ax.bar(weekly_sales['period'], weekly_sales['Quantity Ordered'], width=0.4, label='Quantity Ordered',
                   align='center')
            ax.bar(weekly_sales['period'], weekly_sales['Price Each'], width=0.4, label='Revenue', color='red',
                   bottom=weekly_sales['Quantity Ordered'])

            ax.set_xlabel('Week')
            ax.set_ylabel('Values')
            ax.set_title('Weekly Sales Analysis')
            ax.legend()

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45, ha='right')
        else:
            # Display message if no data is available
            ax.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center',
                    transform=ax.transAxes)

        plt.tight_layout()  # Adjust layout to make room for rotated x-axis labels
        return fig

    def plot_monthly(self, data):
        # Aggregate the data by year and month
        monthly_sales = data.groupby(['year', 'month']).agg({
            'Quantity Ordered': 'sum',
            'Price Each': lambda x: (x * data.loc[x.index, 'Quantity Ordered']).sum()
        }).reset_index()

        # Create a period column for plotting
        monthly_sales['period'] = monthly_sales['year'].astype(str) + '-' + monthly_sales['month'].astype(str)

        # Initialize the figure and primary axis
        fig, ax1 = plt.subplots()

        if not monthly_sales.empty:
            # Plot Quantity Ordered on the primary y-axis
            color = 'tab:blue'
            ax1.set_xlabel('Month')
            ax1.set_ylabel('Quantity Ordered', color=color)
            ax1.plot(monthly_sales['period'], monthly_sales['Quantity Ordered'], label='Quantity Ordered', color=color)
            ax1.tick_params(axis='y', labelcolor=color)

            # Adjusting the month ticks
            ax1.set_xticks(monthly_sales['period'][::len(monthly_sales) // 12 + 1])  # Reduce tick density
            ax1.tick_params(axis='x', rotation=45)  # Rotate labels for better readability

            # Create a second y-axis for the Revenue
            ax2 = ax1.twinx()
            color = 'tab:red'
            ax2.set_ylabel('Revenue', color=color)
            ax2.plot(monthly_sales['period'], monthly_sales['Price Each'], label='Revenue', color=color)
            ax2.tick_params(axis='y', labelcolor=color)

            # Add titles and legends
            ax1.set_title('Monthly Sales Analysis')
            lines, labels = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines + lines2, labels + labels2, loc='upper left')
        else:
            # Display a message if there's no data
            ax1.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center',
                     transform=ax1.transAxes)

        plt.tight_layout()  # Automatically adjust subplot parameters to give specified padding
        plt.show()

        # Return the figure object for further manipulation if needed
        return fig

class SupplyChainStrategy(DataProcessor):
    def process_data(self, data, **kwargs):
        # If 'data' is a file path, read the CSV, else assume 'data' is a DataFrame
        if isinstance(data, str):
            df = pd.read_csv(data)
        else:
            df = data

        # Get selected columns or default to all columns
        selected_columns = kwargs.get('columns', df.columns.tolist())

        # Sort by the first selected column or a default column if provided
        sort_by = kwargs.get('sort_by', selected_columns[0] if selected_columns else 'Brand')

        # Return the DataFrame sorted by the specified column
        return df[selected_columns].sort_values(by=sort_by, ascending=True)
