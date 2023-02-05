from transformers import AutoTokenizer
from transformers import pipeline

max_input_length = 512
max_target_length = 30

# Load the tokenizer
'''model_checkpoint = "google/mt5-small"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

def preprocess_function(examples):
    model_inputs = tokenizer(
        examples["review_body"],
        max_length=max_input_length,
        truncation=True,
    )
    labels = tokenizer(
        examples["review_title"], max_length=max_target_length, truncation=True
    )
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs'''

def bart_summarize(text, max_len):    
    nlp = pipeline("summarization")   

    summary = nlp(text, max_length=max_len)[0]["summary_text"].replace(" .", ".")                    
                        
    return summary

