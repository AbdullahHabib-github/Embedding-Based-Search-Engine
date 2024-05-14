import torch
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel
import os
import docx2txt

# Directory where your course files are stored
# remove en with de for de files !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
course_directory = "data/courses/zqm_modul/en"

# Initialize an empty list to store course descriptions
course_descriptions = {}
course_descriptions_list = []

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


# *****************************************************************
# *****************************************************************
# *****************************************************************
# For Courses in de use this line de 
# loaded_embeddings = torch.load('Embedding\en\merged_embeddings_de.pt')
# and comment line loaded_embeddings = torch.load('Embedding\en\merged_embeddings_en.pt')
# *****************************************************************
# *****************************************************************
# *****************************************************************
loaded_embeddings = torch.load('Embedding/en/merged_embeddings_en.pt')
course_embeddings_tensor = torch.cat([loaded_embeddings])




# Get user prompt
user_prompt = input("Enter your prompt: ")

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
print(top_indices)
recommended_courses = [course_descriptions_list[i] for i in top_indices]

# Present recommendations
print("Recommended Courses:")
for i, course in enumerate(recommended_courses, 1):
    print(f"{i}. {course}")
