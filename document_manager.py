class Document:
    def __init__(self, doc_id: int, file_name: str, size_mb: float):
        self.id = doc_id
        self.file_name = file_name
        self.size_mb = size_mb
        self.tags = []

    def add_tag(self, tag: str):
        tag_lower = tag.strip().lower()
        if tag_lower not in self.tags:
            self.tags.append(tag_lower)


class DocumentManager:
    # РЕФАКТОРИНГ 1: Винесено "магічні рядки" розширень у константу
    ALLOWED_EXTENSIONS = ('.txt', '.pdf', '.docx')
    
    # РЕФАКТОРИНГ 2: Винесено "магічні числа" для аналізу в константи
    MIN_CONFIDENCE = 0.1
    MAX_ANALYSIS_SIZE = 100.0

    def __init__(self):
        self.documents = {}
        self.next_id = 1

    def upload_document(self, file_name: str, size_mb: float) -> Document:
        if size_mb <= 0:
            raise ValueError("Розмір має бути більшим за нуль")
        
        # Використання константи замість жорстко закодованого кортежу
        if not file_name.endswith(self.ALLOWED_EXTENSIONS):
            raise ValueError(f"Формат файлу має бути одним із: {self.ALLOWED_EXTENSIONS}")
        
        doc_id = self.next_id
        self.next_id += 1
        
        doc = Document(doc_id, file_name, size_mb)
        self.documents[doc_id] = doc
        return doc

    def analyze(self, doc: Document) -> dict:
        # Використання констант замість чисел 0.1 та 100
        confidence = max(self.MIN_CONFIDENCE, 1.0 - (doc.size_mb / self.MAX_ANALYSIS_SIZE))
        return {"confidence_score": confidence}

    def search_by_tags(self, query_tags: list) -> list:
        if not all(isinstance(t, str) for t in query_tags):
            raise ValueError("Теги мають бути рядками")
            
        search_tags = [t.strip().lower() for t in query_tags]
        
        results = []
        for doc in self.documents.values():
            for tag in search_tags:
                if tag in doc.tags and doc not in results:
                    results.append(doc)
        return results