__author__ = 'jan.zdunek'

# Copyright 2015 Jan Zdunek
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tempfile
import os
import unittest
from datetime import timedelta

import robot

import robot_profiler


class RobotProfilerUnitTests(unittest.TestCase):
    @staticmethod
    def create_test_case_file(test_case_content):
        test_case_file_descriptor, test_case_filename = tempfile.mkstemp(suffix='.txt', text=True)
        os.write(test_case_file_descriptor, test_case_content)
        os.close(test_case_file_descriptor)
        assert isinstance(test_case_filename, str)
        return test_case_filename

    def assertTimedeltaAlmostEqual(self, first, second, msg=None, delta=timedelta(milliseconds=100)):
        if (type(first) is timedelta) and (type(second) is timedelta):
            if abs(second - first) < delta:
                return
            else:
                raise self.failureException('%s != %s within %s delta.' % (first, second, delta))
        else:
            raise self.failureException('Assertion only takes timedelta objects.')

    @staticmethod
    def run_and_analyse_robottest(testfilename):
        outputfile = tempfile.mkstemp(suffix='.xml')[1]
        robot.run(testfilename, report='NONE', log='NONE', output=outputfile)
        keywords = robot_profiler.analyse_output_xml([outputfile])
        return keywords

    @staticmethod
    def run_and_analyse_multiple_robot_tests(list_of_testfilename):
        list_of_output_xml_files = []
        for testfilename in list_of_testfilename:
            outputfile = tempfile.mkstemp(suffix='.xml')[1]
            robot.run(testfilename, report='NONE', log='NONE', output=outputfile)
            list_of_output_xml_files.append(outputfile)
        keywords = robot_profiler.analyse_output_xml(list_of_output_xml_files)
        return keywords

    def test_analyse_output_xml_1(self):
        test_case = """
*** Test Case ***
Test Case 1
    [Documentation]    Test case for the Robot Profiler: Keyword from the BuiltIn library in different spellings.
    ...                This checks that the profiler is able to read the status messages and to gather the timestamps
    ...                from the output xml file. The Robot Profiler relies on the behaviour of the Robot Framework
    ...                to log the keyword's name as taken from the library despite the spellings used in the test
    ...                files. This is checked as well.
    Sleep            1s
    Sleep            2s
    sleep            3s
    BuiltIn.Sleep    4s
        """
        test_case_file_name = self.create_test_case_file(test_case)
        keywords = self.run_and_analyse_robottest(test_case_file_name)

        self.assertEqual(1, len(keywords), 'Wrong number of keywords found.')
        self.assertIn('BuiltIn.Sleep', keywords)
        self.assertEqual(4, len(keywords['BuiltIn.Sleep']), 'Wrong number of durations found.')
        self.assertTimedeltaAlmostEqual(timedelta(seconds=1), keywords['BuiltIn.Sleep'][0])
        self.assertTimedeltaAlmostEqual(timedelta(seconds=2), keywords['BuiltIn.Sleep'][1])
        self.assertTimedeltaAlmostEqual(timedelta(seconds=3), keywords['BuiltIn.Sleep'][2])
        self.assertTimedeltaAlmostEqual(timedelta(seconds=4), keywords['BuiltIn.Sleep'][3])

    def test_analyse_output_xml_2(self):
        test_case = """
*** Test Case ***
Test Case 2
    [Documentation]    Test case for the Robot Profiler: Multiple keywords from the BuiltIn library.
    ...                This checks that the profiler is able to handle multiple keywords.
    Sleep    1s
    No Operation
        """
        test_case_file_name = self.create_test_case_file(test_case)
        keywords = self.run_and_analyse_robottest(test_case_file_name)

        self.assertEqual(2, len(keywords), 'Wrong number of keywords found.')
        self.assertIn('BuiltIn.Sleep', keywords)
        self.assertIn('BuiltIn.No Operation', keywords)

    def test_analyse_output_xml_3(self):
        test_case = """
*** Keyword ***
User Defined Keyword
    No Operation

*** Test Case ***
Test Case 3
    [Documentation]    Test case for the Robot Profiler: User Defined Keywords.
    ...                This test checks that the profiler is able to handle user defined keywords in different spellings.
    User Defined Keyword
    user defined keyword
    userdefinedkeyword
        """
        test_case_file_name = self.create_test_case_file(test_case)
        keywords = self.run_and_analyse_robottest(test_case_file_name)

        self.assertEqual(2, len(keywords), 'Wrong number of keywords found.')
        self.assertIn('BuiltIn.No Operation', keywords)
        self.assertIn('User Defined Keyword', keywords)
        self.assertEqual(3, len(keywords['User Defined Keyword']), 'Wrong number of durations found.')

    def test_analyse_output_xml_4(self):
        test_case = """
*** Keyword ***
User Defined Keyword
    No Operation

Another User Defined Keyword
    No Operation

*** Test Case ***
Test Case 4
    [Documentation]    Test case for the Robot Profiler: Multiple User Defined Keywords.
    ...                This test checks that the profiler is able to handle multiple user defined keywords.
    User Defined Keyword
    Another User Defined Keyword
        """
        test_case_file_name = self.create_test_case_file(test_case)
        keywords = self.run_and_analyse_robottest(test_case_file_name)

        self.assertEqual(3, len(keywords), 'Wrong number of keywords found.')
        self.assertIn('BuiltIn.No Operation', keywords)
        self.assertIn('User Defined Keyword', keywords)
        self.assertIn('Another User Defined Keyword', keywords)

    def test_analyse_output_xml_5(self):
        test_case = """
*** Settings ***
Documentation    Test Case for the Robot Profiler: Multiple Test Cases
...              Checks that the profiler is able to gather data from multiple test cases.

*** Test Case ***
Test Case 5 A
    Sleep    1s

Test Case 5 B
    Sleep    2s
        """
        test_case_file_name = self.create_test_case_file(test_case)
        keywords = self.run_and_analyse_robottest(test_case_file_name)

        self.assertEqual(1, len(keywords), 'Wrong number of keywords found.')
        self.assertIn('BuiltIn.Sleep', keywords)
        self.assertEqual(2, len(keywords['BuiltIn.Sleep']), 'Wrong number of durations found.')
        self.assertTimedeltaAlmostEqual(timedelta(seconds=1), keywords['BuiltIn.Sleep'][0])
        self.assertTimedeltaAlmostEqual(timedelta(seconds=2), keywords['BuiltIn.Sleep'][1])

    def test_analyse_output_xml_6(self):
        test_case = """
*** Settings ***
Documentation    Test Case for the Robot Profiler: Multiple Test Cases Files - File A
...              Checks that the profiler is able to gather data from multiple output xml files.

*** Test Case ***
Test Case 6 A
    Sleep    1s
        """
        test_case_file_name_6a = self.create_test_case_file(test_case)

        test_case = """
*** Settings ***
Documentation    Test Case for the Robot Profiler: Multiple Test Cases Files - File B
...              Checks that the profiler is able to gather data from multiple output xml files.

*** Test Case ***
Test Case 6 B
    Sleep    2s
        """
        test_case_file_name_6b = self.create_test_case_file(test_case)
        keywords = self.run_and_analyse_multiple_robot_tests([test_case_file_name_6a, test_case_file_name_6b])

        self.assertEqual(1, len(keywords), 'Wrong number of keywords found.')
        self.assertIn('BuiltIn.Sleep', keywords)
        self.assertEqual(2, len(keywords['BuiltIn.Sleep']), 'Wrong number of durations found.')
        self.assertTimedeltaAlmostEqual(timedelta(seconds=1), keywords['BuiltIn.Sleep'][0])
        self.assertTimedeltaAlmostEqual(timedelta(seconds=2), keywords['BuiltIn.Sleep'][1])

    def test_evaluate_durations(self):
        keyword_information = robot_profiler.evaluate_durations(
            {'BuiltIn.Sleep': [timedelta(seconds=1), timedelta(seconds=1)],
             'BuiltIn.No Operation': [timedelta(seconds=0)]})
        self.assertEqual(2, len(keyword_information), 'Wrong number of evaluated keywords.')
        self.assertIn('BuiltIn.Sleep', keyword_information)
        self.assertListEqual([2, timedelta(seconds=2), timedelta(seconds=1)], keyword_information['BuiltIn.Sleep'])
        self.assertIn('BuiltIn.No Operation', keyword_information)
        self.assertListEqual([1, timedelta(seconds=0), timedelta(seconds=0)],
                             keyword_information['BuiltIn.No Operation'])

    def test_create_output_line_1(self):
        line = robot_profiler.create_output_line("BuiltIn.Sleep", 2, timedelta(seconds=2), timedelta(seconds=1), ';')
        fields = line.split(';')
        self.assertEqual(4, len(fields))
        self.assertEqual('BuiltIn.Sleep', fields[0])
        self.assertEqual('2', fields[1])
        self.assertEqual('2', fields[2])
        self.assertEqual('1', fields[3])

    def test_create_output_line_2(self):
        line = robot_profiler.create_output_line("BuiltIn.Sleep", 2, timedelta(seconds=2, milliseconds=200),
                                                 timedelta(seconds=1, milliseconds=100), ';')
        fields = line.split(';')
        self.assertEqual(4, len(fields))
        self.assertEqual('BuiltIn.Sleep', fields[0])
        self.assertEqual('2', fields[1])
        self.assertEqual('2.2', fields[2])
        self.assertEqual('1.1', fields[3])

    def test_parse_file_name_list_1(self):
        file_name_list = ['output_1.xml', 'output_2.xml', 'output_3.xml']
        list_of_input_names, output_name = robot_profiler.parse_file_name_list(file_name_list)
        self.assertListEqual(file_name_list, list_of_input_names)
        self.assertEqual('output_1.csv', output_name)

    def test_parse_file_name_list_2(self):
        file_name_list = ['output_1.xml', 'output_2.xml', 'my_analysis.csv']
        list_of_input_names, output_name = robot_profiler.parse_file_name_list(file_name_list)
        self.assertListEqual(file_name_list[0:-1], list_of_input_names)
        self.assertEqual('my_analysis.csv', output_name)

    def test_parse_file_name_list_3(self):
        with self.assertRaises(AssertionError):
            robot_profiler.parse_file_name_list('output.xml')

    def test_parse_file_name_list_4(self):
        file_name_list = ['output.xml']
        list_of_input_names, output_name = robot_profiler.parse_file_name_list(file_name_list)
        self.assertListEqual(file_name_list, list_of_input_names)
        self.assertEqual('output.csv', output_name)


if __name__ == '__main__':
    unittest.main()
