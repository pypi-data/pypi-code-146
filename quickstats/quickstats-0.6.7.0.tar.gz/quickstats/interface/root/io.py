def redirect_print_stream(streamer):
    import ROOT
    old_streamer = ROOT.RooPrintable.defaultPrintStream(streamer)
    return old_streamer

def get_default_stream():
    import ROOT
    return ROOT.RooPrintable.defaultPrintStream()