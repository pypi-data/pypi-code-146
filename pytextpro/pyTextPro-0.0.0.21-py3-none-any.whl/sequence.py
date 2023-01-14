def pad_sequences(sequences, maxlen=None, dtype='int32', padding='pre'):
    import itertools
    for sequence in sequences:
        if len(sequence) < maxlen:                                  # if current sequence is shorter than maxlen,
            if padding == 'pre':
                temp = [0] * (maxlen - len(sequence))
                nested_seq = [sequence]
                nested_seq.insert(0, temp)
                sequence = list(itertools.chain(*nested_seq))      # flatten
            elif padding == 'post':
                sequence += [0] * (maxlen - len(sequence))          # add padding 0 until maxlen in post-position
    return sequences
