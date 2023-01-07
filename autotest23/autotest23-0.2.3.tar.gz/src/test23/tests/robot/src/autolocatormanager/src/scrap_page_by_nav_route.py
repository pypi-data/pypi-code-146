import re
import sys
from bs4 import BeautifulSoup
from .abstract.i_scrap_page_by_nav_route import IScrapPageByNavRoute


class ScrapPageByNavRoute(IScrapPageByNavRoute):
    
    def scrap_targeted_page(self, base_url: str, locators_and_tags: dict) -> dict:
        print("This operation will take a while....")
        for page in locators_and_tags:
            page_content = locators_and_tags[page]
            hyper_link = self._get_routing_link(base_url, page_content)
            if hyper_link is None:
                locators_and_tags[page] = None
            else: 
                locators_and_tags[page] = {
                    'page_payload': self.web_scraper_obj.scraper(hyper_link)
                    }  
                # sys.stdout.write("-")
                # sys.stdout.flush()
                print(f"==> {page} <==")        
        return locators_and_tags
    
    def _get_routing_link(self, base_url: str, locators_and_tags: dict) -> str:
        tag = locators_and_tags['tag']
        if 'href' in tag.attrs:
            hyper_link = tag.attrs['href']
            base_domain = base_url.split('/')[2]
            # if base_url == hyper_link:
            #     return None

            if base_domain not in hyper_link and "http" in hyper_link:
                print(f"Link: {hyper_link} \n is skipping, because its not the same domain of base_url")
                return None

            if re.match(self.web_scraper_obj.URL_VALIDATOR_CHAR, hyper_link) is None:
                url_start = re.search("^/", hyper_link)
                link_end = re.search("/$", base_url)
                if url_start and link_end:
                    hyper_link = f"{base_url}{hyper_link[1:]}"
                elif url_start or link_end:
                    hyper_link = f"{base_url}{hyper_link}"
                else:
                    hyper_link = f"{base_url}/{hyper_link}"
            return hyper_link

        else:
            print(f"Tag: {tag} \n This tag do not have any hyperlink for routing")
            return None
