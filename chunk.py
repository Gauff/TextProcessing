class Chunk:
    def __init__(self, text, summary=None, response_metadata=None):
        """
        Initialise un objet Chunk avec les propriétés text, summary, et response_metadata.

        :param text: Le texte du chunk.
        :param summary: Le résumé du chunk (par défaut à None).
        :param response_metadata: Les métadonnées de la réponse (par défaut à None).
        """
        self._text = text
        self._summary = summary
        self._response_metadata = response_metadata

    @property
    def text(self):
        """Retourne le texte du chunk."""
        return self._text

    @text.setter
    def text(self, value):
        """Définit le texte du chunk."""
        self._text = value

    @property
    def summary(self):
        """Retourne le résumé du chunk."""
        return self._summary

    @summary.setter
    def summary(self, value):
        """Définit le résumé du chunk."""
        self._summary = value

    @property
    def response_metadata(self):
        """Retourne les métadonnées de la réponse."""
        return self._response_metadata

    @response_metadata.setter
    def response_metadata(self, value):
        """Définit les métadonnées de la réponse."""
        self._response_metadata = value