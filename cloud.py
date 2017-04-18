
"""
Minimal Example
===============

Generating a square wordcloud from the US constitution using default arguments.
"""

from os import path
from wordcloud import WordCloud

d = path.dirname(__file__)

# Read the whole text.
text = open(path.join(d, 'constitution.txt')).read()

# Generate a word cloud image
wordcloud = WordCloud().generate(text)

# Display the generated image:
# the matplotlib way:
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(text)
print wordcloud
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
print "DONE SHOW CLOUD"
# The pil way (if you don't have matplotlib)
image = wordcloud.to_image()
image.show()