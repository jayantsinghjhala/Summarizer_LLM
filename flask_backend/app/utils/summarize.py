import os
import re
import docx
from PyPDF2 import PdfReader
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import threading

MODEL_DIR = os.path.join(os.getcwd(), "app/models")
os.makedirs(MODEL_DIR, exist_ok=True)


model_name = "sshleifer/distilbart-cnn-12-3" #1.02GB
# model_name = "t-small" #250MB #was genrating low quality summaries
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=MODEL_DIR, clean_up_tokenization_spaces=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir=MODEL_DIR)

summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

summarization_thread = None
stop_summarization = threading.Event()
accumulated_summaries = []
summarization_status = {'status': 'idle', 'summary': '', 'error': None}

def split_text(text, max_length=1024):
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def summarize_chunk(index, chunk):
    global accumulated_summaries, summarization_status
    if stop_summarization.is_set():
        print(f"Summarization stopped. Chunk {index+1} will not be processed.")
        return
    print(f"Summarizing chunk {index + 1}...")
    chunk_summary = summarizer(chunk, max_length=100, do_sample=False)[0]['summary_text']
    accumulated_summaries.append(chunk_summary)
    summarization_status['summary'] = " ".join(accumulated_summaries)
    print(f"Chunk {index + 1} summarized.")

def summarize_document(filepath):
    global stop_summarization, accumulated_summaries, summarization_status

    summarization_status['status'] = 'in_progress'
    summarization_status['summary'] = ''
    summarization_status['error'] = None

    try:
        file_extension = os.path.splitext(filepath)[1].lower()

        if file_extension == '.txt':
            with open(filepath, 'r', encoding='utf-8') as file:
                document_text = file.read()
        elif file_extension == '.docx':
            document = docx.Document(filepath)
            document_text = "\n".join([para.text for para in document.paragraphs])
        elif file_extension == '.pdf':
            with open(filepath, 'rb') as file:
                reader = PdfReader(file)
                document_text = ""
                for page in range(len(reader.pages)):
                    document_text += reader.pages[page].extract_text()
        else:
            raise ValueError("Unsupported file format")

        document_text = re.sub(r'\s+', ' ', document_text).strip()

        if len(document_text) > 5000:
            print(f"Document is too long ({len(document_text)} characters). Splitting into chunks...")
            chunks = split_text(document_text, max_length=5000)
            num_chunks = len(chunks)
            print(f"Total chunks: {num_chunks}")
            stop_summarization.clear()
            global summarization_thread
            accumulated_summaries = []

            summarization_thread = threading.Thread(target=lambda: [summarize_chunk(i, chunk) for i, chunk in enumerate(chunks)])
            summarization_thread.start()
            summarization_thread.join()  # So to Wait for the thread to complete

            if stop_summarization.is_set():
                summarization_status['status'] = 'stopped'
            else:
                summarization_status['status'] = 'completed'
            summarization_status['summary'] = " ".join(accumulated_summaries)
        else:
            print(f"Document length is acceptable ({len(document_text)} characters). Summarizing directly...")
            summary = summarizer(document_text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
            summarization_status['status'] = 'completed'
            summarization_status['summary'] = summary

    except Exception as e:
        summarization_status['status'] = 'error'
        summarization_status['error'] = str(e)

def stop_summarization_process():
    global stop_summarization, summarization_thread, summarization_status
    stop_summarization.set()
    if summarization_thread:
        summarization_thread.join()
    summarization_status['status'] = 'stopped'
    return summarization_status['summary']