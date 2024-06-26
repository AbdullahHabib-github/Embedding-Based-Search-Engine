import streamlit as st
import os
import requests
from langdetect import detect


BASE_URL = "http://127.0.0.1:5000"

def search_de_courses_documents(query):
    url = BASE_URL + "/recommend_de_courses"   # Replace this with your URL
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



def search_en_courses_documents(query):
    url = BASE_URL + "/recommend_en_courses"   # Replace this with your URL
    data = {"prompt": query,}  # Assuming your API expects the query in a JSON format
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
st.title("Human Machine Interaction")

st.markdown("### Course Search Engine")

st.markdown("\n\n\n\n\n\n\n\n")

# if selected_document_type == "Courses":
# languages = ["en","de"]
# selected_language = st.selectbox("Select language:", languages)
    
# Get the query
selected_language = None
query = st.text_input("Enter the Course Details:")
if query:
    selected_language = detect(query)
    if selected_language != "de":
        selected_language = "en"

if selected_language and query and st.button("Search"):  # Add the button
    # Pass the selected document type and query to the search function
    if selected_language == "de":
        directory = "data\\courses\\zqm_modul\\de\\"
        results = search_de_courses_documents(query)  # Move search execution inside button logic 

    elif selected_language == "en": 
        directory = "data\\courses\\zqm_modul\\en\\"
        results = search_en_courses_documents(query)  # Move search execution inside button logic 

    recommendations = results["recommendations"]
    # print(recommendations)
    scores = results["scores"]

    if results:
        st.markdown("# Maximum Similar Results")
        if selected_language == "de":
            st.code("The detected language is German")
        elif selected_language == "en":
            st.code("The detected language is English")   
        for i in range(len(recommendations)):
            filepath = os.path.join(directory, recommendations[i])  # Combine path and filename
            filepath = str(filepath)
            with open(filepath, "rb") as f:
                file_data = f.read()
            if scores[i]>0.80:
                color = "green-background"    
            elif scores[i] >0.77:
                color = "blue-background"    
            else:
                color = "red-background"    
            st.download_button(label=f":{color}[{recommendations[i]}]", data=file_data, file_name=recommendations[i])
            st.text(f"Similarity Score: {scores[i]}\n")
# blue, green, orange, red, violet, gray/grey, rainbow
    else:
        st.write("No documents found matching your query.")