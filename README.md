# prescription-search-django
Simple Django-based web app to search for a medication by zip code or by Pharmacy Benefits Manager (PBM).

see the app at www.pharmasee.site

While the app itself is simple, the data definitely was not.

This story begins with 15 csv files, together holding more than 2.5 GB of data representing around 4 million pharmacy prescription claims. Each csv file was somewhat standardized internally, but accross files there was little to no standardization. Quirks and typos originally made this data excessively difficult to use effectively.

The three major folders in this repository 