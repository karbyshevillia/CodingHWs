#!/usr/bin/env python3

def analyse_string(string):
    sequences = []
    current_sequence = ""
    counter = 0
    while counter in range(len(string)):
        symb = string[counter]
        current_sequence += symb
        if counter == len(string) - 1 or string[counter + 1] != symb:
            sequences.append(current_sequence)
            current_sequence = ""
        counter += 1
    max_seq = max(sequences, key=len)
    return [max_seq[0], len(max_seq)]

class JSONConsecutiveSymbols:

    def __init__(self, string):
        S = analyse_string(string)
        self.dict = {'symbol': S[0], 'max_as_consecutive': S[1]}


if __name__ == '__main__':
    d = JSONLetters('aaaabbbbbbbbbbbrrrrgggrrrrrrrrrrrrrrrrhhh    jjj')
    print(d.dict)