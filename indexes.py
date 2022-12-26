from document import Document

from typing import List


def build_inverted_index(documents: List[Document]):
    index = {}

    for document in documents:
        unique_terms = []
        terms_set = set()  # O(1) access and make doctests work (dicts are checked in order)

        for term in document.get_terms():
            if term not in terms_set:
                unique_terms.append(term)
                terms_set.add(term)

        for term in unique_terms:
            references = index.setdefault(term, [])
            if document.reference not in references:
                references.append(document.reference)

    return index


def build_forward_index(documents: List[Document]):
    index = {}
    for document in documents:
        index.setdefault(document.reference, set(document.get_terms()))
    return index


def filter_index_references_by_all_terms(index, query_terms):
    references_containing_all_terms = []
    query_terms_set = frozenset(query_terms)
    found_terms_count_in_files = dict()

    for term, filenames in index.items():
        if term in query_terms_set:
            for filename in filenames:
                found_terms_count_in_files.setdefault(filename, 0)
                found_terms_count_in_files[filename] += 1

    for filename, found_terms_count in found_terms_count_in_files.items():
        if found_terms_count == len(query_terms):
            references_containing_all_terms.append(filename)

    return references_containing_all_terms
