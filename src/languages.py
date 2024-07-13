from langdetect import detect, DetectorFactory
import pycountry


def get(text):
    DetectorFactory.seed = 0
    language = detect(text)
    return language


def get_language_name(code):
    try:
        language = pycountry.languages.get(alpha_2=code)
        if language:
            return language.name
        else:
            return None
    except KeyError:
        return None