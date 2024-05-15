import streamlit as st
import os
import requests


BASE_URL = "http://127.0.0.1:5000"

def search_courses_documents(query,language):
    url = BASE_URL + "/recommend_courses"   # Replace this with your URL
    data = {"prompt": query,
            "language":language}  # Assuming your API expects the query in a JSON format
    headers = {"Content-Type": "application/json"}  # Specifying JSON content type

    # Making the POST request
    response = requests.post(url, json=data, headers=headers)
    print(response)
    # Checking if the request was successful
    if response.status_code == 200:
        # Returning the JSON response
        return response.json()
    else:
        # If the request was not successful, print the status code and response content
        print("Error:", response.status_code, response.content)
        return None  # Or handle the error in a way that suits your application



def search_jobs_documents(query):
    url = BASE_URL + "/recommend_jobs"   # Replace this with your URL
    data = {"prompt": query}  # Assuming your API expects the query in a JSON format
    headers = {"Content-Type": "application/json"}  # Specifying JSON content type

    # Making the POST request
    response = requests.post(url, json=data, headers=headers)
    print(response)
    # Checking if the request was successful
    if response.status_code == 200:
        # Returning the JSON response
        return response.json()
    else:
        # If the request was not successful, print the status code and response content
        print("Error:", response.status_code, response.content)
        return None  # Or handle the error in a way that suits your application


# Streamlit App
st.title("HMI Search Engine")

# Add a dropdown menu for selecting document types
document_types = ["Jobs","Courses"]
selected_document_type = st.selectbox("Select document type:", document_types)


if selected_document_type == "Courses":
    languages = ["en","de"]
    selected_language = st.selectbox("Select language:", languages)
    
# Get the query
query = st.text_input("Enter your search query:")

if st.button("Search"):  # Add the button
    # Pass the selected document type and query to the search function
    if selected_document_type == "Courses" and selected_language:
        results = search_courses_documents(query,selected_language)  # Move search execution inside button logic 
        recommendations = results["recommendations"]
        scores = results["scores"]
        if selected_language == "de":
            directory = "data\\courses\\zqm_modul\\de\\"
        elif selected_language == "en": 
            directory = "data\\courses\\zqm_modul\\en\\"

    elif selected_document_type == "Jobs":
        results = search_jobs_documents(query)  
        directory = "data\\jobs_docs\\"
        recommendations = results["recommendations"]
        scores = results["scores"]
    if results:
        st.markdown("# Results:")
        for i in range(len(recommendations)):
            filepath = os.path.join(directory, recommendations[i])  # Combine path and filename
            filepath = str(filepath)
            with open(filepath, "rb") as f:
                file_data = f.read()
            st.download_button(label=f"{recommendations[i]};  Similarity Score: {scores[i]}", data=file_data, file_name=recommendations[i])

    else:
        st.write("No documents found matching your query.")