def sample_to_text(sample):

    return f"""
    UID: {sample['uid']}
Peptide: {sample['peptide_name']}
Water: {sample['water']}
HAuCl4: {sample['haucl4']}
HEPES: {sample['hepes']}
Slot: {sample['slot']}
Labware Type: {sample['labwaretype']}
Well Code: {sample['wellcode']}
Well Index: {sample['wellindex']}
""".strip()

# def samples_to_text(samples):

#     return [sample_to_text(sample) for sample in samples]

def samples_to_text(samples):

    documents = []

    for sample in samples:

        documents.append({
            "uid": sample["uid"],
            "text": sample_to_text(sample)
        })

    return documents