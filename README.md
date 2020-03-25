# Live Demo
- I plan to upload this to either Linode, Heroku, or possibly AWS. I have had previous experience deploying onto both Linode and Heroku so at the time of initially creating this web application I may choose to upload to AWS as I have not done so.

# Overview
- This project will allow me to practice Python, Django, and Selenium by creating an application which uses the Darksky API (to get weather forecasts from a latitude and longitude pair obtained from an entered user address). The user address is passed into the Google Geocoding API which will ultimately return the latitude and longitude as well as the entered address which will be formatted. 
    
# TODO:
- Refactor code. While writing this I was more worried about functionality so there will definitely by areas with sloppy code and possibly inconsistent styling such as inconsistent variable naming and such.

# Tests:
    - Pytests:
        1) Make a sample Google Geocoding API call.
        2) Make a Geocoding API call and using the result of that to make a Darksky API call which should result in having a list of Daily and Hourly forecasts.

    - Selenium Based Tests:
        1) make the search
	        - as not logged in
	        - as logged in
        - once making the search just try to find the chart based on id
        - for both cases make sure you can view the daily forecasts and find the two charts based on id.
        - try to also click on the next and previous pagination buttons.
	
        2) try to click on the prior searches
            - do this only as logged in
            - click on the next and previous pagination buttons.