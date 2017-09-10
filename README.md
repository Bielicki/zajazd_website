# zajazd_website
Django powered website for hotel and restaurant with reservation system.

***
TODO:
- WRITE TESTS !!!
- Block rooms from picking for specific date when picked for reservation to avoid errors when 2 or more clients make reservation for the same date
- Use django-cleanup or similar third party app to handle old files more efficently
- Make Website Views for logged user with easy content editing
- Add Catering app to check pricing for specific Catering services
- Separate forms and views usage of request
    - I made special class FormProcessor that processes forms(stores data in sessino etc.)
    still need to :
        - Add one more step to confirm all reservation data 
        - consider using rest api and JS for this one


- Create more all-around form processing code (or switch to form wizard)