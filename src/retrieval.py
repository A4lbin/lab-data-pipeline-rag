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

