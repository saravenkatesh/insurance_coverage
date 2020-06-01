from selenium import webdriver

class Driver:
  def __init__(self):
    self.driver = webdriver.Firefox()
    self.driver.implicitly_wait(15)
    
  def close(self):
    self.driver.close()
