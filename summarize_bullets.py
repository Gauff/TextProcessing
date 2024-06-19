from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatLiteLLM
import text_processing
from chunk import Chunk
import environment

# Original idea: https://www.youtube.com/watch?v=qaPMdcCqtWk

BULLET_SUMMARY_TEMPLATE = """
Write a concise summary of the following text delimited by triple backquotes.
Return your response in bullet points which covers the key points of the text.
```{text}```
Do not introduce your answer by sentences like 'Here is the summary in bullet points:'.
Keep text original language.
"""


def extended_bullet_summary(text):
    return _bullet_summary(text)


def condensed_bullet_summary(text):
    bullet_summary = _bullet_summary(text)

    while len(bullet_summary) > environment.SMALL_CONTEXT_MAX_TOKENS:
        bullet_summary = _bullet_summary(text)

    return bullet_summary


def _bullet_summary(text):
    chunk_size = environment.SMALL_CONTEXT_MAX_TOKENS - len(BULLET_SUMMARY_TEMPLATE)
    chunk_overlap = chunk_size // 4
    chunks = text_processing.split(text, chunk_size, chunk_overlap)

    small_context_llm = ChatLiteLLM(model_name=environment.SMALL_CONTEXT_MODEL_NAME)
    summarized_chunks = _summarize_chunks(chunks, small_context_llm)

    bullet_summary = "\n".join(s.summary for s in summarized_chunks)

    return bullet_summary


def _summarize_chunks(chunks, small_context_llm):
    """Detailed function to generate summary with intermediate steps."""
    map_prompt_template = PromptTemplate(template=BULLET_SUMMARY_TEMPLATE, input_variables=["text"])

    def run_map_stage(input_texts):
        _chunks = []
        for doc in input_texts:
            prompt = map_prompt_template.template.format(text=doc.page_content)
            map_result = small_context_llm.invoke(prompt)
            chunk = Chunk(doc.page_content, map_result.content, map_result.response_metadata)
            _chunks.append(chunk)
        return _chunks

    summarized_chunks = run_map_stage(chunks)

    return summarized_chunks
