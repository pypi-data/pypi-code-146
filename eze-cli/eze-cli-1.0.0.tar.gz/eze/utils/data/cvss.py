"""
Tools for parsing and dealing with CVSS:3.1 and CVSS:3.0 data feeds and scores
https://www.first.org/cvss/v3.1/specification-document
https://www.first.org/cvss/v3.0/specification-document

"""

from math import floor


def _roundup(score):
    int_score = round(score * 100000)
    if (int_score % 10000) == 0:
        return int_score / 100000.0
    else:
        return (floor(int_score / 10000) + 1) / 10.0


def _get_cia_score(score_letter):
    """Returns the score for Confidentiality, Integrity and Availability"""
    return {
        "H": 0.56,  # high
        "L": 0.22,  # low
        "N": 0,  # none
    }[score_letter]


def _get_impact_score(score_letter, iss_value):
    """Returns the score for Impact"""

    if score_letter == "U":
        return 6.42 * iss_value
    return 7.52 * (iss_value - 0.029) - 3.25 * ((iss_value - 0.02) ** 15)


def _get_attack_vector_score(score_letter):
    """Returns the score for for Attack Vector"""
    return {
        "N": 0.85,  # network
        "A": 0.62,  # adjacent
        "L": 0.55,  # local
        "P": 0.2,  # physical
    }[score_letter]


def _get_attack_complexity_score(score_letter):
    """Returns the score for for Attack Complexity"""
    return {
        "H": 0.44,  # high
        "L": 0.77,  # low
    }[score_letter]


def _get_privileges_req_score(score_letter, scope="U"):
    """Returns the score for for Privileges Required"""

    if scope == "C":
        return {
            "H": 0.5,  # high
            "L": 0.68,  # low
            "N": 0.85,  # none
        }[score_letter]

    return {
        "H": 0.27,  # high
        "L": 0.62,  # low
        "N": 0.85,  # none
    }[score_letter]


def _get_user_interaction_score(score_letter):
    """Returns the score for for User Interaction"""
    return {
        "R": 0.62,  # required
        "N": 0.85,  # none
    }[score_letter]


def severity_score_v3_1(vector: str):
    """Calculates the CVSS score given a severity vector. Ex CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H"""

    vector_values = dict([x.split(":") for x in vector.split("/")])

    # cia
    confidentiality = _get_cia_score(vector_values["C"])
    integrity = _get_cia_score(vector_values["I"])
    availability = _get_cia_score(vector_values["A"])

    # others
    attack_vector = _get_attack_vector_score(vector_values["AV"])
    attack_complexity = _get_attack_complexity_score(vector_values["AC"])
    privileges_req = _get_privileges_req_score(
        vector_values["PR"],
        vector_values["S"],
    )
    user_interaction = _get_user_interaction_score(vector_values["UI"])

    iss = 1 - ((1 - confidentiality) * (1 - integrity) * (1 - availability))
    impact = _get_impact_score(vector_values["S"], iss)
    exploitability = 8.22 * attack_vector * attack_complexity * privileges_req * user_interaction
    if impact <= 0:
        return 0
    else:
        if vector_values["S"] == "U":
            return _roundup(min(impact + exploitability, 10))
        return _roundup(min(1.08 * (impact + exploitability), 10))
