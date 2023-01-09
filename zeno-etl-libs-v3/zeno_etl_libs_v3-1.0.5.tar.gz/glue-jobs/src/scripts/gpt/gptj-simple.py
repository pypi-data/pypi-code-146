from gpt_j.Basic_api import simple_completion

prompt = "def perfect_square(num):"

max_length = 100

temperature = 0.09

top_probability = 1.0

top_k = 40

repetition = 0.216

query = simple_completion(
    prompt, length=max_length, temp=temperature, top_p=top_probability, top_k=top_k, rep=repetition
)
