import sqlite3
import csv

def run_sql_version(db_path, output_csv):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    SELECT
        c.customer_id AS Customer,
        c.age AS Age,
        LOWER(i.item_name) AS Item,
        SUM(o.quantity) AS Quantity
    FROM Customer c
    JOIN Sales s ON c.customer_id = s.customer_id
    JOIN Orders o ON s.sales_id = o.sales_id
    JOIN Items i ON o.item_id = i.item_id
    WHERE c.age BETWEEN 18 AND 35
      AND o.quantity IS NOT NULL
    GROUP BY c.customer_id, c.age, i.item_name
    HAVING SUM(o.quantity) > 0
    ORDER BY c.customer_id, i.item_name;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    # Write to CSV with ';' delimiter
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Customer', 'Age', 'Item', 'Quantity'])
        writer.writerows(rows)

    conn.close()
    print(f"SQL version output saved to {output_csv}")

if __name__ == "__main__":
    run_sql_version('database.db', 'output_sql.csv')
