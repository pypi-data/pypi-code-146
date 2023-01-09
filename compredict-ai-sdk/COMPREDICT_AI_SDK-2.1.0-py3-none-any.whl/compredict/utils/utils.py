def extract_error_message(text: str):
    """
    Try to extract error message from AI Core 500 HTML response.
    """
    start_keyword = "Exception Value:"
    end_keyword = "Request information"

    beginning = text.find(start_keyword)
    end = text.find(end_keyword)

    if beginning == -1 or end == -1:
        return "Internal Server Error"
    else:
        return text[beginning + len(start_keyword) + 1:end - 1]
