import requests
from bs4 import BeautifulSoup
from config import HEADERS

def fetch_html(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.text


def extract_school_data(html, school_code):

    soup = BeautifulSoup(html, "lxml")

    tables = soup.find_all("table")

    extracted = []

    for table in tables:

        rows = table.find_all("tr")

        # skip small tables
        if len(rows) < 5:
            continue

        # get first row headers
        first_row = rows[0]

        headers = [x.text.strip().upper() for x in first_row.find_all(["td", "th"])]

        # find correct table
        if "CNO" in headers and "DETAILED SUBJECTS" in headers:

            # process student rows
            for row in rows[1:]:

                cols = [c.text.strip() for c in row.find_all("td")]

                if len(cols) < 5:
                    continue

                extracted.append({
                    "school_code": school_code,
                    "cno": cols[0],
                    "sex": cols[1],
                    "aggt": cols[2],
                    "div": cols[3],
                    "detailed_subjects": cols[4]
                })

    return extracted