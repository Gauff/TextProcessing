from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatLiteLLM
import text_processing
from chunk import Chunk
import environment
import languages

# Original idea: https://www.youtube.com/watch?v=qaPMdcCqtWk

TRANSLATION_TEMPLATE = """
Translate the following text delimited by triple backquotes in {language_name}.
```{text}```
Only provide translation without triple backquotes. No other text.
"""


def translate(text, lang):
    language_name = languages.get_language_name(lang)
    return _translate(text, language_name)


def _translate(text, language_name):
    chunk_size = environment.SMALL_CONTEXT_MAX_TOKENS - len(TRANSLATION_TEMPLATE)
    chunk_overlap = chunk_size // 4
    chunks = text_processing.split(text, chunk_size, chunk_overlap)

    small_context_llm = ChatLiteLLM(model_name=environment.SMALL_CONTEXT_MODEL_NAME)
    translated_chunks = _translate_chunks(chunks, language_name, small_context_llm)

    bullet_summary = "\n".join(s.summary for s in translated_chunks)

    return bullet_summary


def _translate_chunks(chunks, language_name, small_context_llm):
    map_prompt_template = PromptTemplate(template=TRANSLATION_TEMPLATE, input_variables=["text", "language_name"])

    def run_map_stage(input_texts):
        _chunks = []
        for doc in input_texts:
            prompt = map_prompt_template.template.format(text=doc.page_content, language_name=language_name)
            map_result = small_context_llm.invoke(prompt)
            chunk = Chunk(doc.page_content, map_result.content, map_result.response_metadata)
            _chunks.append(chunk)
        return _chunks

    translated_chunks = run_map_stage(chunks)

    return translated_chunks
