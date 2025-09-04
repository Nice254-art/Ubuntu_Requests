import requests
import os
import hashlib
from urllib.parse import urlparse

def fetch_image(url, download_dir="Fetched_Images", known_hashes=set()):
    try:
        # Create directory if it doesn't exist
        os.makedirs(download_dir, exist_ok=True)

        # Fetch the image
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Extract filename
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_image.jpg"

        # Generate file path
        filepath = os.path.join(download_dir, filename)

        # Prevent duplicates using file hash
        file_hash = hashlib.md5(response.content).hexdigest()
        if file_hash in known_hashes:
            print(f"⚠ Duplicate skipped: {filename}")
            return known_hashes
        known_hashes.add(file_hash)

        # Save only if content-type is image
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Skipped (Not an image): {url}")
            return known_hashes

        # Save the image
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")

    return known_hashes


def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Ask user for multiple URLs
    urls = input("Enter image URLs (comma separated): ").split(",")

    known_hashes = set()
    for url in urls:
        url = url.strip()
        if url:
            known_hashes = fetch_image(url, known_hashes=known_hashes)

    print("\nConnection strengthened. Community enriched.")


if __name__ == "__main__":
    main()
