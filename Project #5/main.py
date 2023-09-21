from bs4 import BeautifulSoup
import requests
import csv

district_details = []

def get_info(url):
    try:
        print(i)
        results = requests.get(url)
        results.raise_for_status()
        soup = BeautifulSoup(results.text, "html.parser")
        
        district_info = soup.find("table", border="0", cellspacing="5", cellpadding="0").find_all("font")
        
        district_name = district_info[1].text.strip()
        nces_district_id = district_info[4].text.strip()
        state_district_id = district_info[6].text.strip()
        mailing_address = district_info[8].text.strip()
        physical_address = district_info[10].text.strip()
        phone = district_info[12].text.strip()
        district_type = district_info[14].text.strip()
        status = district_info[16].text.strip()
        total_schools = district_info[18].text.strip()
        website= district_info[38].text.strip() if district_info[38] else "-"
        district_details.append({
            "District Name": district_name,
            "NCES District ID": nces_district_id,
            "State District ID": state_district_id,
            "Mailing Address": mailing_address,
            "Physical Address": physical_address,
            "Phone": phone,
            "Type": district_type,
            "Status": status,
            "Total Schools": total_schools,
            "Website": website
        })

    except Exception as e:
        print(f"An error occurred while extracting data from {url}: {e}")


for i in range(1, 143):  # Adjust the loop range for multiple pages
    url = f"https://nces.ed.gov/ccd/districtsearch/district_list.asp?Search=1&details=1&State=06&DistrictType=1&DistrictType=2&DistrictType=3&DistrictType=4&DistrictType=5&DistrictType=6&DistrictType=7&DistrictType=8&DistrictType=9&NumOfStudentsRange=more&NumOfSchoolsRange=more&DistrictPageNum={i}"
    result = requests.get(url)
    result.raise_for_status()
    soup = BeautifulSoup(result.text, "html.parser")
    table = soup.find_all("table")[3]
    rows = table.find_all("tr")
    for row in rows[1:]:  # Skip the first row since it's the header
        cells = row.find_all("td")
        link_cell = cells[0]  # Assuming the link cell is the first column
        link = link_cell.find("a")
        if link:
            a = "https://nces.ed.gov/ccd/districtsearch/" + link["href"]
            get_info(a)

csv_filename = "districts.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["District Name", "NCES District ID", "State District ID", "Mailing Address","Physical Address", "Phone", "Type", "Status", "Total Schools","Website"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(district_details)

print(f"Scraped data saved to {csv_filename}")
