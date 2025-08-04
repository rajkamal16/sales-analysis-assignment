import sqlite3
import pandas as pd

def run_pandas_version(db_path, output_csv):
    conn = sqlite3.connect(db_path)

    # Load tables
    customers = pd.read_sql_query("SELECT * FROM Customer WHERE age BETWEEN 18 AND 35", conn)
    sales = pd.read_sql_query("SELECT * FROM Sales", conn)
    orders = pd.read_sql_query("SELECT * FROM Orders", conn)
    items = pd.read_sql_query("SELECT * FROM Items", conn)

    # Merge tables
    merged = (
        customers
        .merge(sales, on='customer_id')
        .merge(orders, on='sales_id')
        .merge(items, on='item_id')
    )

    # Filter out NULL or zero quantities
    filtered = merged[merged['quantity'].notnull() & (merged['quantity'] > 0)]

    # Group by customer, age, item and sum quantity
    grouped = (
        filtered
        .groupby(['customer_id', 'age', 'item_name'], as_index=False)
        .agg({'quantity': 'sum'})
    )

    # Lowercase the item names
    grouped['item_name'] = grouped['item_name'].str.lower()

    # Rename columns to match output
    grouped.rename(columns={
        'customer_id': 'Customer',
        'age': 'Age',
        'item_name': 'Item',
        'quantity': 'Quantity'
    }, inplace=True)

    # Convert quantities to int (no decimals)
    grouped['Quantity'] = grouped['Quantity'].astype(int)

    # Save to CSV with semicolon delimiter
    grouped.to_csv(output_csv, sep=';', index=False)

    conn.close()
    print(f"Pandas version output saved to {output_csv}")

if __name__ == "__main__":
    run_pandas_version('database.db', 'output_pandas.csv')
