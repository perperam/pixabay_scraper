class Progressbar():
    def __init__(self, to_value, name="", prefix="Progress:", suffix="Complete"):
        self.to_value = to_value
        self.is_value = 0
        self.name = name
        self.prefix = prefix
        self.suffix = suffix
        self.form = "\r{prefix} [{bar}] {is_value}/{to_value} {name} {suffix} "
        self.print_bar()

    def print_bar(self):
        test_value = lambda isv : 1 if (isv > 0) else 0
        bar = "=" * (self.is_value - 1) + ">" * test_value(self.is_value) + "_" * (self.to_value - self.is_value)
        print(self.form.format(
            bar=bar,
            prefix = self.prefix,
            name = self.name,
            suffix = self.suffix,
            is_value=self.is_value,
            to_value=self.to_value,
            ), end="\r")
        if self.is_value == self.to_value:
            print()

    def add(self, value):
        self.is_value += value
        self.print_bar()

    def set(self, value):
        self.is_value = value
        self.print_bar()
