from string import ascii_lowercase, punctuation, digits
from re import search

def avail_words(phrase):
    with open('all words.txt', 'r') as f:
        ws = [word.rstrip('\n').lower() for word in f.readlines() if not bool(search('[' + punctuation + digits + ']', word)) and len(word) == len(phrase) + 1]
    for n, l in enumerate(phrase):
        if l != '_' and l != '?':
            ws = [word for word in ws if word[n] == l]

    return ws

def best_gss(phrase, avail):
    freq = {l:0 for l in ascii_lowercase}
    for wrd in avail:
        for l in (wrd):
            freq[l] += 1
    return freq

def main():
    phrase = None
    while phrase != '':
        phrase = input("Revealed: (use a '_' or '?' for unknown) ").lower()
        freq = best_gss(phrase, avail_words(phrase))
        for l in sorted(freq, key=freq.get, reverse=True):
            if l not in phrase:
                print(l, freq[l])

if __name__ == '__main__':
    main()
