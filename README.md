# To prepare data for Tempr:
- two files need to be created
- see code/processing/_PHET_a2_low_log.txt for an example
- all users for one group will be in one file
- the first line of a user file should be ========================================
- each proceeding line is one user action, in order


# To use Tempr:
- create two files as specified above, one for each group of users
- edit the "USER ENTERED SPECIFICATIONS" section of code/processing/parse_get_temporal_freq.py
- you will need to specify the name of each of the two files above, a name for the data, and a two letter abbreviation for each group
- within the code/processing directory, run parse_get_temporal_freq.py with python 2
- open index.html in firefox


Video for an older version of the project can be found at: https://www.youtube.com/watch?v=kkeWC6rLBe4
