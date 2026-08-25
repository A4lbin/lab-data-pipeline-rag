from queries import (
    get_sample_by_uid,
    get_samples_by_peptide,
    get_samples_by_well,
    get_all_samples
)
from document import sample_to_text

def retrieve_sample_by_uid(uid):

    sample = get_sample_by_uid(uid)

    #change this code below laterrr :/
    if sample is None:
        return None

    return dict(sample)

def retrieve_samples_by_peptide(peptide):

    samples = get_samples_by_peptide(peptide)

    return [dict(sample) for sample in samples]


def retrieve_samples_by_well(wellcode):

    samples = get_samples_by_well(wellcode)

    return [dict(sample) for sample in samples]


def retrieve_all_samples():

    samples = get_all_samples()

    return [dict(sample) for sample in samples]

def retrieve_all_as_text():

    samples = retrieve_all_samples()

    documents = []

    for sample in samples:
        text = sample_to_text(sample)

        documents.append({
            "uid": sample["uid"],
            "text": text
        })

    return documents

# def sample_to_text(sample):

#     return f"""
#     UID: {sample['uid']}
#     Peptide: {sample['peptide_name']}
#     Water: {sample['water']}
#     HAuCl4: {sample['haucl4']}
#     HEPES: {sample['hepes']}
#     Slot: {sample['slot']}
#     Labware Type: {sample['labwaretype']}
#     Well Code: {sample['wellcode']}
#     Well Index: {sample['wellindex']}
#     """

# documents = retrieve_all_as_text()
# print(documents)