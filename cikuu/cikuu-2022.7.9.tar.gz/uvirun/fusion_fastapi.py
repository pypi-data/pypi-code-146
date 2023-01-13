# 2022.8.29 #https://huggingface.co/transformers/v3.5.1/model_doc/bertgeneration.html
from uvirun import *

@app.get('/fusion', tags=["transformers"])
def fusion(snts:str="I am tired. I can not move on."):
	''' 2022.8.29 '''
	from transformers import EncoderDecoderModel, AutoTokenizer
	import torch
	if not hasattr( fusion,'tokenizer'):
		fusion.sentence_fuser = EncoderDecoderModel.from_pretrained("/data/model/google/roberta2roberta_L-24_discofuse")
		fusion.tokenizer = AutoTokenizer.from_pretrained("/data/model/google/roberta2roberta_L-24_discofuse")
	input_ids = fusion.tokenizer(snts, add_special_tokens=False, return_tensors="pt").input_ids
	outputs = fusion.sentence_fuser.generate(input_ids)
	return fusion.tokenizer.decode(outputs[0])

if __name__ == "__main__":   #uvicorn.run(app, host='0.0.0.0', port=80)
	pass 

'''
https://huggingface.co/google/roberta2roberta_L-24_discofuse?text=I+am+tired.+I+can+not+move+on.
==> therefore 
I am tired. Therefore I can not move on.
'''