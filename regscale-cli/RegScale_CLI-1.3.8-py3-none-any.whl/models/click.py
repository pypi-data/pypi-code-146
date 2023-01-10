#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Module to allow dynamic click arguments """

# stand python imports
import click


class NotRequiredIf(click.Option):
    def __init__(self, *args, **kwargs):
        """
        updates the help command to let the user know if a command is exclusive or not
        """
        self.not_required_if: list = kwargs.pop("not_required_if")

        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs["help"] = (
            kwargs.get("help", "")
            + "Option is mutually exclusive with "
            + ", ".join(self.not_required_if)
            + "."
        ).strip()
        super(NotRequiredIf, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        """
        function to handle the click arguments and whether a parameter is required
        """
        current_opt: bool = self.name in opts
        for mutex_opt in self.not_required_if:
            if mutex_opt in opts:
                if current_opt:
                    raise click.UsageError(
                        "Illegal usage: '"
                        + str(self.name)
                        + "' is mutually exclusive with "
                        + str(mutex_opt)
                        + "."
                    )
                else:
                    self.prompt = None
        return super(NotRequiredIf, self).handle_parse_result(ctx, opts, args)
