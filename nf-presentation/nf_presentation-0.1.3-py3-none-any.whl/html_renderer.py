import html2text
class HTMLRenderer:
    def render(self,html:str) -> str:
        return html2text.html2text(html)