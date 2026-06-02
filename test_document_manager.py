import pytest
from document_manager import DocumentManager


# РЕФАКТОРИНГ 3: Створено фікстуру для усунення дублювання (Code Duplication)
@pytest.fixture
def manager():
    """Повертає новий екземпляр DocumentManager для кожного тесту."""
    return DocumentManager()


def test_upload_valid_document(manager):
    doc = manager.upload_document("test.pdf", 5.0)
    assert doc is not None
    assert doc.file_name == "test.pdf"


def test_upload_zero_size(manager):
    with pytest.raises(ValueError, match="більшим за нуль"):
        manager.upload_document("error.txt", 0.0)


def test_upload_exact_max_size(manager):
    doc = manager.upload_document("large.txt", 10.0)
    assert doc.id == 1  


def test_search_existing_tag(manager):
    doc = manager.upload_document("notes.txt", 1.0)
    doc.add_tag("python")
    
    results = manager.search_by_tags(["python"])
    assert len(results) == 1
    assert results[0].id == doc.id


def test_search_non_existing_tag(manager):
    doc = manager.upload_document("notes.txt", 1.0)
    doc.add_tag("java")
    
    results = manager.search_by_tags(["python"])
    assert len(results) == 0


def test_process_existing_document(manager):
    # Документ розміром 10.0 MB
    doc = manager.upload_document("report.docx", 10.0)
    report = manager.analyze(doc)
    
    # Формула: 1.0 - (10.0 / 100.0) = 0.9
    assert report["confidence_score"] == pytest.approx(0.9)