from selenium import webdriver
from Driver import Driver
import time

class NavigatePages:

  def __init__(self, tests, driver):
    self.driver = driver
    self.tests = tests
    self.cptcodes = []
    self.links = [[]]

  #Get CPT codes
  def getcpt(self):
    '''Input: a list of lab test names, separated by commas.  Output: a list of
    the corresponding CPT codes.'''
    cptcodes = []

    for i in range(len(self.tests)):
      self.driver.get(f"https://testdirectory.questdiagnostics.com/test/results?q={self.tests[i]}")
      test = self.driver.find_element_by_xpath("//qd-results-card/*[1]")
      testcode = test.get_attribute("id")[6:]
      self.driver.get(f"https://testdirectory.questdiagnostics.com/test/test-detail/{testcode}/?cc=MASTER")
      cptelement = self.driver.find_element_by_xpath("//div[@class='qd-header__codes padding-bottom-10']/div[2]")
      cptcodes.append(cptelement.text)
      
    self.cptcodes = cptcodes

    return cptcodes

  #Get Aetna webpages
  def getbulletins(self):
    '''Input: A list of CPT codes.  Output: hrefs of the Aetna Medical Bulletins
     mentioning these CPT codes'''
    links = [[] for i in range(len(self.tests))]

    for i, code in enumerate(self.cptcodes):
      self.driver.get(f"https://www.aetna.com/health-care-professionals/clinical-policy-bulletins/medical-clinical-policy-bulletins/medical-clinical-policy-bulletins-search-results.html?query={code}&cat=CPBs#")
      time.sleep(5)
      for element in self.driver.find_elements_by_xpath("//a[contains(@href,"
        " '/cpb/medical/data/')]"):
        link = element.get_attribute("href")
        if link not in links[i]:
          links[i].append(link)
        
    self.links = links

    return links
