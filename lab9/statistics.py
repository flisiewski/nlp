from collections import Counter


def present_most_common(multigrams, dash_count=1):
    multigram_counts = Counter({
        str(bigram, "utf_8"): count for bigram, count in multigrams.vocab.items()
        if str(bigram).count("_") >= dash_count
    })

    for multigram, count in multigram_counts.most_common(10):
        print("{} -> {}".format(multigram, count))
