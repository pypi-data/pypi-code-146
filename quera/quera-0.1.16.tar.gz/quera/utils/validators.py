def is_colab():
    try:
        from google.colab import drive
        return True
    except Exception as e:
        return False
