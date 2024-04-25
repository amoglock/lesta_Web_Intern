import string
from fastapi import UploadFile
from src.tfidf_inspector import TfidfInspector


class FileWorker:
    def __init__(self):
        self.table = str.maketrans("", "", string.punctuation)
        self.inspector = TfidfInspector()
        self.summary_files = {}
        self.texts = {}

    async def worker(self, files: list[UploadFile]) -> dict[str, str]:
        for file in files:
            text = await file.read()
            await file.close()

            self.summary_files[file.filename] = text.decode()[:150] + "..."
            preprocessed_text = [self.inspector.lemma(word) for word in text.decode().translate(self.table).split()]
            self.texts[file.filename] = preprocessed_text

        return self.summary_files
