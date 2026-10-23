"""'Not enough evidence' rule: don't guess when the research isn't there."""

MIN_SIMILARITY = 0.80   # chosen from measurements: in-scope 0.858+, out-of-scope 0.767 and below

NOT_ENOUGH = ("The research database does not contain enough relevant evidence to answer this question. "
              "TrustMed only covers published breast cancer research.")

WEAK_WARNING = ("⚠️ This answer is based only on weak evidence (observational studies or narrative reviews). "
                "Treat it with caution.")


def check_evidence(chunks):
    """Return (enough_evidence, warnings)."""
    if not chunks or max(c["score"] for c in chunks) < MIN_SIMILARITY:
        return False, []
    if all(c["evidence_level"] == "weak" for c in chunks):
        return True, [WEAK_WARNING]
    return True, []