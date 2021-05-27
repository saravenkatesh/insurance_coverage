# insurance_coverage

Automates the arduous process of checking whether lab testing is covered by Aetna's policies. 

Uses Selenium to navigate

lab test name -> CPT code -> clinical policy bulletins mentioning CPT code

and then scrape relevant clinical policy bulletins for information about CPT code coverage.

Needs Firefox, Selenium, and geckodriver to run.
