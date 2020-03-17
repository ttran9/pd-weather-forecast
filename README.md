# Live Demo
- I plan to upload this to either Linode, Heroku, or possibly AWS. I have had previous experience deploying onto both Linode and Heroku so at the time of initially creating this web application I may choose to upload to AWS as I have not done so.

# Overview
- This project will allow me to practice Python, Django, and Selenium by creating an application which uses the Darksky API (to get weather forecasts from a latitude and longitude pair obtained from an entered user address). The user address is passed into the Google Geocoding API which will ultimately return the latitude and longitude as well as the entered address which will be formatted. 
    
# TODO:
- Create models to hold the data such as: Daily and Hourly forecasts and searches.
- Create views to respond to when user requests a page.
- Create url mappings for a variety of routes.
- Create tests (view below for more information)

# Tests:
    - Pytests:
        - Make a sample Darksky API call
        - Make a sample Google Geocoding API call.
        - Make a Geocoding API call and using the result of that to make a Darksky API call which should result in having a list of Daily and Hourly forecasts.

    - Selenium Based Tests:
        - Make a search while not logged in.
        - Make a search while logged in. 
        - When logged in go to the page with prior searches.
            - Pick a search to look at.
                - View the daily and hourly forecasts.
        - When logged in go to the page with prior searches (but user has not made any).