from database import get_connection

def get_sample_by_uid(uid):

    connection = get_connection()

    result = connection.execute("""
        SELECT *
        FROM samples
        WHERE uid = ?
    """, (uid,)).fetchone()

    connection.close()
    return result

def get_samples_by_peptide(peptide):
    connection = get_connection()

    results = connection.execute("""
        SELECT *
        FROM samples
        WHERE peptide_name = ?
    """, (peptide,)).fetchall()

    connection.close()
    return results

def get_samples_by_well(wellcode):

    connection = get_connection()

    results = connection.execute("""
        SELECT *
        FROM samples
        WHERE wellcode = ?
    """, (wellcode,)).fetchall()

    connection.close()
    return results

def get_peptide_counts():

    connection = get_connection()

    results = connection.execute("""
        SELECT
            peptide_name,
            COUNT(*) AS sample_count
        FROM samples
        GROUP BY peptide_name
        ORDER BY sample_count DESC
    """).fetchall()

    connection.close()
    return results

def get_all_samples():

    connection = get_connection()

    results = connection.execute("""
        SELECT *
        FROM samples
    """).fetchall()

    connection.close()
    return results