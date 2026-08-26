from queries import (
    get_sample_by_uid,
    get_samples_by_peptide,
    get_samples_by_well,
    get_peptide_counts,
    get_all_samples,
    filter_samples
)

# sample = get_sample_by_uid("2021-07-22Z2M246I_S4_A1")
# print("\nSample:")
# print(sample)


# samples = get_samples_by_peptide("Z2M246I")
# print("\nSamples for peptide:")
# print(samples)


# well_samples = get_samples_by_well("A1")
# print("\nSamples in well:")
# print(well_samples)


# counts = get_peptide_counts()
# print("\nPeptide counts:")
# print(counts)


# all_samples = get_all_samples()
# print("\nNumber of samples:")
# print(len(all_samples))

filters = [
    {
        "field": "haucl4",
        "operator": "=",
        "value": "0.0002"
    }
]

results = filter_samples(filters)
print(len(results))
# for row in results:
#     print(row["peptide_name"])
# print(row["peptide_name"] for row in results)
print([row["haucl4"] for row in results])