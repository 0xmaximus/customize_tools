#!/usr/bin/env python3
import argparse
import uuid
import csv
import os
import shutil
import hmac
import hashlib

def generate_token(email, use_hmac=False, secret_key=b'secret'):
    """
    Generate a unique token for each email.
    If HMAC is enabled, use HMAC(email, secret_key) with SHA256 and take first 16 hex chars.
    Otherwise, generate a random UUID.
    """
    if use_hmac:
        return hmac.new(secret_key, email.encode(), hashlib.sha256).hexdigest()[:16]
    else:
        return uuid.uuid4().hex

def main():
    p = argparse.ArgumentParser(description="Generate unique tracking-pixels per email")
    p.add_argument("-email",   required=True, help="Path to emails.txt")
    p.add_argument("-domain",  required=True, help="Base URL (with trailing slash)")
    p.add_argument("-file",    required=True, help="Source image file (e.g. pixel.png)")
    p.add_argument("-out",     required=True, help="Output folder")
    p.add_argument("--hmac",   action="store_true", help="Use HMAC(email) instead of UUID")
    p.add_argument("--secret", default="secret", help="Secret key for HMAC")
    args = p.parse_args()

    # Prepare output folder
    os.makedirs(args.out, exist_ok=True)
    mapping_path = os.path.join(args.out, "mapping.csv")

    # Ensure domain ends with /
    base = args.domain if args.domain.endswith("/") else args.domain + "/"
    _, ext = os.path.splitext(os.path.basename(args.file))

    with open(args.email, encoding="utf-8") as fin, \
         open(mapping_path, "w", newline="", encoding="utf-8") as fout:

        writer = csv.writer(fout)
        writer.writerow(["email", "pixel_filename", "pixel_url"])

        for line in fin:
            email = line.strip()
            if not email:
                continue

            # Generate token for this email
            token = generate_token(email, use_hmac=args.hmac, secret_key=args.secret.encode())

            # Use only the token as filename
            new_filename = f"{token}{ext}"
            src = args.file
            dst = os.path.join(args.out, new_filename)
            shutil.copy2(src, dst)

            # Build tracking URL
            url = f"{base}{new_filename}"

            # Write to CSV
            writer.writerow([email, new_filename, url])

    print(f"✅ Output folder: {args.out}")
    print(f"✅ Mapping CSV: {mapping_path}")

if __name__ == "__main__":
    main()

# Usage: python3 code.py -email email.txt -domain "https://site.com/image/" -file "pixel.png" -out pixel/
