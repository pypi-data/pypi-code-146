import os
import json
from arkivist import Arkivist
from sometime import Sometime
from nektar import Condenser

def main():

    counter = 0
    print("Initializing tests...")

    ##################################################
    # Condenser Class                                #
    # CondenserAPI methods                           #
    ##################################################

    print(f"\nTEST: Initialize Condenser class.")
    hive = Condenser()

    start = 1
    limit = 1
    tag = "hive"
    account = "hiveio"
    author = "hivehealth"
    stimestamp = "2022-01-01T00:00:00"
    etimestamp = "2022-01-02T00:00:00"
    permlink = "the-updated-easy-onboarding-manual"
    tid = "6fde0190a97835ea6d9e651293e90c89911f933c"
    tx = {
        "ref_block_num": 56236,
        "ref_block_prefix": 2845561047,
        "expiration": "2022-11-30T11:55:00",
        "operations": [
            ["custom_json", {"required_auths": [account], "required_posting_auths": [], "id": "contract_id", "json": "{}"}]],
        "extensions": []
    }
    keys = ["STM6vJmrwaX5TjgTS9dPH8KsArso5m91fVodJvv91j7G765wqcNM9",
            "STM6vJmrwaX5TjgTS9dPH8KsArso5m91fVodJvv91j7G765wqcNM9"]
    
    """
    print(f"\nTEST: get_account_count")
    hive.get_account_count()
    
    print(f"\nTEST: get_account_history, operation = all")
    hive.get_account_history(account, start, limit)

    print(f"\nTEST: get_account_history, operation = 0")
    hive.get_account_history(account, start, limit, low=0)

    print(f"\nTEST: get_account_reputations")
    hive.get_account_reputations(start="a", limit=5)
    
    print(f"\nTEST: get_account_reputations")
    hive.get_account_reputations("ba", 10)
    
    print(f"\nTEST: get_accounts")
    accounts = ["gtg"]
    delayed_votes_active = True
    hive.get_accounts(accounts, delayed_votes_active)
    
    print(f"\nTEST: get_accounts")
    accounts = ["gtg", "abc"]
    hive.get_accounts(accounts, False)
    
    print(f"\nTEST: get_active_votes")
    hive.get_active_votes(author, permlink)
    
    print(f"\nTEST: get_active_witnesses")
    hive.get_active_witnesses()
    
    print(f"\nTEST: get_block")
    hive.get_block(1)
    
    print(f"\nTEST: get_block_header")
    hive.get_block_header(1)
    
    print(f"\nTEST: get_blog")
    start_entry_id = 10
    hive.get_blog(account, start_entry_id, limit)
    
    ## failing
    print(f"\nTEST: get_blog_authors")
    # hive.get_blog_authors(account)
    
    print(f"\nTEST: get_blog_entries")
    hive.get_blog_entries(account, 1, 1)
    
    print(f"\nTEST: get_chain_properties")
    hive.get_chain_properties()
    
    print(f"\nTEST: get_comment_discussions_by_payout")
    tag = "ctp"
    hive.get_comment_discussions_by_payout(tag, limit=10, truncate=1)
    
    print(f"\nTEST: get_config")
    hive.get_config()
    
    print(f"\nTEST: get_content")
    hive.get_content(author, permlink)
    
    print(f"\nTEST: get_content_replies")
    hive.get_content_replies(author, permlink)
    
    print(f"\nTEST: get_conversion_requests")
    hive.get_conversion_requests(account)
    
    print(f"\nTEST: get_current_median_history_price")
    hive.get_current_median_history_price()
    
    # Assert Exception:false: Supported by hivemind
    print(f"\nTEST: get_discussions_by_active")
    # hive.get_discussions_by_active(tag, limit=2, truncate=0)
    
    print(f"\nTEST: get_discussions_by_author_before_date")
    date = "2022-12-30T00:00:00"
    hive.get_discussions_by_author_before_date(author, "", date, limit=1)

    print(f"\nTEST: get_discussions_by_blog")
    hive.get_discussions_by_blog(tag, limit=2, truncate=0)
    
    # Assert Exception:false: Supported by hivemind
    print(f"\nTEST: get_discussions_by_cashout")
    # hive.get_discussions_by_cashout(tag, limit=2, truncate=0)
    
    # Assert Exception:false: Supported by hivemind
    print(f"\nTEST: get_discussions_by_children")
    # hive.get_discussions_by_children(tag, limit=2, truncate=0)

    print(f"\nTEST: get_discussions_by_comments")
    author = "hive"
    permlink = ""
    hive.get_discussions_by_comments(author, permlink, limit=1)
    
    # Assert Exception:false: Supported by hivemind
    print(f"\nTEST: get_discussions_by_created")
    # hive.get_discussions_by_created(tag, limit=2, truncate=0)
    
    print(f"\nTEST: get_discussions_by_feed")
    hive.get_discussions_by_feed(tag, author="", permlink="", limit=1)
    
    print(f"\nTEST: get_discussions_by_hot")
    hive.get_discussions_by_hot(tag, limit=2, truncate=0)
    
    print(f"\nTEST: get_discussions_by_promoted")
    hive.get_discussions_by_promoted(tag, limit=2, truncate=0)
    
    print(f"\nTEST: get_discussions")
    by = "votes"
    hive.get_discussions(by, tag, limit=2, truncate=0)
    
    print(f"\nTEST: get_escrow")
    hive.get_escrow(account="hiveio", eid=0)
    
    print(f"\nTEST: get_expiring_vesting_delegations")
    account = "hiveio"
    after = "2018-01-01T00:00:00"
    hive.get_expiring_vesting_delegations(account, after)
    
    # Assert Exception:false: Supported by hivemind
    print(f"\nTEST: get_feed")
    account = "hiveio"
    # hive.get_feed(account, eid=0, limit=1)
    
    # Assert Exception:false: Supported by hivemind
    print(f"\nTEST: get_feed_entries")
    account = "hiveio"
    # hive.get_feed_entries(account, eid=0, limit=1)
    
    print(f"\nTEST: get_follow_count")
    hive.get_follow_count(account)
    
    print(f"\nTEST: get_followers")
    hive.get_followers(account, start="", ftype="blog", limit=5)
    
    print(f"\nTEST: get_following")
    hive.get_following(account, start="", ftype="blog", limit=5)
    
    print(f"\nTEST: get_hardfork_version")
    hive.get_hardfork_version()
    
    print(f"\nTEST: get_key_references")
    hive.get_key_references(keys)
    
    # TODO: re-validate
    print(f"\nTEST: get_market_history")
    hive.get_market_history(seconds=3600, start=stimestamp, end=etimestamp)
    
    print(f"\nTEST: get_market_history_buckets")
    hive.get_market_history_buckets()
    
    print(f"\nTEST: get_next_scheduled_hardfork")
    hive.get_next_scheduled_hardfork()
    
    print(f"\nTEST: get_open_orders")
    hive.get_open_orders(account)
    
    print(f"\nTEST: get_ops_in_block")
    hive.get_ops_in_block(number=5443322, virtual=True)
    
    print(f"\nTEST: get_order_book")
    hive.get_order_book(limit=5)
    
    print(f"\nTEST: get_owner_history")
    hive.get_owner_history(account)
    
    print(f"\nTEST: get_potential_signatures")
    hive.get_potential_signatures(tx)
    
    print(f"\nTEST: get_reblogged_by")
    hive.get_reblogged_by(author, permlink)
    
    print(f"\nTEST: get_recent_trades")
    hive.get_recent_trades(limit=5)
    
    print(f"\nTEST: get_recovery_request")
    hive.get_recovery_request(account)
    
    print(f"\nTEST: get_replies_by_last_update")
    hive.get_replies_by_last_update(author="hive", permlink="", limit=1)
    
    print(f"\nTEST: get_required_signatures")
    hive.get_required_signatures(transaction=tx, keys=[])
    
    print(f"\nTEST: get_reward_fund")
    hive.get_reward_fund(action="post")
    
    print(f"\nTEST: get_savings_withdraw_from")
    hive.get_savings_withdraw_from(account)
    
    print(f"\nTEST: get_savings_withdraw_to")
    hive.get_savings_withdraw_to(account)
    
    # Assert Exception:false: Supported by hivemind
    print(f"\nTEST: get_tags_used_by_author")
    # hive.get_tags_used_by_author(account)
    
    print(f"\nTEST: get_ticker")
    hive.get_ticker()
    
    print(f"\nTEST: get_trade_history")
    hive.get_trade_history(start=stimestamp, end=etimestamp, limit=10)
    
    print(f"\nTEST: get_transaction")
    hive.get_transaction(tid)
    
    print(f"\nTEST: get_transaction_hex")
    hive.get_transaction_hex(transaction=tx)
    
    print(f"\nTEST: get_trending_tags")
    hive.get_trending_tags(start="", limit=10)
    
    print(f"\nTEST: get_version")
    hive.get_version()
    
    print(f"\nTEST: get_vesting_delegations")
    hive.get_vesting_delegations(account, start="", limit=5)
    
    print(f"\nTEST: get_volume")
    hive.get_volume()
    
    print(f"\nTEST: get_withdraw_routes")
    hive.get_withdraw_routes(account, route="all")
    
    print(f"\nTEST: get_witness_by_account")
    hive.get_witness_by_account(account)
    
    print(f"\nTEST: get_witness_count")
    hive.get_witness_count()
    
    print(f"\nTEST: get_witness_count")
    hive.get_witness_count()
    
    print(f"\nTEST: get_witness_schedule")
    hive.get_witness_schedule()
    
    print(f"\nTEST: get_witnesses")
    hive.get_witnesses(indices=[0,19,20])
    
    print(f"\nTEST: get_witnesses_by_vote")
    hive.get_witnesses_by_vote(start="a", limit=5)
    
    print(f"\nTEST: lookup_account_names")
    hive.lookup_account_names(accounts=[account], delayed_votes_active=False)
    
    print(f"\nTEST: lookup_accounts")
    hive.lookup_accounts(start="a", limit=5)
    
    print(f"\nTEST: find_proposals")
    hive.find_proposals(pid=0)
    
    print(f"\nTEST: list_proposal_votes, by proposal voter")
    order = "by_proposal_voter"
    direction = "ascending"
    hive.list_proposal_votes(start, limit, order, direction, status="all")
    
    print(f"\nTEST: list_proposal_votes, by voter proposal")
    start = "gtg"
    order = "by_voter_proposal"
    direction = "descending"
    status = "active"
    hive.list_proposal_votes(start, limit, order, direction, status)
    
    print(f"\nTEST: list_proposals, by creator")
    start = "gtg"
    order = "by_creator"
    direction = "ascending"
    status = "active"
    hive.list_proposals(start, limit, order, direction, status)
    
    print(f"\nTEST: list_proposals, by start date")
    start = "2022-01-01T00:00:00"
    limit = 5
    order = "by_start_date"
    direction = "ascending"
    status = "active"
    hive.list_proposals(start, limit, order, direction, status)
    
    print(f"\nTEST: list_proposals, by end date")
    start = "2022-12-30T00:00:00"
    limit = 5
    order = "by_end_date"
    direction = "ascending"
    status = "active"
    hive.list_proposals(start, limit, order, direction, status)
    
    print(f"\nTEST: list_proposals, by total votes")
    start = 0
    limit = 5
    order = "by_total_votes"
    direction = "ascending"
    status = "active"
    hive.list_proposals(start, limit, order, direction, status)
    
    print(f"\nTEST: is_known_transaction")
    hive.is_known_transaction(tid)
    
    print(f"\nTEST: get_collateralized_conversion_requests")
    hive.get_collateralized_conversion_requests(account)
    
    print(f"\nTEST: find_recurrent_transfers")
    hive.find_recurrent_transfers(account)
    
    print(f"\nTEST: find_rc_accounts")
    hive.find_rc_accounts(accounts=account)
    
    print(f"\nTEST: list_rc_accounts")
    hive.list_rc_accounts(account, limit=5)
    
    print(f"\nTEST: list_rc_direct_delegations")
    hive.list_rc_direct_delegations(delegator="oniemaniego", delegatee="hivehealth", limit=5)
    """

if __name__ == "__main__":
    main()
