# The MIT License (MIT)
#
# Copyright (c) 2016 Litrin Jiang
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from abc import ABCMeta

__all__ = [
    'Normal',
    'NormalS',
    'MA',
    'EMA',
]


class BaseAverage:
    __metaclass__ = ABCMeta

    count = 0
    value = 0.0

    def add_sample(self, sample):
        self.count += 1
        if self.count == 1:
            self.value = sample

            # raise ImportError("Method haven't implemented!")
    def add(self,sample):
        return self.add_sample(sample)

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __float__(self):
        return self.value

    def __len__(self):
        return self.count

    def __add__(self, other):
        return self.value + other.value

    def __sub__(self, other):
        return self.value - other.value


class Normal(BaseAverage):
    sample_list = []

    def add_sample(self, sample):
        self.count += 1
        self.sample_list.append(sample)
        self.value = reduce(lambda a, b: a + b, self.sample_list) / float(
            self.count)

        return self.value


class NormalS(BaseAverage):
    value = 0.0

    def add_sample(self, sample):
        self.value = (self.value * self.count + sample) / (self.count + 1)
        self.count += 1

        return self.value


class MA(BaseAverage):
    def add_sample(self, sample):
        BaseAverage.add_sample(self, sample)
        self.value = (self.value + sample) / 2.0

        return self.value


class EMA(BaseAverage):
    window_size = None
    alpha = 1

    def __init__(self, window_size):
        self.window_size = window_size
        self.alpha = 2.0 / (window_size + 1)

    def add_sample(self, sample):
        BaseAverage.add_sample(self, sample)
        self.value += (sample - self.value) * self.alpha

        return self.value
