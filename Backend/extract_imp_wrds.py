from clarifai.client.model import Model
from audio import extract_text


def keyword(content):
    keyword_prompt = """[INST] I have the following document:- [DOCUMENT]Please give me the important lines that are present in this document and separate them with commas.
Make sure you to only return the sentences and say nothing else. For example, don't say:"Here are the keywords present in the document"[/INST]"""
    intro = "and the content from which the important sentences should be from is :"
    result_ip = keyword_prompt + intro + str(content)
    model_url="https://clarifai.com/openai/chat-completion/models/gpt-4-turbo"
    model_prediction = Model(url=model_url,pat="de242f3fc61f4e5b9388c9dc7fe7b0a9").predict_by_bytes(result_ip.encode(), input_type="text")
#  model_prediction = Model(url=model_url,pat="deb0a9").predict_by_bytes(prompt.title().encode(), input_type="text")  
    # print(model_prediction.outputs[0].data.text.raw)
    return model_prediction.outputs[0].data.text.raw


extracted_text = extract_text("ml.pdf")
print(keyword(extracted_text))
                