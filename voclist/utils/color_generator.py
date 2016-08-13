"""
Contains the ColorGenerator class.
"""
from math import ceil, floor

__author__ = "Basile Vu <basile.vu@gmail.com>"


class ColorGenerator:
    """
    Allows generation of hex colors as strings in the form #rgb from a given integer.

    The "step" parameter allows to generate different ranges of values.
    For example step = 1 will give (1 -> #001 means for the value 1, #001 is generated):

        0 -> #000,
        1 -> #001,
        2 -> #002,
        3 -> #003,
        ...

    whereas step = 3 will give
        0 -> #000,
        1 -> #003,
        2 -> #006,
        3 -> #009,
        ...

    The max "whiteness" of the colors generated can be controlled with
    the "cp_max_value" parameter. It represents the max value that each color part
    r, g and b can have at the same time.

    For example, if cp_max_value is 9, #999, #aa9, #a9a, #9aa are valid, but not #aaa.

    :param step: defines the range for the generated values.
    :param cp_max_value: defines the colors that can be generated.
    """

    def __init__(self, step=1, cp_max_value=15):
        self.step = step
        self.n_multiples = ceil(16/step)
        self.ban_list = [
            hex(r) + hex(g).strip("0x") + hex(b).strip("0x")
            for r in range(16)
            for g in range(16)
            for b in range(16)
            if r > cp_max_value and g > cp_max_value and b > cp_max_value
            and r % step == 0 and g % step == 0 and b % step == 0
        ]
        self.MAX_VALUE = self.n_multiples ** 3 - len(self.ban_list)

    def gen_color(self, n):
        """
        Generates an hex color as string in the form #xyz.
        """
        n %= self.MAX_VALUE
        r = hex(floor(n / (self.n_multiples ** 2)) * self.step)
        g = hex(floor((n % (self.n_multiples ** 2)) / self.n_multiples) * self.step).split("0x")[1]
        b = hex((n % self.n_multiples) * self.step).split("0x")[1]

        res = r + g + b
        if res in self.ban_list:
            return self.gen_color(n + 1)

        return "#" + res.split("0x")[1].rjust(3, "0")
