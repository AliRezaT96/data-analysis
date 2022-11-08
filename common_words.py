import matplotlib.pyplot as plt
from analysis import common_words

attr1 = input('Enter first attribute for common words:')
attr2 = input('Enter second attribute for common words:')
plt.show(common_words(attr1, attr2))