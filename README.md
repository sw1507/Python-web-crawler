# Python-web-crawler

This python program is able to do the following:
    1) For each inspection for each facility on a single page of results from the Napa county health
       department website (http://ca.healthinspections.us/napa/search.cfm?searchType=letter&srchLetter=A), scrape the following      information:
       - Facility name
       - Address (just street info, not city, state, or zip)
       - City
       - State
       - Zipcode
       - Inspection date
       - Inspection type
       - For each out-of-compliance violation type, scrape the violation type number and corresponding description.
         For example, an inspection might contain violation type numbers 6 and 7, and descriptions
         "Adequate handwashing facilities supplied & accessible" and "Proper hot and cold holding temperatures"
         
    2) Place this information in a database of some sort. You can use whatever you want; sqlite, postgres, mongodb, etc.
       Organize the data in a fashion which seems the most logical and useful to you. Include in your result the
       necessary instructions to set up this database, such as create table statements.
       
    3) Fetch this information from the database, and print it to the console in some fashion which clearly
       and easily displays the data you scraped.
