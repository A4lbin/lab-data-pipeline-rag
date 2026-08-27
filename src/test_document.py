from .retrieval import retrieve_all_samples
from .document import samples_to_text

samples = retrieve_all_samples()

documents = samples_to_text(samples)

print(len(documents))
for i in documents:
    # help(i)
    print(i['text'])
    print("\n")
# print(documents)