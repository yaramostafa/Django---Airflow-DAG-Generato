import sqlite3

def view_database(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM processed_data")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    connection.close()


def get_expression(asset_id):
    """
    This function retrieves the 'expression' for a given 'asset_id' from the database.
    It joins the 'kpi_kpi' and 'kpi_assetkpi' tables based on the 'kpi_id' and 'asset_id'
    to fetch the corresponding 'expression' value. If the 'asset_id' is found, it returns
    the expression as a string, otherwise, it returns None.
    """
    connection = sqlite3.connect("djangoTask/processed_data.db")
    cursor = connection.cursor()
    cursor.execute("""
            SELECT kpi_kpi.expression
            FROM kpi_kpi
            JOIN kpi_assetkpi ON kpi_kpi.id = kpi_assetkpi.kpi_id
            WHERE kpi_assetkpi.asset_id = ?
        """, (asset_id,))

    result = cursor.fetchone()  # Fetch a single result

    if result:
        # Access the first element of the tuple and strip any surrounding whitespace
        expression = result[0].strip() if isinstance(result[0], str) else result[0]
        return expression
    else:
        return None


if __name__ == "__main__":
    view_database("processed_data.db")

