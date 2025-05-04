import hmac
import hashlib

def verify_signature(secret: str, payload: bytes, signature_header: str) -> bool:
    """
    Verify HMAC SHA256 signature.
    signature_header: expected format "sha256=hex_digest"
    """
    if not secret or not signature_header:
        return False
    try:
        sig_prefix = "sha256="
        if not signature_header.startswith(sig_prefix):
            return False
        signature = signature_header[len(sig_prefix):]
        mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
        expected_sig = mac.hexdigest()
<<<<<<< HEAD
        return hmac.compare_digest(expected_sig.lower(), signature.lower())
=======
        return hmac.compare_digest(expected_sig, signature)
>>>>>>> 65cd0d2 (Initial Commit)
    except Exception:
        return False

def get_retry_delay(attempt_number: int):
    delays = [10, 30, 60, 300, 900]  # seconds
    if attempt_number <= len(delays):
        return delays[attempt_number - 1]
    return delays[-1]
