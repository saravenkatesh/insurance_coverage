from selenium import webdriver
from Driver import Driver

class ParsePages:

  def __init__(self, links, driver, cptcodes, tests):
    self.driver = driver
    self.links = links
    self.covered = [0] * len(tests)
    self.cptcodes = cptcodes
    self.tests = tests
    
  def criteriaMet(self):
    for i, case in enumerate(self.links):
      for link in case:
        bool = False
        self.driver.get(link)
        table = self.driver.find_element_by_xpath("//table[@id='complexTable']")
        rows = table.find_elements_by_xpath("//tr")
        for row in rows:
          text = row.text.split()
          if text[-7:] == ['codes', 'covered', 'if', 'selection', 'criteria', 'are', 'met:']:
            bool = True
          elif row.get_attribute("colspan") == "2":
            bool = False
          elif text[0] == self.cptcodes[i].strip():
            if self.covered[i] == 0:
              self.covered[i] = bool
            elif self.covered[i] == (not bool):
              self.covered[i] = 1
            break
            
  def printCoverage(self):
    for item in zip(self.tests, self.covered):
      print('{:<10s}{:>4s}'.format(item[0], self.output(item[1])))
      
  def output(self, input):
    if input == True:
      return "Probably"
    elif input == False:
      return "Probably Not"
    elif input == 0:
      return "No information"
    else:
      return "Depends"
            
