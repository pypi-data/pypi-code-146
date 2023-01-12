from gandai.datastore import Cloudstore
from gandai.models import Event
from gandai.services import Query

ds = Cloudstore()

from time import time
def load_search(search_key: str, actor_key: str = "") -> dict:
    # Event.post_event(
    #     actor_key=actor_key, search_key=search_key, domain="", type="search"
    # )  # hmm really?

    t0 = time()
    companies = Query.companies_query(search_key)
    events = Query.events_query(search_key)
    comments = Query.comments_query(search_key)
    print("queries:", (time()-t0))

    def _get_comments(domain: str) -> list:
        if len(comments) == 0:
            return []
        return comments.query("domain == @domain").to_dict(orient="records")

    def _get_events(domain: str) -> list:
        if len(events) == 0:
            return []
        return events.query("domain == @domain").to_dict(orient="records")
        

    companies["comments"] = companies["domain"].apply(_get_comments)
    companies["events"] = companies["domain"].apply(_get_events)
    companies["last_event_type"] = companies["events"].apply(
        lambda x: x[-1]["type"] if len(x) > 0 else "created"
    )

    def _companies_by_state(last_event_type: str) -> list:
        df = companies.query("last_event_type == @last_event_type")
        return df.fillna("").to_dict(orient="records")

    
    inbox = _companies_by_state("created")
    review = _companies_by_state("advance")
    qualified = _companies_by_state("qualify")
    rejected = _companies_by_state("reject")

    resp = {
        "search_key": search_key,
        "actor_key": actor_key,
        "meta": {},
        "companies": {
            "inbox": inbox,
            "review": review,
            "qualified": qualified,
            "rejected": rejected,
        },
    }
    return resp


