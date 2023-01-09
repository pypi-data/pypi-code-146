import traceback

def get_exception_str(e: Exception) -> str:
    return str(e) + '\n' + traceback.format_exc()
