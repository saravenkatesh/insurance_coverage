from selenium import webdriver
from Driver import Driver
from NavigatePages import NavigatePages
from ParsePages import ParsePages

if __name__ == "__main__":
  tests = input("Enter names of lab tests, separated by commas\n")
  tests = tests.split(',')
  
  driver = Driver()
  
  Navigate = NavigatePages(tests, driver.driver)
  cptcodes = Navigate.getcpt()
  links = Navigate.getbulletins()

  Parser = ParsePages(links, driver.driver, cptcodes, tests)
  
  Parser.criteriaMet()
  Parser.printCoverage()
  
  driver.close()
