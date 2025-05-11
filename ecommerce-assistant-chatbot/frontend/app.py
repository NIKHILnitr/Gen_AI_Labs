import streamlit as st
import requests

st.set_page_config(page_title="E-commerce Dashboard", layout="wide")
st.title("🛍️ E-commerce Assistant Dashboard")

tabs = st.tabs(["🎸 Product Search", "📦 Order Lookup", "💬 Basic Chat"])

# ---------------- PRODUCT SERVICE ----------------
with tabs[0]:
    st.header("🎸 Search Products")

    query = st.text_input("Search query (e.g., guitar, microphone)")
    category = st.text_input("Product category (optional)")
    min_price = st.number_input("Minimum price", value=0.0)
    max_price = st.number_input("Maximum price", value=1000.0)
    limit = st.slider("Limit results", 1, 20, 5)

    if st.button("🔍 Search Products"):
        with st.spinner("Fetching product data..."):
            try:
                resp = requests.get(
                    "http://localhost:8001/search",
                    params={
                        "q": query,
                        "category": category,
                        "min_price": min_price,
                        "max_price": max_price,
                        "limit": limit
                    }
                )
                results = resp.json().get("results", [])
                if results:
                    for r in results:
                        st.markdown(f"""
                            **{r['title']}**  
                            💵 Price: ${r['price']}  
                            ⭐ Rating: {r['average_rating']} ({r['rating_number']} reviews)  
                            🏪 Store: {r['store']}  
                            🏷️ Category: {r['categories']}
                            ---
                        """)
                else:
                    st.info("No products found.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ---------------- ORDER SERVICE ----------------
with tabs[1]:
    st.header("📦 Check Your Orders")

    customer_id = st.text_input("Enter Customer ID", placeholder="e.g., 37077")

    if st.button("📬 Fetch Orders"):
        with st.spinner("Contacting order service..."):
            try:
                resp = requests.get("http://localhost:8002/orders", params={"customer_id": customer_id})
                orders = resp.json().get("orders", [])
                if orders:
                    for o in orders:
                        st.markdown(f"""
                            🗓️ Date: {o['Order_Date']}  
                            📦 Product: {o['Product']}  
                            💰 Sales: ${o['Sales']}  
                            🚚 Shipping: ${o['Shipping_Cost']}  
                            🔥 Priority: {o['Order_Priority']}
                            ---
                        """)
                else:
                    st.warning("No orders found for that customer ID.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ---------------- BASIC CHAT ----------------
with tabs[2]:
    st.header("💬 Basic Chatbot")

    if "history" not in st.session_state:
        st.session_state.history = []

    msg = st.chat_input("Say something...")

    if msg:
        st.session_state.history.append(("user", msg))

        # Simple logic or fallback response
        if "hello" in msg.lower():
            bot_response = "Hi there! 👋 How can I assist you today?"
        elif "product" in msg.lower():
            bot_response = "You can search for products in the first tab above."
        elif "order" in msg.lower():
            bot_response = "Use the second tab to check your orders!"
        else:
            bot_response = f"You said: {msg}"

        st.session_state.history.append(("bot", bot_response))

    for role, content in st.session_state.history:
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(content)



# import streamlit as st
# import requests

# st.set_page_config(page_title="E-commerce Chatbot", layout="centered")
# st.title("🛍️ E-commerce Assistant Chatbot")

# # Store chat history
# if "history" not in st.session_state:
#     st.session_state.history = []

# user_input = st.chat_input("Ask me something about products or your orders!")

# if user_input:
#     st.session_state.history.append(("user", user_input))

#     with st.spinner("Thinking..."):
#         response = requests.post(
#             "http://localhost:8003/chat",  # This should point to your running chat service
#             json={"query": user_input}
#         )
#         bot_reply = response.json()["answer"]
#         st.session_state.history.append(("bot", bot_reply))

# # Display chat history
# for role, msg in st.session_state.history:
#     with st.chat_message("user" if role == "user" else "assistant"):
#         st.markdown(msg)
