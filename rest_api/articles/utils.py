class DisplayNameMixin:
    name = None

    def __str__(self):
        return self.name
