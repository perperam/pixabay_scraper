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
        BAR_SIZE = 30
        test_value = lambda isv : 1 if (isv > 0) else 0
        equal = round(BAR_SIZE * self.is_value/self.to_value) -1
        under = BAR_SIZE - equal

        if self.is_value == 0:
            equal = 0
            under = BAR_SIZE
        if self.is_value == self.to_value:
            under = 0
            equal = BAR_SIZE

        bar = "=" * equal + ">" * test_value(self.is_value/self.to_value) + "_" * under

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
