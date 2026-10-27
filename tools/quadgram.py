#!/usr/bin/env python3
"""English quadgram log-probability model (w-gromark 2026-10-26).
Build: python3 quadgram.py build OUT.tsv TEXT1 [TEXT2 ...]   (Project Gutenberg plain-text files;
       header/footer stripped at the *** START/END *** markers; letters A-Z only, joined).
Use:   from quadgram import load; qg = load(path); qg.score(text)  -> mean log10 P per scored quadgram
       Quadgrams containing '?' are skipped. Unseen quadgrams get log10(0.01/N).
Default corpus used by w-gromark: PG #2600 (War and Peace) + PG #1342 (Pride and Prejudice)."""
import sys, math, re, collections

def clean(path):
    t = open(path, encoding="utf-8", errors="ignore").read()
    m = re.search(r"\*\*\* ?START OF.*?\*\*\*", t); n = re.search(r"\*\*\* ?END OF", t)
    t = t[m.end() if m else 0: n.start() if n else len(t)]
    return re.sub("[^A-Z]", "", t.upper())

class QG:
    def __init__(self, counts):
        self.N = sum(counts.values())
        self.lp = {k: math.log10(v / self.N) for k, v in counts.items()}
        self.floor = math.log10(0.01 / self.N)
    def quads(self, text, mask=None):
        """yield log-probs of quadgrams with no '?'; mask (set of indices) -> only quads touching mask"""
        for i in range(len(text) - 3):
            q = text[i:i + 4]
            if "?" in q: continue
            if mask is not None and not any(j in mask for j in range(i, i + 4)): continue
            yield self.lp.get(q, self.floor)
    def score(self, text, mask=None):
        v = list(self.quads(text, mask))
        return (sum(v) / len(v), len(v)) if v else (float("nan"), 0)

def load(path):
    c = {}
    for line in open(path):
        q, n = line.split(); c[q] = int(n)
    return QG(c)

if __name__ == "__main__":
    if sys.argv[1] == "build":
        txt = "".join(clean(p) for p in sys.argv[3:])
        c = collections.Counter(txt[i:i + 4] for i in range(len(txt) - 3))
        with open(sys.argv[2], "w") as f:
            for q, n in c.most_common(): f.write(f"{q} {n}\n")
        print(len(txt), "letters", len(c), "quadgrams")
