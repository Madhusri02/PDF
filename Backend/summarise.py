from transformers import pipeline

def summarise_content(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=150, min_length=40, do_sample=False)
    print("Type is ")
    print(type(summary[0]['summary_text']))
    return summary[0]['summary_text']

    # print(summary[0]['summary_text'])