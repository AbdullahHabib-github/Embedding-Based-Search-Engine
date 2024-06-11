import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
import os
import docx2txt


course_descriptions = {}
course_descriptions_list = []
course_embeddings_tensor = ""
cde = None
def get(cd,ed):
    global cde
    course_directory = cd
    course_embeddings_tensor = ed
    cde = torch.load(course_embeddings_tensor)
    # Initialize an empty list to store course descriptions

    # Loop through each file in the directory
    for filename in os.listdir(course_directory):
        if filename.endswith(".docx"):
            # Read the contents of the Word file
            file_path = os.path.join(course_directory, filename)
            course_content = docx2txt.process(file_path)
            
            # Append course content to the list
            course_descriptions[filename] = course_content
            course_descriptions_list.append(filename)

# Now you have course descriptions in the `course_descriptions` dictionary
# Initialize tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("thenlper/gte-large")
model = AutoModel.from_pretrained("thenlper/gte-large")
# Load embeddings tensor
recommended_courses = []
score = []
# Get user prompt
def take_prompt(use):
    user_prompt = use

    # Tokenize the prompt
    prompt_tokenized = tokenizer(user_prompt, max_length=512, padding=True, truncation=True, return_tensors='pt')

    # Compute embeddings for the prompt
    prompt_outputs = model(**prompt_tokenized)
    prompt_embedding = prompt_outputs.last_hidden_state.mean(dim=1)
    prompt_embedding = F.normalize(prompt_embedding, p=2, dim=1)
    
    # Calculate similarity scores
    scores = torch.matmul(prompt_embedding, cde.T)
    scores = scores.squeeze()  # Remove extra dimensions

    # Rank courses based on similarity scores
    top_indices = scores.argsort(descending=True)
    global recommended_courses
    global score
    score = scores[top_indices].tolist()
    for i in top_indices:
        recommended_courses.append(course_descriptions_list[i])

    
def empty():
    global recommended_courses
    global score
    score = []
    recommended_courses = []
def sent():
        global score
        global recommended_courses
        return {'recommendations': recommended_courses, "scores": score}