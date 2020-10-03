import selenium
from selenium.webdriver.support.ui import WebDriverWait, Select

browser = selenium.webdriver.Firefox()

browser.get("https://elections.sos.ga.gov/Elections/countyregistrars.do")

county_dropdown = Select(browser.find_element_by_id("idTown"))

registrars = {}

for i in range(0, len(county_dropdown.options)):
    county_dropdown = Select(browser.find_element_by_id("idTown"))
    county_dropdown.select_by_index(i)
    county_name = county_dropdown.first_selected_option.text
    # Since we will be going back and forth on the page need to refresh this each time
    select_button = browser.find_element_by_name("SubmitCounty")
    select_button.click()
    back_button = browser.find_element_by_name("SubmitBack")
    # The first element tbody is the "elections division" header
    registrar_data = browser.find_elements_by_tag_name("tbody")[1]

    # Strip extraneous whitespace from the text, then remove the first line "COUNTY BOARD OF REGISTRARS OFFICES"
    registrars[str.capitalize(county_name)] = "\n".join(registrar_data.text.strip().splitlines()[1:])

    back_button.click()

with open("georgia_registrars.txt", 'w') as f:
    for county in sorted(registrars):
        f.write(county + " County\n")
        f.write(registrars[county] + "\n")
        f.write("\n")
