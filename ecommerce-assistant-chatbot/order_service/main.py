from fastapi import FastAPI, HTTPException, Query
import mock_api
import pandas as pd

app = FastAPI(title="Order Service")

@app.get("/orders")
async def get_orders(
    customer_id: int = Query(None, description="Filter by customer ID"),
    category: str = Query(None, description="Filter by product category"),
    start_date: str = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(None, description="End date (YYYY-MM-DD)")
):
    """
    Retrieve orders with optional filters: customer_id, category, date range.
    """
    # Start with all orders
    orders_df = mock_api.get_all_orders().copy()

    # Apply customer filter if provided
    if customer_id is not None:
        filtered = orders_df[orders_df['Customer_Id'] == customer_id]
        orders_df = filtered

    # Apply product category filter if provided
    if category:
        filtered = orders_df[orders_df['Product_Category'].str.lower() == category.lower()]
        orders_df = filtered

    # Apply date range filter if both dates provided
    if start_date and end_date:
        # Ensure date column is datetime
        orders_df['Order_Date'] = pd.to_datetime(orders_df['Order_Date'])
        mask = (orders_df['Order_Date'] >= start_date) & (orders_df['Order_Date'] <= end_date)
        orders_df = orders_df[mask]

    # If no results found, return empty list
    if orders_df.empty:
        return {"orders": []}

    # Convert to list of dicts for JSON response
    orders_list = orders_df.to_dict(orient='records')
    return {"orders": orders_list}
