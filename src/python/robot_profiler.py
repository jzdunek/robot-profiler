__author__ = 'jan.zdunek'
# Copyright 2013 Jan Zdunek
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import codecs
import locale
import os.path

import xml.etree.cElementTree as cElementTree

from datetime import datetime
from datetime import timedelta


def convert_time(t):
    seconds = t.seconds
    seconds += (t.microseconds / 1000000.0)
    return seconds


def get_keyword(kw_tag):
    name = kw_tag.attrib.get('name')
    name = name[name.rfind('=')+1:].strip()
    return name


def calc_elapsed_time(status_tag):
    endtime = datetime.strptime(status_tag.attrib.get('endtime')+'000',
                                  '%Y%m%d %H:%M:%S.%f')
    starttime = datetime.strptime(status_tag.attrib.get('starttime')+'000',
                                    '%Y%m%d %H:%M:%S.%f')
    return endtime - starttime


def analyse_output_xml(path_to_output_xml):
    keywords = {}
    tree = cElementTree.parse(path_to_output_xml)
    root = tree.getroot()
    for kw in root.findall(".//kw[@type='kw']"):
        name = get_keyword(kw)
        status = kw.find('./status')
        duration = calc_elapsed_time(status)
        if name in keywords:
            durations = keywords[name]
            durations.append(duration)
        else:
            durations = [duration]
        keywords.update({name: durations})
    return keywords


def profile(infile_name, outfile_name, file_encoding, separator_character, loc):
    keywords = analyse_output_xml(infile_name)

    default_locale = locale.getlocale()
    locale.setlocale(locale.LC_ALL, loc)
    output_file = codecs.open(outfile_name, 'w', encoding=file_encoding)
    output_file.write(
        'Keyword' + separator_character +
        'No of Occurrences' + separator_character +
        'Time Sum' + separator_character +
        'Time Avg' + '\n'
    )
    for kw in keywords:
        durations = keywords[kw]
        duration = timedelta()
        for d in durations:
            duration += d
        avg_duration = duration / len(durations)
        output_file.write(
            kw + separator_character +
            str(len(durations)) + separator_character +
            '{:n}'.format(convert_time(duration)) + separator_character +
            '{:n}'.format(convert_time(avg_duration)) + '\n'
        )
    output_file.close()
    locale.setlocale(locale.LC_ALL, default_locale)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file_name',
                        help='The output.xml file to read from.')
    parser.add_argument('output_file_name', nargs='?',
                        help='The file to write the profiler data to.')
    parser.add_argument('-e',
                        '--encoding',
                        default='cp1252',
                        help='Encoding for output file.')
    parser.add_argument('-s',
                        '--separator',
                        default=';',
                        help='Separator used in output file.')
    parser.add_argument('-l',
                        '--locale',
                        default='',
                        help="Locale used for number formatting.")
    args = parser.parse_args()
    output_file_name = args.output_file_name
    if output_file_name is None:
        output_file_name = os.path.splitext(args.input_file_name)[0] + '.csv'
    separator = args.separator
    if separator == '\\t':
        separator = '\t'
    profile(args.input_file_name,
            output_file_name,
            args.encoding,
            separator,
            args.locale)
