from flask import Flask, request, jsonify
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
import os
import docx2txt

app = Flask(__name__)

# Directories
course_directory_en = "data/courses/zqm_modul/en"
course_directory_de = "data/courses/zqm_modul/de"

# Course descriptions (dictionary and list)
course_descriptions = {}
course_descriptions_list = []

job_descriptions_list = []
job_directory = "data/jobs_docs"

# Initialize tokenizer and model (can be done outside for better performance)
tokenizer = AutoTokenizer.from_pretrained("thenlper/gte-large")
model = AutoModel.from_pretrained("thenlper/gte-large")

def load_course_descriptions(course_directory):
  for filename in os.listdir(course_directory):
    if filename.endswith(".docx"):
      file_path = os.path.join(course_directory, filename)
      course_content = docx2txt.process(file_path)
      course_descriptions[filename] = course_content
      course_descriptions_list.append(filename)


def load_jobs_description(job_directory):
    # Load job descriptions outside the request loop
  for filename in os.listdir(job_directory):
    if filename.endswith(".docx"):
      file_path = os.path.join(job_directory, filename)
      job_descriptions_list.append(filename)

@app.route('/recommend_jobs', methods=['POST'])
def recommend_jobs():
  # Get user prompt from JSON payload
  data = request.get_json()
  user_prompt = data.get('prompt')
  print("user_prompt",user_prompt)
  if not user_prompt:
    return jsonify({'error': 'Missing prompt in request body'}), 400

  loaded_embeddings = torch.load('Embedding/Jobs/merged_embeddings.pt')  # Adjust path based on language logic
  job_embeddings_tensor = torch.cat([loaded_embeddings])

  if not job_descriptions_list:
    load_jobs_description(job_directory)

  # Tokenize the prompt
  prompt_tokenized = tokenizer(user_prompt, max_length=512, padding=True, truncation=True, return_tensors='pt')

  # Compute embeddings for the prompt
  prompt_outputs = model(**prompt_tokenized)
  prompt_embedding = prompt_outputs.last_hidden_state.mean(dim=1)
  prompt_embedding = F.normalize(prompt_embedding, p=2, dim=1)

  # Calculate similarity scores
  scores = torch.matmul(prompt_embedding, job_embeddings_tensor.T)
  scores = scores.squeeze()  # Remove extra dimensions

  top_k = 5  # Number of top jobs to recommend

  top_indices = scores.argsort(descending=True)[:top_k]

  recommended_job = [job_descriptions_list[i] for i in top_indices]

  # Return recommendations as JSON
  return jsonify({'recommendations': recommended_job})




# Load descriptions based on language in request
@app.route('/recommend_courses', methods=['POST'])
def recommend_courses():
  # Get data from JSON payload

  data = request.get_json()
  language = data.get('language')
  
  if not language or language not in ['en', 'de']:
    return jsonify({'error': 'Missing or invalid language in request body'}), 400

  # Load course descriptions based on language
  if language == 'en':
  
    loaded_embeddings = torch.load('Embedding/en/merged_embeddings_en.pt')  # Adjust path based on language logic
    course_embeddings_tensor = torch.cat([loaded_embeddings])

    if not course_descriptions_list:
      load_course_descriptions(course_directory_en)
  else:
    
    loaded_embeddings = torch.load('Embedding/de/merged_embeddings_de.pt')  # Adjust path based on language logic
    course_embeddings_tensor = torch.cat([loaded_embeddings])

    if not course_descriptions_list:
      load_course_descriptions(course_directory_de)

  # Rest of the recommendation logic (same as before)
  user_prompt = data.get('prompt')

  if not user_prompt:
    return jsonify({'error': 'Missing prompt in request body'}), 400

  # Tokenize the prompt
  prompt_tokenized = tokenizer(user_prompt, max_length=512, padding=True, truncation=True, return_tensors='pt')

  # Compute embeddings for the prompt
  prompt_outputs = model(**prompt_tokenized)
  prompt_embedding = prompt_outputs.last_hidden_state.mean(dim=1)
  prompt_embedding = F.normalize(prompt_embedding, p=2, dim=1)

  # Calculate similarity scores
  scores = torch.matmul(prompt_embedding, course_embeddings_tensor.T)
  scores = scores.squeeze()  # Remove extra dimensions

  # Rank courses based on similarity scores
  top_k = 5  # Number of top courses to recommend
  top_indices = scores.argsort(descending=True)[:top_k]
  recommended_courses = [course_descriptions_list[i] for i in top_indices]

  # Return recommendations as JSON
  return jsonify({'recommendations': recommended_courses})


if __name__ == '__main__':
  app.run(debug=True)
