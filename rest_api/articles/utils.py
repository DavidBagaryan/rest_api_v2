class DisplayNameMixin:
    name = None
    title = None

    def __str__(self):
        return self.name or self.title
