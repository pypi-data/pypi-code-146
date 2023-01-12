import re

class Video:
    def __init__(self, soup):
        self.soup = soup
        self.link = self.__getLink()

    def __getLink(self):
        download_link = ""
        # Find the download link in the HTML
        # The .mp4 link is found in an input where the id starts with "edit-debate-file-options-download-"
        # Then the link is found in the value attribute of that input
        
        download_link = self.soup.find(
            "input", {"id": re.compile(r"^edit-debate-file-options-download-")}
        )

        if download_link is not None:
            # Remove the "download_" prefix from the link
            download_link = download_link.replace("download_", "")
        else:
            try:
                # Find an input id that starts with "edit-debate-file-options-azure-httpsdebatgemist"
                download_link = self.soup.find(
                    "input", {"id": re.compile(r"^edit-debate-file-options-azure-httpsdebatgemist")}
                )
                download_link = download_link["value"]
                download_link = download_link.replace("azure_", "")
            except:
                pass

        return download_link