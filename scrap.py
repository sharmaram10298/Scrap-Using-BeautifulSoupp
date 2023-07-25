from bs4 import BeautifulSoup
from selenium import webdriver
import csv

try:
    # Using Selenium to get the page source
    driver = webdriver.Chrome()  # Make sure chromedriver is in the same directory or provide its path
    driver.get('http://apma.in/members/index.php')
    source = driver.page_source

    # Parsing with BeautifulSoup
    soup = BeautifulSoup(source, 'html.parser')
    
    # Check if tbody exists
    tbody = soup.find('tbody')
    if tbody:
        # Find all <th> elements for headings
        headings = []
        th_elements = tbody.find('tr').find_all('th')
        headings = [th.get_text(strip=True) for th in th_elements]
        headings.extend(["Links"])  # Add column heading for the Links

        # Find all <tr> elements for data rows
        rows = tbody.find_all('tr')

        # Collect the data in a list of lists
        data = []
        for row in rows:
            cells = row.find_all('td')
            row_data = [cell.get_text(strip=True) for cell in cells]

            # Find all <a> tags and extract data from the href attribute
            links = ', '.join([a['href'] for a in row.find_all('a')])
            row_data.append(links)

            data.append(row_data)

        # Save data to a CSV file
        with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(headings)  # Write the headings as the first row
            csv_writer.writerows(data)

        print("Scraped data saved to scraped_data.csv")

    else:
        print("tbody element not found on the page.")

    driver.quit()  # Close the browser after scraping

except Exception as e:
    print(e)


