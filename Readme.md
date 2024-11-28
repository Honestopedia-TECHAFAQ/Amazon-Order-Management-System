# Amazon Order Management - Streamlit App

## Overview

This is a simple web application built using  **Streamlit** ,  **SQLite** , and **Pandas** to manage Amazon orders. The app allows you to:

* **Import orders** from a CSV file.
* **View orders** in a filtered list.
* **Edit orders** (add, update, or delete).
* **Export orders** to CSV or Excel.
* **Log actions** for audit purposes.
* **Filter orders** based on various criteria like product name, status, quantity, and price.

The application is designed to help users manage and track orders efficiently, making it suitable for small-scale order management tasks.

## Features

### 1. **Import Orders**

* Allows uploading of a CSV file containing order details.
* Automatically adds new orders that aren't already in the system.
* Validates the data (checks for valid price, quantity, and tracking number).
* Logs the import action.

### 2. **View Orders**

* Displays a table of all orders in a user-friendly way.
* Supports filtering based on:
  * Product Name
  * Order Status (Unshipped, Shipped)
  * Quantity (min/max)
  * Price (min/max)

### 3. **Edit Orders**

* Allows adding new orders or editing existing ones.
* Edit details like:
  * Product Name
  * Quantity
  * Price
  * Tracking Number
  * Order Status
* Logs the edit or addition action.

### 4. **Export Orders**

* Provides the option to export orders to either a CSV or Excel file.

### 5. **Action Logs**

* Keeps a log of all actions performed (e.g., importing, editing, saving orders) with timestamps.
* Logs are stored in a separate SQLite table.

### 6. **Session State**

* Uses `Streamlit` session state to keep track of the current state (orders, logs, etc.) between app reruns.

## Requirements

* Python 3.8+
* `streamlit`
* `pandas`
* `sqlite3`

You can install the required Python packages with:

`pip install streamlit pandas`

## Setup

### 1. **Clone or Download the Code**

* Clone the repository or download the code into your local machine.

### 2. **Database Setup**

* The app automatically creates an SQLite database called `orders.db` if it doesn't exist.
* The database contains two tables: `orders` for storing order data and `logs` for storing action logs.

### 3. **Running the App**

* Open a terminal and navigate to the directory containing the script.
* Run the following command:

`pip install -r requirements.txt `

`streamlit run app.py  `

`or`

`py -m streamlit run main.py`

This will start the Streamlit server and open the app in your default web browser.

## How to Use the App

1. **Import Orders**
   * Navigate to the "Import Orders" section on the sidebar.
   * Upload a CSV file containing the following columns:
     * `Order ID`
     * `Product Name`
     * `Quantity`
     * `Price`
     * `Tracking Number`
     * `Status` (Unshipped, Shipped)
2. **Filter Orders**
   * Use the "Advanced Search Filters" section in the sidebar to filter orders by:
     * Product Name
     * Order Status
     * Quantity (Min/Max)
     * Price (Min/Max)
3. **Edit Orders**
   * Select an order to edit by choosing its Order ID from the "Edit Order" section.
   * Modify the order details and click "Save Order" to save the changes.
4. **Export Orders**
   * Export the filtered orders list by selecting the file type (CSV or Excel) in the "Export Orders" section.
   * The app provides a download button to download the exported file.
5. **Action Logs**
   * All actions like importing orders, editing orders, and saving changes are logged in the SQLite database and can be used for audit purposes.

## File Structure

* `app.py`: Main Streamlit application file.
* `orders.db`: SQLite database to store orders and logs.
* `exported_orders.csv`: (Optional) Generated file when exporting orders.
* `exported_orders.xlsx`: (Optional) Generated file when exporting orders.

## Database Tables

1. **Orders Table**
   * `Order ID`: Unique identifier for each order (primary key).
   * `Product Name`: Name of the product.
   * `Quantity`: Quantity of the product ordered.
   * `Price`: Price of the product.
   * `Tracking Number`: Tracking number for the shipment.
   * `Status`: Order status (Unshipped, Shipped).
2. **Logs Table**
   * `Timestamp`: The date and time of the action.
   * `Action`: The type of action performed (e.g., "Imported Orders", "Edited Order").
   * `Order ID`: The associated order ID (if applicable).
   * `User`: The user who performed the action (admin, for now).

## Troubleshooting

* **Error during Import** : Ensure that the CSV file is in the correct format. The required columns are: `Order ID`, `Product Name`, `Quantity`, `Price`, `Tracking Number`, `Status`.
* **Order ID already exists** : If you attempt to import orders with an existing Order ID, the app will only import new, unique orders.
* **Missing Columns** : The app checks for the validity of the columns in the CSV file. Ensure all required columns are present.

## Contributing

Feel free to fork the repository, create branches, and submit pull requests with bug fixes, new features, or improvements.
