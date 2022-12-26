import string
from dataclasses import dataclass


@dataclass
class Document:
    reference: str
    content: str

    @classmethod
    def from_medium_csv_line(cls, url, title, subtitle):
        return cls(url, title + subtitle)

    @classmethod
    def from_file_path(cls, file_path):
        with open(file_path, "r") as f:
            return cls(file_path, f.read())

    @staticmethod
    def normalize_text(text: str) -> str:
        return text.lower().replace("\n", " ")

    def __post_init__(self):
        self.content = self.normalize_text(self.content)

    def get_terms(self):
        return [raw_term.strip(string.punctuation) for raw_term in self.content.split()]


class Article(Document):
    title: str

    def __post_init__(self):
        self.title = self.extract_title_from_text(self.content)
        super().__post_init__()

    @staticmethod
    def extract_title_from_text(text):
        try:
            return text.splitlines()[0]
        except IndexError:
            return ''