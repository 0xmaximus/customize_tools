#!/usr/bin/env python3
import argparse
import uuid
import csv
import os
import hmac
import hashlib

def generate_token(email, use_hmac=False, secret_key=b'secret'):
    if use_hmac:
        return hmac.new(secret_key, email.encode(), hashlib.sha256).hexdigest()[:16]
    else:
        return uuid.uuid4().hex

def main():
    p = argparse.ArgumentParser(description="Generate tracking-pixel URLs per email")
    p.add_argument("-email",   required=True, help="Path to emails.txt")
    p.add_argument("-domain",  required=True, help="Base URL (include trailing slash)")
    p.add_argument("-file",    required=True, help="Filename of your pixel (e.g. image.png)")
    p.add_argument("--hmac",   action="store_true", help="Use HMAC(email) instead of UUID")
    p.add_argument("--out",    default="mapping.csv", help="Output CSV filename")
    args = p.parse_args()

    # مطمئن می‌شویم دامین پایانش /
    base = args.domain if args.domain.endswith("/") else args.domain + "/"

    with open(args.email, encoding="utf-8") as fin, \
         open(args.out, "w", newline="", encoding="utf-8") as fout:

        writer = csv.writer(fout)
        writer.writerow(["email", "pixel_url"])

        for line in fin:
            email = line.strip()
            if not email: continue
            token = generate_token(email, use_hmac=args.hmac)
            # URL یکتا برای هر ایمیل
            url = f"{base}{os.path.splitext(args.file)[0]}-{token}{os.path.splitext(args.file)[1]}"
            writer.writerow([email, url])

    print(f"✅ Mapping generated in {args.out}")

if __name__ == "__main__":
    main()


## Sample: python pixel.py -email email.txt -domain "http://162.223.89.77:8080/" -file "pixel.png"
