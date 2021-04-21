'''A common cause of medical bills occurs when a long series of bloodtests are ordered by a doctor, and the list happens to include tests that are not covered by insurance.  This information is difficult and time-consuming to look up because the patient is given the tests as a list of test names, however, insurance information is parsed using CPT codes associated to each test.'''

'''This script uses Selenium to automate the process of fetching the relevant Aetna insurance documents, given a user-inputted list of test names.  Future implementation will also take as input a list of medical conditions and will parse the medical bulletins to check whether a test is covered.  Note that the only insurance documents currently supported are those belonging to Aetna.'''

'''Usage: need Selenium, Firefox, and geckodriver installed.  Run "python aetna.py".  Enter all bloodtest names, separated by commas.  Returns a list of the medical bulletins that mention the bloodtest names.'''

from selenium import webdriver

#Get CPT codes
def getcpt(tests):
  '''Input: a list of lab test names, separated by commas.  Output: a list of 
     the corresponding CPT codes.'''
  cptcodes = []

  #Set up browser
  browser = webdriver.Firefox()
  browser.implicitly_wait(10) #Pause after visiting a new page to load all elements

  #Get the CPT code for each test
  for i in range(len(tests)):
    browser.get(f"https://testdirectory.questdiagnostics.com/test/results?q={tests[i]}")    #Quest search results for test name
    test = browser.find_element_by_xpath(\
      "//qd-results-card/*[1]")    #First search hit
    testcode = test.get_attribute("id")[6:]     #Test code of first hit
    browser.get(f"https://testdirectory.questdiagnostics.com/test/test-detail/{testcode}/?cc=MASTER")     #First hit's  webpage
    cptelement = browser.find_element_by_xpath("//div[@class='qd-header__codes padding-bottom-10']/div[2]")     #CPT code
    cptcodes.append(cptelement.text)
  
  browser.close()

  return cptcodes

#Get Aetna webpages
def getbulletins(cptcodes):
  '''Input: A list of CPT codes.  Output: hrefs of the Aetna Medical Bulletins
     mentioning these CPT codes'''
  links = [[] for i in range(len(cptcodes))]

  #Set up browser
  browser = webdriver.Firefox()
  browser.implicitly_wait(10) #Pause after visiting a new page to load all elements
  
  #Get Aetna Medical Policy Bulletin search results for all CPT codes.
  for i in range(len(cptcodes)):
    browser.get(f"https://www.aetna.com/health-care-professionals/clinical-policy-bulletins/medical-clinical-policy-bulletins/medical-clinical-policy-bulletins-search-results.html?query={cptcodes[i]}&cat=CPBs#")

    #Append the links for all Aetna search results of cptcodes[i] to links[i]
    for element in browser.find_elements_by_xpath("//a[contains(@href,"
      " '/cpb/medical/data/')]"):
      link = element.get_attribute("href")
      if link not in links[i]:
        links[i].append(link)

  browser.close()

  return links

#TO DO: implement
#Parse pages
def parse_bulletin(link, cptcode):
  '''Input: a CPT code and a page of Aetna Medical Policy Bulletin mentioning
     that code.  Returns:
     Not covered -- if selection criteria not met.
     A list of selection criteria if covered.'''
 
  #Set up browser
  browser = webdriver.Firefox()
  browser.implicitly_wait(10)

  browser.get(link)
  cpt_instance = browser.find_element_by_xpath("//*[contains(text(),"
    " cptcode)]")


#Output
if __name__ == "__main__":
  tests = input("Enter names of lab tests, separated by commas\n")
  tests = tests.split(',')
  cptcodes = getcpt(tests)
  bulletins = getbulletins(cptcodes)
  print(bulletins)

  #link = "http://www.aetna.com/cpb/medical/data/900_999/0925.html"
  #cptcode = "85048"
  #parse_bulletin(link, cptcode)
