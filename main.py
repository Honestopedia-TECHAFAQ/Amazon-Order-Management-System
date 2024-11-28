import streamlit as st
import pandas as pd
import sqlite3

DB_FILE = 'amazon_orders.db'


def ensure_columns():
    """Ensure that 'note' and 'dispatch' columns exist in the 'orders' table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(orders)")
    columns = [info[1] for info in cursor.fetchall()]

    if 'note' not in columns:
        cursor.execute("ALTER TABLE orders ADD COLUMN note TEXT")
    if 'dispatch' not in columns:
        cursor.execute("ALTER TABLE orders ADD COLUMN dispatch TEXT DEFAULT 'unshipped'")

    conn.commit()
    conn.close()


def recreate_table(df):
    """Recreate the orders table and insert data."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS orders")
    columns_with_types = ", ".join([f'"{col}" TEXT' for col in df.columns])
    create_table_query = f"CREATE TABLE orders ({columns_with_types}, note TEXT, dispatch TEXT DEFAULT 'unshipped')"
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()


def insert_data(df):
    """Insert data into the orders table."""
    conn = sqlite3.connect(DB_FILE)
    df['note'] = None
    df['dispatch'] = 'unshipped'
    df.to_sql('orders', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()


def load_data():
    """Load data from the orders table."""
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql('SELECT * FROM orders', conn)
    conn.close()
    return df


def update_note_by_product_name(product_name, note):
    """Update the note for a specific product name."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('UPDATE orders SET note = ? WHERE "product-name" = ?', (note, product_name))
    conn.commit()
    conn.close()


def update_dispatch_status(product_name, dispatch_status):
    """Update the dispatch status for a specific product name."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('UPDATE orders SET dispatch = ? WHERE "product-name" = ?', (dispatch_status, product_name))
    conn.commit()
    conn.close()


def delete_order_by_product_name(product_name):
    """Delete a specific order by product name."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM orders WHERE "product-name" = ?', (product_name,))
    conn.commit()
    conn.close()


def get_column_names():
    """Fetch column names dynamically from the 'orders' table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(orders)")
    columns = [info[1] for info in cursor.fetchall()]
    conn.close()
    return columns


def main():
    st.title("Amazon Order Management System")
    ensure_columns()

    # Sidebar menu for uploading files and managing orders
    st.sidebar.header("Manage Orders")
    sidebar_menu = st.sidebar.radio("Select an action:", ["Upload Orders", "Edit Orders", "Delete Orders"])

    if sidebar_menu == "Upload Orders":
        uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "xlsx", "txt"])

        if uploaded_file:
            file_type = uploaded_file.name.split(".")[-1]
            try:
                if file_type == "csv":
                    df = pd.read_csv(uploaded_file)
                elif file_type == "xlsx":
                    df = pd.read_excel(uploaded_file)
                elif file_type == "txt":
                    df = pd.read_csv(uploaded_file, delimiter="\t")

                st.subheader("File Preview")
                st.write(df.head())

                # Recreate the table and insert data into the database
                recreate_table(df)
                insert_data(df)
                st.success("Data stored in the database!")

            except Exception as e:
                st.error(f"Error: {e}")

    try:
        orders = load_data()
        st.subheader("View Orders")
        columns = get_column_names()
        st.write(f"Columns available: {', '.join(columns)}")

        if not orders.empty:
            st.dataframe(orders)
        else:
            st.warning("No products found in the database.")
    except Exception as e:
        st.error(f"Failed to load orders: {e}")

    if sidebar_menu == "Edit Orders":
        st.subheader("Edit Order")
        product_name_input = st.text_input("Enter Product Name to edit:")
        if product_name_input:
            try:
                orders_found = orders[orders['product-name'] == product_name_input.strip()]

                if not orders_found.empty:
                    st.write("Product Details:")
                    st.write(orders_found)

                    note = st.text_area("Enter note to add/update:")
                    dispatch_status = st.selectbox("Dispatch Status", ["shipped", "unshipped"])

                    if st.button("Update Order"):
                        if note or dispatch_status:
                            if note:
                                update_note_by_product_name(product_name_input, note)
                            if dispatch_status:
                                update_dispatch_status(product_name_input, dispatch_status)
                            st.success(f"Order updated for Product: '{product_name_input}'")

                            orders = load_data()
                            st.write("Updated Data:")
                            st.write(orders)
                        else:
                            st.error("Please enter valid note or dispatch status.")
                else:
                    st.warning("No exact match found for the product name provided.")

            except Exception as e:
                st.error(f"Error: {e}")

    if sidebar_menu == "Delete Orders":
        st.subheader("Delete Order")
        product_name_input = st.text_input("Enter Product Name to delete:")
        if product_name_input:
            try:
                orders_found = orders[orders['product-name'] == product_name_input.strip()]

                if not orders_found.empty:
                    st.write("Product Details:")
                    st.write(orders_found)

                    if st.button("Delete Order"):
                        delete_order_by_product_name(product_name_input)
                        st.success(f"Order with Product '{product_name_input}' has been deleted.")

                        orders = load_data()
                        st.write("Updated Data:")
                        st.write(orders)
                else:
                    st.warning("No exact match found for the product name provided.")

            except Exception as e:
                st.error(f"Error: {e}")


if __name__ == "__main__":
    main()
