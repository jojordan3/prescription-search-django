# prescription-search-django
Simple Django-based web app to search for a medication by zip code or by Pharmacy Benefits Manager (PBM).

See the app at www.pharmasee.site

### While the app itself is simple, the data definitely was not.

This story begins with 15 csv files, together holding more than 2.5 GB of data representing over 4.4 million pharmacy prescription claims. Each csv file was somewhat standardized internally, but accross files there was little to no standardization. Quirks and typos originally made this data excessively difficult to use effectively.

This originally began as a group capstone project for Lambda School's only Artificial Intelligence/Machine Learning/Data Science cohort. The permanent app at www.pharmasee.site was deployed through Heroku in October 2018. All group contributions are displayed in notebook form via html on the site's homepage. Since then, I have picked up this project once again to take a second shot at actually getting the data clean. 

In our original deployment, we threw out any claim that had an empty `PharmacyZip` field, and when someone searched by zip code and medication name, it was not uncommon for the same pharmacy to show up in the results twice--for reasons as small as a single character differing in the address or name and as big as several fields with entirely wrong or missing information.

Using many methods and tools, exhibited in the `claims_data_handling` folder, I was able to reduce the occurrence of this inaccuracy while also greatly increasing the total number of claims contained in the database.

The `local_deploy` folder shows a little more specifically how I was able to accomplish this higher efficiency as well as better speed efficiency by organizing the data more efficiently. The `claims_data_handling` folder also shows the pipelining used to take in new claims once a sufficiently large database could be used for comparison.
