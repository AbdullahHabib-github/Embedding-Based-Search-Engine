from flask import Flask, request, jsonify
import courses as nc
import facets as fc

app = Flask(__name__)

# Load descriptions based on language in request
@app.route('/recommend_en_courses', methods=['POST'])
def recommend_en_courses():
  # Get data from JSON payload

  fc.get("data/courses/zqm_modul/en")
  nc.get("data/courses/zqm_modul/en","Embedding/en/merged_embeddings_en.pt")

  data = request.get_json()
  
  # Rest of the recommendation logic (same as before)
  user_prompt = data.get('prompt')

  if not user_prompt:
    return jsonify({'error': 'Missing prompt in request body'}), 400

  fc.taking_input(user_prompt)
  out1 = fc.sent()
  out2 = nc.sent()
  #These are the list of of output files
  # print(out1)
  # print(out2)

  combined_names = out1["recommendations"] + out2["recommendations"]
  combined_scores = out1["scores"] + out2["scores"]

  # Create a list of tuples (score, name) and sort it
  combined = list(zip(combined_scores, combined_names))
  combined_sorted = sorted(combined,reverse=True,key=lambda x: x[0])

  # Separate the sorted scores and names
  sorted_scores, sorted_names = zip(*combined_sorted)

  # Create the new dictionary
  out = {"recommendations": list(sorted_names), "scores": list(sorted_scores)}
  fc.empty()
  nc.empty()


  return jsonify(out)




# Load descriptions based on language in request
@app.route('/recommend_de_courses', methods=['POST'])
def recommend_de_courses():
  # Get data from JSON payload

  fc.get("data/courses/zqm_modul/de")
  nc.get("data/courses/zqm_modul/de","Embedding/de/merged_embeddings_de.pt")

  data = request.get_json()
  
  # Rest of the recommendation logic (same as before)
  user_prompt = data.get('prompt')

  if not user_prompt:
    return jsonify({'error': 'Missing prompt in request body'}), 400

  fc.taking_input(user_prompt)
  out1 = fc.sent()
  out2 = nc.sent()
  #These are the list of of output files
  # print(out1)
  # print(out2)

  combined_names = out1["recommendations"] + out2["recommendations"]
  combined_scores = out1["scores"] + out2["scores"]

  # Create a list of tuples (score, name) and sort it
  combined = list(zip(combined_scores, combined_names))
  combined_sorted = sorted(combined,reverse=True, key=lambda x: x[0])

  # Separate the sorted scores and names
  sorted_scores, sorted_names = zip(*combined_sorted)

  # Create the new dictionary
  out = {"recommendations": list(sorted_names), "scores": list(sorted_scores)}
  fc.empty()
  nc.empty()

  return jsonify(out)


if __name__ == '__main__':
  app.run(debug=True)
