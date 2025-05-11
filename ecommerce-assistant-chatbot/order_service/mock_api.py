import pandas as pd

# Load the order dataset once
df_orders = pd.read_csv("Order_Data_Dataset.csv", parse_dates=['Order_Date'])

def get_all_orders():
    """
    Return the entire orders DataFrame.
    """
    return df_orders

def get_orders_by_customer(customer_id: int):
    """
    Return orders for a specific customer ID.
    """
    return df_orders[df_orders['Customer_Id'] == customer_id]

def get_orders_by_category(category: str):
    """
    Return orders for a specific product category (case-insensitive).
    """
    mask = df_orders['Product_Category'].str.lower() == category.lower()
    return df_orders[mask]

def get_orders_by_date_range(start_date: str, end_date: str):
    """
    Return orders where Order_Date is between start_date and end_date (inclusive).
    Dates should be in 'YYYY-MM-DD' format.
    """
    # Ensure Order_Date is datetime (already parsed)
    mask = (df_orders['Order_Date'] >= start_date) & (df_orders['Order_Date'] <= end_date)
    return df_orders[mask]
