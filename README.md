robot-profiler
==============

A Profiler for the Robot Framework.

Overview
--------
The Robot Profiler analysis the output.xml file generated
during test runs by the Robot Framework. It calculates
the overall runtime, the average runtime, and the number
of calls on a "per keyword" level. The calculated data
are written to a file for later use with a spreadsheet.

Pre-requisites
--------------
* Python 2.x

Installation
------------
Copy the file `robot_profiler.py` into the module search path of your
python installation.

Sorry, but no easy_setup or pip support at this time...

Usage
-----
```
usage: robot_profiler.py [-h] [-e ENCODING] [-s SEPARATOR] [-l LOCALE]
                         input_file_name [output_file_name]
```
```
positional arguments:
  input_file_name       The output.xml file to read from.
  output_file_name      The file to write the profiler data to.
```
```
optional arguments:
  -h, --help            show this help message and exit
  -e ENCODING, --encoding ENCODING
                        Encoding for output file.
  -s SEPARATOR, --separator SEPARATOR
                        Separator used in output file.
  -l LOCALE, --locale LOCALE
                        Locale used for number formatting.
```
If no `output_file_name` is given the name (and path) of the input file name is taken with
`.csv` as the new extension.

Parameters `-e`, `-s`, and `-l` are optional. They can be used to set the file encoding,
the field separator and the localization of the number format. The default values for these parameters
are chosen as sensible as possible and create a csv file that can be opened using Excel: it
uses cp1252 as encoding (Windows standard), and semicolon as field separator. If you need a
TSV file (tab separated values) you can use `-s \t`. The localization option uses no explicit
default value - it uses the platform's default locale. Please note that valid values for `-l`
might be platform depending. E.g. a german locale is `de_DE` on Linux but `German` on Windows...
