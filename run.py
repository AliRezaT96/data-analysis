import matplotlib.pyplot as plt
from analysis import analize_text


if __name__ == '__main__':
    plt.show(analize_text.TokenDestribution())
    plt.show(analize_text.plot_value_per_attribute())
    plt.show(analize_text.plot_word_count())
    plt.show(analize_text.mean_number_of_tokens())
    plt.show(analize_text.NgramsValue())
    plt.show(analize_text.word_cloud())