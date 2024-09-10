import requests
from bs4 import BeautifulSoup


def fetch_xsd_schemas():
    """
    Fetch schema URLs based on directory names from the DDEX ERN directory.
    """
    base_url = "https://service.ddex.net/xml/ern/"
    try:
        response = requests.get(base_url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract directory links (which are versions)
        xsd_urls = []
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and href.endswith("/"):  # Check if it's a directory
                # Construct the schema URL for this version's directory
                version = href.strip("/")  # Remove trailing slash
                xsd_url = f"{base_url}{version}/release-notification.xsd"

                # Create a display name like "ERN 382" from the directory name
                display_name = f"ERN {version}"
                if "xml" not in version:
                    xsd_urls.append((xsd_url, display_name))

        return xsd_urls

    except requests.RequestException as e:
        print(f"Error fetching XSD schemas: {e}")
        return []
