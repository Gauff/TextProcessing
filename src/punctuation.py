def restore(text_chunks):
    from deepmultilingualpunctuation import PunctuationModel
    model = PunctuationModel(model="oliverguhr/fullstop-punctuation-multilang-large")
    result = model.restore_punctuation(text_chunks)
    return result