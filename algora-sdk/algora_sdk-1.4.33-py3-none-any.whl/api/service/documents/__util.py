from algora.api.service.documents.model import DocumentRequest, SearchDocumentRequest


def _get_document_request_info(id: str) -> dict:
    return {
        'endpoint': f"config/documents/{id}"
    }


def _search_documents_request_info(request: SearchDocumentRequest) -> dict:
    return {
        'endpoint': "config/documents/search",
        'json': request.request_dict()
    }


def _create_document_request_info(request: DocumentRequest) -> dict:
    return {
        'endpoint': "config/documents",
        'json': request.request_dict()
    }


def _update_document_request_info(id: str, request: DocumentRequest) -> dict:
    return {
        'endpoint': f"config/documents/{id}",
        'json': request.request_dict()
    }


def _delete_document_request_info(id: str) -> dict:
    return {
        'endpoint': f"config/documents/{id}"
    }
