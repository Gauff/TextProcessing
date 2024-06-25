from langchain_community.chat_models import ChatLiteLLM
from langchain_core.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
import environment
import text_processing

MAP_PROMPT_TEMPLATE = """
Write a concise summary of the following:
"{text}"
CONCISE SUMMARY:
"""

COMBINE_PROMPT_TEMPLATE = """
You will be given a series of summaries from a book. The summaries will be enclosed in triple backticks (```)
Your goal is to give a verbose summary of what happened in the story.
The reader should be able to grasp what happened in the book.

```{text}```
VERBOSE SUMMARY:
"""


def create_summary(text):
    """Generate summary using map-reduce chain."""

    chunk_size = environment.SMALL_CONTEXT_MAX_TOKENS - len(MAP_PROMPT_TEMPLATE)
    small_context_llm = ChatLiteLLM(model_name=environment.SMALL_CONTEXT_MODEL_NAME)

    if len(text) < chunk_size:
        prompt = MAP_PROMPT_TEMPLATE.replace("{text}", text)
        summary = small_context_llm.invoke(prompt)
        return summary.content

    chunk_overlap = chunk_size // 4
    chunks = text_processing.split(text, chunk_size, chunk_overlap)

    map_prompt_template = PromptTemplate(template=MAP_PROMPT_TEMPLATE, input_variables=["text"])
    combine_prompt_template = PromptTemplate(template=COMBINE_PROMPT_TEMPLATE, input_variables=["text"])
    summary_chain = load_summarize_chain(llm=small_context_llm,
                                         chain_type='map_reduce',
                                         map_prompt=map_prompt_template,
                                         combine_prompt=combine_prompt_template)
    output = summary_chain.run(chunks)
    return output
