
import streamlit as st
import requests
import pandas as pd

API_URL = "http://fastapi_app:8000"

st.title("Product Management")

st.header("All Products")



if st.button("View Products"):
    res = requests.get(f"{API_URL}/products")

    if res.status_code == 200:
        df = pd.DataFrame(res.json())
        st.dataframe(df)
    else:
        st.error("Failed to fetch products")



st.header("Add Product")

id = st.number_input("ID", min_value=1, step=1)
name = st.text_input("Name")
description = st.text_input("Description")
price = st.number_input("Price", min_value=0.0)
quantity = st.number_input("Quantity", min_value=0, step=1)

if st.button("Add Product"):
    payload = {
        "id": int(id),
        "name": name,
        "description": description,
        "price": float(price),        
        "quantity": int(quantity)     
    }

    res = requests.post(f"{API_URL}/products", json=payload)

    if res.status_code == 200:
        st.success("Product added!")
    else:
        st.error(res.text)

st.header("Delete Product")

delete_id = st.number_input("Enter ID to Delete", min_value=1, step=1)

if st.button("Delete Product"):
    res = requests.delete(f"{API_URL}/products/{delete_id}")

    if res.status_code == 200:
        st.success("Product deleted successfully!")
    elif res.status_code == 404:
        st.error(" Product not found")
    else:
        st.error(f" Error: {res.json().get('detail', 'Something went wrong')}")

