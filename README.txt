This is version 0.2 of a Python implementation of the Flesch Reading
Ease score.

There's no install documentation yet.  Read the source to work out how
it goes.

The 'worddb' module, which contains syllable counts, was built from
the 'rhyme' word lookup table, by reading the whole thing into a
regular dict, cutthin the stored values down to just the syllable
count, and serializing the whole repr() out to a worddb.py file,
prepended with "worddb = ". (Thanks for Micah Dubinko for this)

To rebuild from the 'rhyme' db, you will need to grab a copy from
http://rhyme.sourceforge.net/ and create a gdbm file for your
platform.  

Seb Bacon
<seb.bacon@gmail.com>
March 29, 2005
