# Usage: streamlit run barfi_app.py

from barfi import st_barfi, Block

feed = Block(name='Feed')
feed.add_input()
result = Block(name='Result')
result.add_output()

barfi_result = st_barfi(base_blocks=[feed, result])
