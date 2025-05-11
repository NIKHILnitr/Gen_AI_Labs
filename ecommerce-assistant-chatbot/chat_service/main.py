# from fastapi import FastAPI
# from pydantic import BaseModel
# import google.generativeai as genai
# import requests
# import os
# import re

# # Set your Gemini API key here
# os.environ["GOOGLE_API_KEY"] = "AIzaSyDj91EDOo7ixG9gqyZEBaPZWDpor4QjrcE"
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
# model = genai.GenerativeModel("gemini-pro")

# PRODUCT_SERVICE_URL = "http://localhost:8001"
# ORDER_SERVICE_URL = "http://localhost:8002"

# app = FastAPI(title="Chat Service")

# class ChatRequest(BaseModel):
#     query: str

# @app.post("/chat")
# def chat(request: ChatRequest):
#     query = request.query.lower()
#     prompt = ""

#     # ---------- Product Related ----------
#     if any(kw in query for kw in ["guitar", "microphone", "instrument", "product", "price", "rating"]):
#         try:
#             resp = requests.get(f"{PRODUCT_SERVICE_URL}/search", params={"q": query})
#             if resp.status_code != 200:
#                 raise Exception(resp.text)

#             products = resp.json().get("results", [])
#             if not products:
#                 return {"answer": "I couldn’t find any matching products."}

#             summary = "\n".join([
#                 f"{p['title']} (${p['price']}, {p['average_rating']}⭐)"
#                 for p in products[:5]
#             ])

#             prompt = f"The user asked: '{request.query}'.\nHere are top products:\n{summary}\nPlease generate a friendly recommendation."

#         except Exception as e:
#             return {"answer": f"Sorry, I couldn't fetch product info. Error: {str(e)}"}

#     # ---------- Order Related ----------
#     elif "order" in query or "customer" in query or "shipping" in query:
#         try:
#             match = re.search(r"\b\d{5}\b", query)
#             if not match:
#                 return {"answer": "Please provide a 5-digit customer ID to look up your order."}

#             customer_id = match.group()
#             resp = requests.get(f"{ORDER_SERVICE_URL}/orders", params={"customer_id": customer_id})
#             if resp.status_code != 200:
#                 raise Exception(resp.text)

#             orders = resp.json().get("orders", [])
#             if not orders:
#                 return {"answer": f"No orders found for customer ID {customer_id}."}

#             latest = orders[0]
#             prompt = (
#                 f"The user asked: '{request.query}'.\n"
#                 f"Latest order details:\n"
#                 f"- Date: {latest['Order_Date']}\n"
#                 f"- Product: {latest['Product']}\n"
#                 f"- Sales: ${latest['Sales']}\n"
#                 f"- Shipping: ${latest['Shipping_Cost']}\n"
#                 f"- Priority: {latest['Order_Priority']}\n"
#                 f"Generate a friendly response with this info."
#             )
#         except Exception as e:
#             return {"answer": f"Sorry, I couldn't fetch order details. Error: {str(e)}"}

#     else:
#         prompt = f"The user asked: '{request.query}'. Please respond like a friendly e-commerce assistant."

#     # ---------- Generate Gemini Response ----------
#     try:
#         reply = model.generate_content(prompt)
#         return {"answer": reply.text}
#     except Exception as e:
#         return {"answer": f"Failed to get Gemini response: {str(e)}"}






from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="Mini Chatbot")

# ✅ Small & fast model
chatbot = pipeline("text-generation", model="distilgpt2", max_new_tokens=50)

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
def chat(request: ChatRequest):
    result = chatbot(request.query)[0]["generated_text"]
    return {"answer": result}




# from fastapi import FastAPI
# from pydantic import BaseModel
# import requests
# import google.generativeai as genai
# import os
# import re

# # Set up Gemini API key
# os.environ["GOOGLE_API_KEY"] = "AIzaSyCG3tDZJpVT2F76bCYcLLd1vQaub2dNpLw"
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
# model = genai.GenerativeModel("gemini-pro")

# # Services
# PRODUCT_SERVICE_URL = "http://localhost:8001"
# ORDER_SERVICE_URL = "http://localhost:8002"

# app = FastAPI(title="Chat Service")

# class ChatRequest(BaseModel):
#     query: str

# @app.post("/chat")
# def chat(request: ChatRequest):
#     user_query = request.query.strip().lower()

#     prompt = ""

#     # -------- PRODUCT QUERIES -------- #
#     if any(word in user_query for word in ["guitar", "microphone", "product", "price", "rating"]):
#         try:
#             print("👉 Fetching from Product Service:", f"{PRODUCT_SERVICE_URL}/search?q={user_query}")
#             resp = requests.get(f"{PRODUCT_SERVICE_URL}/search", params={"q": user_query})
#             print("📦 Status:", resp.status_code)

#             if resp.status_code != 200:
#                 raise Exception(resp.text)

#             results = resp.json().get("results", [])
#             if not results:
#                 return {"answer": "I couldn't find any products matching your query."}

#             top_items = "\n".join([
#                 f"- {p['title']} (${p['price']}, {p['average_rating']}⭐)"
#                 for p in results[:5]
#             ])

#             prompt = f"You are an e-commerce assistant. The user asked: '{user_query}'.\nHere are top matching products:\n{top_items}\nGenerate a helpful, friendly response."

#         except Exception as e:
#             return {"answer": f"Sorry, I couldn't fetch product information. Error: {str(e)}"}

#     # -------- ORDER QUERIES -------- #
#     elif "order" in user_query or "customer" in user_query:
#         try:
#             customer_id_match = re.search(r"\b\d{5}\b", user_query)
#             if not customer_id_match:
#                 return {"answer": "Please provide your 5-digit Customer ID to check your orders."}
#             customer_id = int(customer_id_match.group(0))

#             print("👉 Fetching from Order Service:", f"{ORDER_SERVICE_URL}/orders?customer_id={customer_id}")
#             resp = requests.get(f"{ORDER_SERVICE_URL}/orders", params={"customer_id": customer_id})
#             print("📦 Status:", resp.status_code)

#             if resp.status_code != 200:
#                 raise Exception(resp.text)

#             orders = resp.json().get("orders", [])
#             if not orders:
#                 return {"answer": f"No orders found for customer ID {customer_id}."}

#             latest = orders[0]
#             prompt = (
#                 f"The user asked: '{user_query}'.\n"
#                 f"Latest order details:\n"
#                 f"- Date: {latest['Order_Date']}\n"
#                 f"- Product: {latest['Product']}\n"
#                 f"- Sales: ${latest['Sales']}\n"
#                 f"- Shipping: ${latest['Shipping_Cost']}\n"
#                 f"- Priority: {latest['Order_Priority']}\n"
#                 f"Please generate a helpful reply."
#             )
#         except Exception as e:
#             return {"answer": f"Sorry, I couldn't fetch order details. Error: {str(e)}"}

#     # -------- DEFAULT -------- #
#     else:
#         prompt = f"The user asked: '{user_query}'. Provide a helpful e-commerce answer."

#     # -------- GENERATE RESPONSE -------- #
#     try:
#         gemini_response = model.generate_content(prompt)
#         return {"answer": gemini_response.text}
#     except Exception as e:
#         return {"answer": f"Failed to generate response with Gemini: {str(e)}"}



