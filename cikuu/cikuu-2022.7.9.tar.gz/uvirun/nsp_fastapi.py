#20-3-5  /data/model/bert/uncased_L-12_H-768_A-12
from uvirun import * 

@app.get('/nsp')
def nsp(snt0:str='Who was Jim Henson ?', snt1:str='Jim Henson was a puppeteer'): # tokenzied
	''' 2022.8.29 '''
	import torch
	from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM, BertForNextSentencePrediction  # pip install pytorch_pretrained_bert
	if not hasattr(nsp, 'model'): 
		nsp.tokenizer = BertTokenizer.from_pretrained('/data/model/bert-base-uncased')
		nsp.model = BertForNextSentencePrediction.from_pretrained('/data/model/bert-base-uncased')
		nsp.model.eval()	

	text = f"[CLS] {snt0} [SEP] {snt1} [SEP]" #[CLS] Who was Jim Henson ? [SEP] Jim Henson was a puppeteer [SEP]
	tokenized_text = nsp.tokenizer.tokenize(text)
	indexed_tokens = nsp.tokenizer.convert_tokens_to_ids(tokenized_text)
	segments_ids = [ 0 if i <= tokenized_text.index("[SEP]") else  1 for i,w in enumerate(tokenized_text) ] #[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1] # Define sentence A and B indices associated to 1st and 2nd sentences (see paper)
	tokens_tensor = torch.tensor([indexed_tokens])
	segments_tensors = torch.tensor([segments_ids])
	with torch.no_grad():
		predictions = nsp.model(tokens_tensor, segments_tensors)
	tup =  torch.softmax(predictions, axis=-1).detach().numpy().tolist() #[[0.005735984072089195, 0.9942639470100403]]
	#return tup[0] 
	return round(tup[0][0], 4)

if __name__ == '__main__':
	print(nsp("It is ok .", "The quick fox jumped over the lazy dog ."))
	print(nsp())