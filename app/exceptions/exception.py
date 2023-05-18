class DiagnosisException(Exception):
    def __init__(self, details):
        self.details = details
        super().__init__(self.details)
