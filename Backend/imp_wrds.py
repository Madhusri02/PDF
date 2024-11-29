from ctransformers import AutoModelForCausalLM
from transformers import AutoTokenizer, pipeline
from keybert.llm import TextGeneration
from keybert import KeyLLM
from audio import extract_text

""" to run : 
     use hugging face login command  : 
    -> huggingface-cli login
    enter this access token : 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

    then install these : 
      pip install --upgrade git+https://github.com/UKPLab/sentence-transformers
      pip install keybert ctransformers[cuda]
      pip install --upgrade git+https://github.com/huggingface/transformers 
    
     """

global model 
global tokenizer
global generator

def model_init():
    model = AutoModelForCausalLM.from_pretrained(
    "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
    model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    model_type="mistral",
    gpu_layers=50,
    hf=True
    )

    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
    generator = pipeline(
    model=model, tokenizer=tokenizer,
    task='text-generation',
    max_new_tokens=50,
    repetition_penalty=1.1
     )

    


def model_creation(content):
    keyword_prompt = """[INST] I have the following document:- [DOCUMENT]Please give me the keywords that are present in this document and separate them with commas.
Make sure you to only return the keywords and say nothing else. For example, don't say:"Here are the keywords present in the document"[/INST]"""
    example_prompt = """<s>[INST]
    I have the following document:
      - The website mentions that it only takes a couple of days to deliver but I still have not received mine.
Please give me the keywords that are present in this document and separate them with commas.
Make sure you to only return the keywords and say nothing else. For example, don't say:
"Here are the keywords present in the document"
[/INST] meat, beef, eat, eating, emissions, steak, food, health, processed, chicken</s>"""
    exp_prompt = keyword_prompt + example_prompt
    llm = TextGeneration(generator, prompt= exp_prompt)
    kw_model = KeyLLM(llm)

    keywords = kw_model.extract_keywords(content)
    return keywords


model_init()

text_extracted = extract_text('ml.pdf')
gen_keywords = model_creation(text_extracted)
print(gen_keywords)




    


