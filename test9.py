'''from statistics import mode


def most_common(List):
    return (mode(List))


List = ["a", "b", "b", "c", "a", "c"]
print(most_common(List)) '''

from collections import Counter


def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0:][0]


List = ["a", "b", "b", "c", "c", "c","c"]
a = int(most_frequent(List)[1])
if a > 3:
    print(most_frequent(List)[0])