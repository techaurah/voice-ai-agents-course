"""Metrics for transcripts and conversations."""

import string

_PUNCT = str.maketrans("", "", string.punctuation)


def tokens(text):
    return text.lower().translate(_PUNCT).split()


def edit_counts(ref, hyp):
    """Word-level Levenshtein breakdown: (substitutions, deletions,
    insertions) turning ref into hyp."""
    r, h = tokens(ref), tokens(hyp)
    m, n = len(r), len(h)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if r[i - 1] == h[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1,
                           dp[i - 1][j - 1] + cost)
    subs = dels = ins = 0
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and r[i - 1] == h[j - 1]:
            i, j = i - 1, j - 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            subs += 1
            i, j = i - 1, j - 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            dels += 1
            i -= 1
        else:
            ins += 1
            j -= 1
    return subs, dels, ins


def wer(ref, hyp):
    """Word error rate of hyp against ref, rounded to 4 places."""
    r = tokens(ref)
    if not r:
        return 0.0
    subs, dels, ins = edit_counts(ref, hyp)
    return round((subs + dels + ins) / len(r), 4)


def mean(values):
    return round(sum(values) / len(values), 4) if values else 0.0
