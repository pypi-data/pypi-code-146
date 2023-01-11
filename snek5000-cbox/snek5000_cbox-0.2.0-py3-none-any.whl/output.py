from snek5000.output.base import Output as OutputBase

from snek5000_cbox.templates import box, size, makefile_usr


class OutputCbox(OutputBase):
    template_box = box
    template_makefile_usr = makefile_usr
    template_size = size

    @property
    def makefile_usr_sources(self):
        """
        Sources for inclusion to makefile_usr.inc
        Dict[directory]  -> list of source files
        """
        return {
            "toolbox": [
                ("frame.f", "FRAMELP"),
                ("mntrlog_block.f", "MNTRLOGD"),
                ("mntrlog.f", "MNTRLOGD"),
                ("mntrtmr_block.f", "MNTRLOGD", "MNTRTMRD"),
                ("mntrtmr.f", "MNTRLOGD", "MNTRTMRD", "FRAMELP"),
                ("rprm_block.f", "RPRMD"),
                ("rprm.f", "RPRMD", "FRAMELP"),
                ("io_tools_block.f", "IOTOOLD"),
                ("io_tools.f", "IOTOOLD"),
                ("chkpoint.f", "CHKPOINTD"),
                ("chkpt_mstp.f", "CHKPTMSTPD", "CHKPOINTD"),
                ("map2D.f", "MAP2D", "FRAMELP"),
                ("stat.f", "STATD", "MAP2D", "FRAMELP"),
                ("stat_IO.f", "STATD", "MAP2D", "FRAMELP"),
                ("sfd.f", "SFDD", "FRAMELP"),
                ("math_tools.f",),
            ],
        }


Output = OutputCbox
