import pandas as pd, numpy as np
from nltk.corpus import stopwords
from nltk import word_tokenize
from collections import Counter
import unidecode
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Create list of stop words for analyzing Narrative text
stop_words = list(set(stopwords.words("english")))
stop_words = stop_words + ['\"', '\'', ',', ';', ':', '-', '~', '?',
                           '!', '.', '(', ')', '[', ']', '{', '}', '/',
                           '&', 'airplane', 'aircraft', 'pilot', 'nan']

# Import flattened CSV census data into dataframe
df = pd.read_csv('../output/Full_Aviation_Data.csv')
num_rows = len(df)
word_cloud_max = 25
df = df.head(n=num_rows)
df['probable_cause'] = df['probable_cause'].astype(str)
df['narrative'] = df['narrative'].astype(str)

df['probable_cause'] = df['probable_cause'].apply(lambda x: x + ' ')

all_terms = word_tokenize(df['probable_cause'].astype(str).agg('sum'))
all_terms = [x.lower() for x in all_terms if x.lower() not in stop_words]
all_counts = Counter(all_terms).most_common()

prob_dict = {}
for term, freq in all_counts:
    prob_dict[term] = float(freq)/float(num_rows)

# Function to extract first sentence of probable_cause.
def get_ntsb_disclaimer(row):
    txt = row['narrative']
    if isinstance(txt, bytes):
        return np.NaN
    elif 'NTSB' not in txt:
        return 'N/A'
    else:
        ntsb_start = txt.upper().find('NTSB')
        ntsb_end = txt.find('.')+1
        return txt[ntsb_start:ntsb_end].upper().strip()


# Function to extract term frequencies for probable_cause text
def get_term_frequencies(row):
    txt = unidecode.unidecode(row['probable_cause'])
    if isinstance(txt, bytes):
        return np.NaN
    else:
        # Exclude disclaimer text from frequency counts and tokenize terms
        #new_txt = word_tokenize(txt.replace(row['first_sentence'], "").lower())
        new_txt = word_tokenize(txt.lower())

        # Remove stop words from list of tokenized words
        new_txt = [x for x in new_txt if x not in stop_words]

        # Retrieve term frequencies to return top 5 terms by count
        counts = Counter(new_txt).most_common()

        return counts[0:100]


# Extract first sentence of narrative text
df['first_sentence'] = df.apply(get_ntsb_disclaimer, axis=1)

# Pull top term frequencies for each probable_cause text
df['term_frequencies'] = df.apply(get_term_frequencies, axis=1)

df = df[df['term_frequencies'] != np.NaN]

by_var = 'AircraftDamage'
y = pd.DataFrame({'term_frequencies': df.groupby(by_var)['term_frequencies'].apply(lambda x: x.sum()),
                  'count': df[by_var].value_counts()})
y = y.reset_index()


def sum_term_freqs(lst,top_x):
    new_lst = []
    for i in lst:
        for j in range(0, i[1]):
            new_lst.append(i[0])
    counts = Counter(new_lst).most_common()
    return counts[0:top_x]


def sum_term_frequencies(row):
    lst = []
    counts = sum_term_freqs(row['term_frequencies'], 1000)
    for term, freq in counts:
        weight = float(freq) / float(row['count'])
        try:
            if weight / prob_dict[term] > 1:
                lst.append((term, (weight/prob_dict[term])*freq))
        except KeyError:
            if weight / prob_dict[term[:-1]] > 1:
                lst.append((term, (weight/prob_dict[term[:-1]])*freq))
    lst.sort(key=lambda tup: tup[1], reverse=True)
    return lst[0:word_cloud_max]


y['frequency_sums'] = y.apply(sum_term_frequencies, axis=1)
index_list = ['Minor', 'Substantial', 'Destroyed']


# Create wordcloud image for the indices used to group frequency counts
def create_wordcloud_by_index(index_list):
    for index_val in index_list:
        term_counts = list(y[y['index'] == index_val]['frequency_sums'])[0]
        cloud_text = ' '.join([i[0] for i in term_counts])
        wordcloud = WordCloud(max_font_size=40, background_color='white').generate(cloud_text)

        # Display the generated image:
        # the matplotlib way:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.title(index_val + ': Most Informative Terms')
        plt.savefig('../output/figs/wordcloud/' + index_val + '_wordcloud.png', bbox_inches='tight')
        plt.close()


create_wordcloud_by_index(index_list)
