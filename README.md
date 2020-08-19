# postcard-tag-data

Extracts Zooniverse postcard data and outputs tsv.

## Input Format

The data arrived in the form of a spreadsheet, with "val1" in one column, "val2" in another, and id in a third. 
I concatenated the values in excel to json format (something like =concatenate("[",a2,",",b2,", ""id"":", c2, "]"))
then brought the results into a code editor and used a prettify script on it.

## Unicode Characters

In this script's original run, there were some non-ascii characters which I manually replaced.  
If there's a non-ascii error, search the dataset for [^\x00-\x7f] and manually fix;
If there are more than a handful, we can add a substitution to the script.
