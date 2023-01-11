class Stringable(object):

    def __str__(self):
        return (
            self.__class__.__name__ + "(" + ', '.join(
                [str(k) + '=' + str(v) for k, v in self.__dict__.items()]
            ) + ")"
        )


class Representable(object):

    def __repr__(self):
        return (
            self.__class__.__name__ + "(" + ', '.join(
                [str(k) + '=' + str(v) for k, v in self.__dict__.items()]
            ) + ")"
        )


class Printable(Stringable, Representable):
    pass
