from langdetect import detect, DetectorFactory


def get(text):
    DetectorFactory.seed = 0
    language = detect(text)
    return language