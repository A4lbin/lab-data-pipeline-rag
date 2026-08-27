from .retrieval import (
    retrieve_sample_by_uid,
    retrieve_samples_by_peptide,
    retrieve_samples_by_well,
    retrieve_all_samples
)

sample = retrieve_sample_by_uid("2021-12-29Z2M6I_S5_A1")
print("UID result:")
print(sample)

samples = retrieve_samples_by_peptide("Z2M246I")
print("\nPeptide results:")
print(samples)

well_samples = retrieve_samples_by_well("A1")
print("\nWell results:")
print(well_samples)

all_samples = retrieve_all_samples()
print("\nTotal samples:")
print(len(all_samples))