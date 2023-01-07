import matplotlib.pyplot as plt
from collections import Counter

def plot_words(word_counts, n=10):
    """Plot a bar chart of word counts.

    Parameters
    ----------
    word_counts : collections.Counter
        Counter object of word counts.
    n : int, optional
        Plot the top n words. By default, 10.

    Returns
    -------
    matplotlib.container.BarContainer
        Bar chart of word counts.

    Examples
    --------
    >>> from pkgs_test.pkgs_test import count_words
    >>> from pkgs_test.plotting import plot_words
    >>> counts = count_words("text.txt")
    >>> plot_words(counts)
    """
    if not type(word_counts) == Counter:
        raise TypeError(f"'word_counts' need to be of type 'Counter'!")
    top_n_words = word_counts.most_common(n)
    word, count = zip(*top_n_words)
    fig = plt.bar(range(n), count)
    plt.xticks(range(n), labels=word, rotation=45)
    plt.xlabel("Word")
    plt.ylabel("Count")
    return fig