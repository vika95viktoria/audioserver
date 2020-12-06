from docx import Document


def create_word_doc(text, name_without_ext):
    document = Document()
    document.add_paragraph(text)
    doc_name = f'{name_without_ext}.docx'
    document.save(doc_name)
    return doc_name
