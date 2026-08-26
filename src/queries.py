from database import get_connection

ALLOWED_FIELDS = {
    "uid",
    "peptide_name",
    "peptide",
    "water",
    "haucl4",
    "hepes",
    "slot",
    "wellcode",
    "wellindex",
    "labwaretype"
}

ALLOWED_OPERATORS = {
    "=",
    "!=",
    "<",
    ">",
    "<=",
    ">=",
    "IN",
    "NOT IN"
}

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

def filter_samples(filters):

    connection=get_connection()

    conditions = []
    values = []

    for filter_item in filters:
        field = filter_item["field"]
        operator = filter_item["operator"]
        value = filter_item["value"]

        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Invalid field: {field}")

        if operator not in ALLOWED_OPERATORS:
            raise ValueError(f"Invalid operator: {operator}")

        if operator in {"IN", "NOT IN"}:

            if not isinstance(value, list):
                raise ValueError(
                    f"{operator} requires a list"
                )

            if len(value) == 0:
                raise ValueError(
                    f"{operator} requires at least one value"
                )

            placeholders = ", ".join(["?"] * len(value))

            conditions.append(
                f"{field} {operator} ({placeholders})"
            )

            values.extend(value)

        else:

            conditions.append(
                f"{field} {operator} ?"
            )

            values.append(value)

    if not conditions:
        results = connection.execute("""
            SELECT *
            FROM samples
        """).fetchall()

        connection.close()

        return results

    where_clause = " AND ".join(conditions)

    query = f"""
        SELECT *
        FROM samples
        WHERE {where_clause}
    """

    results = connection.execute(
        query,
        values
    ).fetchall()

    connection.close()

    return results