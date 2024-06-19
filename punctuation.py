from deepmultilingualpunctuation import PunctuationModel

model = PunctuationModel(model="oliverguhr/fullstop-punctuation-multilang-large")


def restore(text_chunks):
    result = model.restore_punctuation(text_chunks)
    return result