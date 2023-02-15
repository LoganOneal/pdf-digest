import os
from apps.models import File
from apps import grobid_client
from apps.grobid_client.api.pdf import process_fulltext_document
from apps.grobid_client.models import Article, ProcessForm
from apps.grobid_client.types import TEI, File
from transformers import AutoTokenizer
from transformers import pipeline


BASE_TEMP_DIR = 'temp'


async def parse(file) -> Article:
    if file.extension != 'pdf':
        print('File is not a PDF!')
        return None

    os.makedirs(BASE_TEMP_DIR, exist_ok=True)
    pdf_file = os.path.join(BASE_TEMP_DIR, f'{file.id}.pdf')

    with open(pdf_file, "wb") as f:
        f.write(file.data)

    with open(pdf_file,"rb") as fin:
        form = ProcessForm(
            segment_sentences="0",
            input_=File(file_name=file.filename, payload=fin, mime_type="application/pdf"),
        )
        r = process_fulltext_document.sync_detailed(client=grobid_client, multipart_data=form)

        if r.is_success:
            article: Article = TEI.parse(r.content, figures=False)
            assert article.title
        else:
            print("Error: failed to parse file")

    os.remove(pdf_file)

    return article

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

max_input_length = 512
max_target_length = 30

def bart_summarize(text, max_len):    
    nlp = pipeline("summarization")   

    summary = nlp(text, max_length=max_len)[0]["summary_text"].replace(" .", ".")                    
                        
    return summary


