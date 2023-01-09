""" pip install  openai """

import openai

# Set the API key (your own api key)
openai.api_key = ""

# Set up the model
model_engine = "text-davinci-002"
model_prompt = (
    f"""find me the flat number, building name, locality, landmark, city, state, country and pincode 
    in this address as colon separated 
    1007, landmark gardens near bishops school kalyani nagar pune maharashtra 411006
    """
)

# Generate text
completion = openai.Completion.create(
    engine=model_engine,
    prompt=model_prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.7,
)

# Print the generated text
generated_text = completion.choices[0].text
print(generated_text)
