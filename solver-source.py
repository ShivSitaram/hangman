from string import ascii_lowercase, punctuation, digits
from re import search

def avail_words(phrase):
    with open('wordlists/wordlist.txt', 'r') as f:
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
    phrase = '#'
    letters_rem_list = []
    while phrase != '':
        old = phrase
        phrase = input("Revealed: (use a '_' or '?' for unknown) ").lower()
        if ['?' if ch == '_' or ch == '?' else ch for ch in phrase] == ['?' if ch == '_' or ch == '?' else ch for ch in old]:
            letters_rem = input("Letters removed: (enter if none this turn) ")
            letters_rem_list.append(letters_rem)
        freq = best_gss(phrase, avail_words(phrase))
        for l in sorted(freq, key=freq.get, reverse=True):
            if l not in phrase:
                if l not in letters_rem_list:
                    print(l, freq[l])

if __name__ == '__main__':
    main()
