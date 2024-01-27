from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate

def summarize(llm, documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000)
    docs = text_splitter.split_documents(documents)
    combine_template = """{text}
    You summarize this document in the following format.
    Be sure to write it in Korean.
    Write the results of your summary in the following format:
    제목: Title
    내용: Write your key takeaways in bullet point format
    """
    combine_prompt = PromptTemplate(template=combine_template, input_variables=['text'])
    chain = load_summarize_chain(
        llm,
        chain_type="map_reduce",
        combine_prompt=combine_prompt,
        verbose=True
        )
    summaries = chain.invoke(docs)
    return summaries  # Directly return the summaries if they are already strings
