from queries import get_sample_by_uid


def retrieve_sample_by_uid(uid):

    sample = get_sample_by_uid(uid)

    #change this code below laterrr :/
    if sample is None:
        return None

    return dict(sample)


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
    """