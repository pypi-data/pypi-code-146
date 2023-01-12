# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116


"config"


from opr import Cfg, edit, keys, last, printable, write


def cfg(event):
    last(Cfg)
    if not Cfg.prs.txt:
        event.reply("config is empty")
        return
    if not event.sets:
        event.reply(printable(
                              Cfg,
                              keys(Cfg),
                              skip="name,password,prs",
                             )
                   )
    else:
        edit(Cfg, event.sets)
        write(Cfg)
        event.done()
