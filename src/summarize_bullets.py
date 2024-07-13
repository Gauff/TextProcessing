from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatLiteLLM
import text_processing
from chunk import Chunk
import environment


# Original idea: https://www.youtube.com/watch?v=qaPMdcCqtWk

BULLET_SUMMARY_TEMPLATE = """
Write a concise summary of the following text delimited by triple backquotes.
```{text}```
Return your response in bullet points which covers the key points of the text.
Do not introduce your answer by sentences like 'Here is the summary in bullet points:'.
"""
ORIGINAL_LANGUAGE="Keep text original language."
FORCED_LANGUAGE="Process and reply using the {forced_language_name} human language." 


def extended_bullet_summary(text, forced_language_code=None):
    return _bullet_summary(text, forced_language_code)


def condensed_bullet_summary(text, forced_language_code=None):
    bullet_summary = _bullet_summary(text, forced_language_code)

    while len(bullet_summary) > environment.SMALL_CONTEXT_MAX_TOKENS:
        bullet_summary = _bullet_summary(bullet_summary, forced_language_code)

    return bullet_summary


def _bullet_summary(text, forced_language_code=None):
    chunk_size = environment.SMALL_CONTEXT_MAX_TOKENS - len(BULLET_SUMMARY_TEMPLATE) - len(FORCED_LANGUAGE)
    chunk_overlap = chunk_size // 4
    chunks = text_processing.split(text, chunk_size, chunk_overlap)

    small_context_llm = ChatLiteLLM(model_name=environment.SMALL_CONTEXT_MODEL_NAME)
    summarized_chunks = _summarize_chunks(chunks, small_context_llm, forced_language_code)

    bullet_summary = "\n".join(s.summary for s in summarized_chunks)

    return bullet_summary


def _summarize_chunks(chunks, small_context_llm, forced_language_code):
    
    if forced_language_code is None:
        prompt_template = BULLET_SUMMARY_TEMPLATE + ORIGINAL_LANGUAGE
    else:
        import languages
        forced_language_name = languages.get_language_name(forced_language_code)
        prompt_template = BULLET_SUMMARY_TEMPLATE + FORCED_LANGUAGE
    
    map_prompt_template = PromptTemplate(template=prompt_template, input_variables=["text", "forced_language_name"])

    def run_map_stage(input_texts):
        _chunks = []
        for doc in input_texts:
            prompt = map_prompt_template.template.format(text=doc.page_content,forced_language_name=forced_language_name)
            map_result = small_context_llm.invoke(prompt)
            chunk = Chunk(doc.page_content, map_result.content, map_result.response_metadata)
            _chunks.append(chunk)
        return _chunks

    summarized_chunks = run_map_stage(chunks)

    return summarized_chunks
