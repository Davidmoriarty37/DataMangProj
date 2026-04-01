from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def tokenize(df, text_column, tokenizer,labels, max_length=128):
    texts = df[text_column].tolist()
    
    encodings = tokenizer(
        texts,
        truncation=True,
        padding=True,
        max_length=max_length,
        return_tensors='pt'   # returns PyTorch tensors
    )
    
    return encodings, df[labels]