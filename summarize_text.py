from langchain_community.chat_models import ChatLiteLLM
from langchain_core.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
import environment
import text_processing
import languages


MAP_PROMPT_TEMPLATE = """
Write a concise summary of the following without any introduction:
"{text}"
CONCISE SUMMARY:
"""

COMBINE_PROMPT_TEMPLATE = """
You will be given a series of summaries from a book. The summaries will be enclosed in triple backticks (```)
Your goal is to give a verbose summary of what happened in the story.
The reader should be able to grasp what happened in the book.
Do not give any introduction.
```{text}```
VERBOSE SUMMARY:
"""

ORIGINAL_LANGUAGE = "Keep text original language."
FORCED_LANGUAGE = "Process and reply using the {forced_language_name} human language." 

def create_summary(text, forced_language_code=None):
    """Generate summary using map-reduce chain."""

    if forced_language_code is None:
        forced_language_name = "original language"  # Default placeholder
        map_prompt_template = ORIGINAL_LANGUAGE + MAP_PROMPT_TEMPLATE 
        combine_prompt_template = ORIGINAL_LANGUAGE + COMBINE_PROMPT_TEMPLATE
    else:
        forced_language_name = languages.get_language_name(forced_language_code)
        map_prompt_template = FORCED_LANGUAGE + MAP_PROMPT_TEMPLATE 
        combine_prompt_template = FORCED_LANGUAGE + COMBINE_PROMPT_TEMPLATE

    chunk_size = environment.SMALL_CONTEXT_MAX_TOKENS - len(map_prompt_template)
    small_context_llm = ChatLiteLLM(model_name=environment.SMALL_CONTEXT_MODEL_NAME)

    if len(text) < chunk_size:
        prompt = map_prompt_template.replace("{text}", text).replace("{forced_language_name}", forced_language_name)
        summary = small_context_llm.invoke(prompt)
        return summary.content

    chunk_overlap = chunk_size // 4
    chunks = text_processing.split(text, chunk_size, chunk_overlap)

    _map_prompt_template = PromptTemplate(template=map_prompt_template, input_variables=["text", "forced_language_name"])
    _combine_prompt_template = PromptTemplate(template=combine_prompt_template, input_variables=["text", "forced_language_name"])
    
    summary_chain = load_summarize_chain(
        llm=small_context_llm,
        chain_type='map_reduce',
        map_prompt=_map_prompt_template,
        combine_prompt=_combine_prompt_template
    )

    input_documents = [Document(page_content=str(chunk)) for chunk in chunks]
    output = summary_chain.invoke({"input_documents": input_documents, "forced_language_name": forced_language_name})

    return output["output_text"]