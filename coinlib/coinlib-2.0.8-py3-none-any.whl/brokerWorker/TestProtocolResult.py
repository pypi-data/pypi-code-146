

class TestProtocolResult:
    success: bool = False
    success = False
    fetch_symbols = False
    fetch_price_for_symbol = False
    fetch_symbol_statistics = False
    no_trade_open = False
    create_limit_order = False
    im_in_check_works = False
    fetch_last_orders = False
    im_out_check_works_after_out = False
    profit_group_works = False
    profit_future_works = False
    profit_session_works = False
    position_in_position_list = False
    order_found_in_open_orders = False
    money_available = False
    no_trade_open_because_limit = False
    get_all_orders = False
    cancel_order = False
    create_order = False
    log: str = ""
    close_order = False

    def appendLog(self, log):
        print(log)
        self.log = self.log + log + "\r\n"
        return self.log
