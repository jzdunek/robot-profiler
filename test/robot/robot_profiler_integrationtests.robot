*** Settings ***
Documentation    Testing the Robot Profiler as a integrated program.

Library    OperatingSystem
Library    String

Test Setup    Test Setup

*** Variables ***
${ROBOT TEST CASE}     ${TEMPDIR}${/}SimpleRobotTest.txt
${ROBOT OUTPUT}        ${TEMPDIR}${/}output.xml
${ROBOT OUTPUT TWO}    ${TEMPDIR}${/}output2.xml
${PROFILER OUTPUT}     ${TEMPDIR}${/}output.csv

*** Test Cases ***
Call Robot Profiler without arguments
    When calling Robot Profiler without any arguments
    Then the command should fail with an return code not equal to zero


Call Robot Profiler with help argument
    When calling Robot Profiler with help argument
    Then the command should succeed with a return code equal to zero


Call Robot Profiler with default values
    Given a Robot Framework output xml file has been created
    When calling Robot Profiler with default values and the output xml file as arguments
    Then the command should succeed with a return code equal to zero
    And a Robot Profiler output file output.csv should exist
    And the output.csv file should contain the expected data


Call Robot Profiler with non default encoding
    Given a Robot Framework output xml file has been created
    When calling Robot Profiler with utf-8 encoding and the output xml file as arguments
    Then the command should succeed with a return code equal to zero
    And a Robot Profiler output file output.csv should exist
    And the output.csv file should contain the expected data encoded utf-8


Call Robot Profiler with non default separator
    Given a Robot Framework output xml file has been created
    When calling Robot Profiler with colon as separator and the output xml file as arguments
    Then the command should succeed with a return code equal to zero
    And a Robot Profiler output file output.csv should exist
    And the output.csv file should contain the expected data colon separated


Call Robot Profiler with tab as separator
    Given a Robot Framework output xml file has been created
    When calling Robot Profiler with tab as separator and the output xml file as arguments
    Then the command should succeed with a return code equal to zero
    And a Robot Profiler output file output.csv should exist
    And the output.csv file should contain the expected data tab separated


Call Robot Profiler with English locale
    Given a Robot Framework output xml file has been created
    When calling Robot Profiler with English locale and the output xml file as arguments
    Then the command should succeed with a return code equal to zero
    And a Robot Profiler output file output.csv should exist
    And the output.csv file should contain the expected data with English number formatting


Call Robot Profiler with German locale
    Given a Robot Framework output xml file has been created
    When calling Robot Profiler with German locale and the output xml file as arguments
    Then the command should succeed with a return code equal to zero
    And a Robot Profiler output file output.csv should exist
    And the output.csv file should contain the expected data with German number formatting


Call Robot Profiler with multiple output XML files as input
    Given a Robot Framework output xml file has been created
    And another Robot Framework output xml file has been created
    When calling Robot Profiler with multiple output xml files as input
    Then the command should succeed with a return code equal to zero
    And a Robot Profiler output file output.csv should exist
    And the output.csv file should contain the expected data from two output xml files aggregated


*** Keywords ***
Test Setup
    Clean Up Files
    Determine OS Encoding
    Determine Locales
    Determine Tab Escaping


Clean Up Files
    Remove File    ${ROBOT TEST CASE}
    Remove File    ${ROBOT OUTPUT}
    Remove File    ${PROFILER OUTPUT}


Determine OS Encoding
    ${passed}=    Run Keyword And Return Status    Environment Variable Should Be Set    OS
    ${os}=    Set Variable If    ${passed}    %{OS}    Unix style
    ${ENCODING}=    Set Variable If    '${os}'.startswith('Windows')    cp1252    utf-8
    Set Test Variable    ${ENCODING}


Determine Locales
    ${passed}=    Run Keyword And Return Status    Environment Variable Should Be Set    OS
    ${os}=    Set Variable If    ${passed}    %{OS}    Unix style
    ${LOCALE DE}    ${LOCALE EN}=    Run Keyword If    '${os}'.startswith('Windows')    Create List    German    UK
    ...                              ELSE                                               Create List    de_DE.utf8     en_US.utf8
    Set Test Variable    ${LOCALE DE}
    Set Test Variable    ${LOCALE EN}


Determine Tab Escaping
    ${passed}=    Run Keyword And Return Status    Environment Variable Should Be Set    OS
    ${os}=    Set Variable If    ${passed}    %{OS}    Unix style
    ${TAB}=    Set Variable If    '${os}'.startswith('Windows')    \\t    '\t'
    Set Test Variable    ${TAB}


Calling Robot Profiler without any arguments
    ${rc}=    Run And Return Rc    python -m robot_profiler
    Set Test Variable    ${rc}


The command should fail with an return code not equal to zero
    Should Not Be Equal As Integers    0    ${rc}    Robot Profiler return code should not be zero


Calling Robot Profiler with help argument
    ${rc}=    Run And Return Rc    python -m robot_profiler -h
    Set Test Variable    ${rc}


The command should succeed with a return code equal to zero
    Should Be Equal As Integers    0    ${rc}    Robot Profiler return code should be zero


A Robot Framework output xml file has been created
    [Arguments]    ${output xml file name}=${ROBOT OUTPUT}
    ${content}=    Set Variable    *** Testcase ***${\n}SimpleTest${\n}${SPACE}${SPACE}Schlüsselwort Mit Ä und Ö${\n}*** Keyword ***${\n}Schlüsselwort Mit Ä und Ö${\n}${SPACE}${SPACE}Sleep${SPACE}${SPACE}5.1s${\n}
    Create File    ${ROBOT TEST CASE}    ${content}
    ${rc}=    Run And Return Rc    python -m robot.run --report NONE --log NONE --output ${output xml file name} ${ROBOT TEST CASE}
    Should Be Equal As Integers    0    ${rc}    Robot failed - return code


Another Robot Framework output xml file has been created
    A Robot Framework output xml file has been created    ${ROBOT OUTPUT TWO}


Calling Robot Profiler with default values and the output xml file as arguments
    ${rc}=    Run And Return Rc    python -m robot_profiler ${ROBOT OUTPUT}
    Set Test Variable    ${rc}


Calling Robot Profiler with utf-8 encoding and the output xml file as arguments
    ${rc}=    Run And Return Rc    python -m robot_profiler -e utf8 ${ROBOT OUTPUT}
    Set Test Variable    ${rc}


Calling Robot Profiler with colon as separator and the output xml file as arguments
    ${rc}=    Run And Return Rc    python -m robot_profiler -s : ${ROBOT OUTPUT}
    Set Test Variable    ${rc}


Calling Robot Profiler with tab as separator and the output xml file as arguments
    ${rc}=    Run And Return Rc    python -m robot_profiler -s ${TAB} ${ROBOT OUTPUT}
    Set Test Variable    ${rc}


Calling Robot Profiler with English locale and the output xml file as arguments
    ${rc}=    Run And Return Rc    python -m robot_profiler -l ${LOCALE EN} ${ROBOT OUTPUT}
    Set Test Variable    ${rc}


Calling Robot Profiler with German locale and the output xml file as arguments
    ${rc}=    Run And Return Rc    python -m robot_profiler -l ${LOCALE DE} ${ROBOT OUTPUT}
    Set Test Variable    ${rc}


Calling Robot Profiler with multiple output xml files as input
    ${rc}=    Run And Return Rc    python -m robot_profiler ${ROBOT OUTPUT} ${ROBOT OUTPUT TWO}
    Set Test Variable    ${rc}


A Robot Profiler output file output.csv should exist
    File Should Exist    ${PROFILER OUTPUT}


The output.csv file should contain the expected data
    Check Robot Profiler output


The output.csv file should contain the expected data encoded utf-8
    Check Robot Profiler output    encoding=utf-8


The output.csv file should contain the expected data colon separated
    Check Robot Profiler output    separator=:


The output.csv file should contain the expected data tab separated
    Check Robot Profiler output    separator=\t


The output.csv file should contain the expected data with English number formatting
    Check Robot Profiler output    decimal sign=\.


The output.csv file should contain the expected data with German number formatting
    Check Robot Profiler output    decimal sign=,


Check Robot Profiler output
    [Arguments]    ${encoding}=cp1252    ${separator}=;    ${decimal sign}=[,\.]
    ${content}=    Get File                       ${PROFILER OUTPUT}    encoding=${encoding}
    @{lines}=      Split To Lines                 ${content}
    ${count}=      Get Length                     ${lines}
                   Should Be Equal As Integers    3                     ${count}

    Check Robot Profiler Headline    @{lines}[0]    ${separator}
    Check Robot Profiler Dataline    @{lines}[1]    Schlüsselwort Mit Ä und Ö    1    5.1    5.1    ${separator}    ${decimal sign}
    Check Robot Profiler Dataline    @{lines}[2]    BuiltIn.Sleep                1    5.1    5.1    ${separator}    ${decimal sign}


The output.csv file should contain the expected data from two output xml files aggregated
    ${content}=    Get File                       ${PROFILER OUTPUT}    encoding=cp1252
    @{lines}=      Split To Lines                 ${content}
    ${count}=      Get Length                     ${lines}
                   Should Be Equal As Integers    3                     ${count}

    Check Robot Profiler Headline    @{lines}[0]
    Check Robot Profiler Dataline    @{lines}[1]    Schlüsselwort Mit Ä und Ö    2    10.2    5.1
    Check Robot Profiler Dataline    @{lines}[2]    BuiltIn.Sleep                2    10.2    5.1


Check Robot Profiler Headline
    [Arguments]    ${line}    ${separator}=;
    @{fields}=     Split String                   ${line}              separator=${separator}
    ${count}=      Get Length                     ${fields}
                   Should Be Equal As Integers    4                    ${count}
                   Should Be Equal                Keyword              @{fields}[0]
                   Should Be Equal                No of Occurrences    @{fields}[1]
                   Should Be Equal                Time Sum             @{fields}[2]
                   Should Be Equal                Time Avg             @{fields}[3]


Check Robot Profiler Dataline
    [Arguments]    ${line}    ${keyword}    ${occurrences}    ${time sum}    ${time avg}    ${separator}=;    ${decimal sign}=[,\.]
    @{fields}=     Split String                   ${line}           separator=${separator}
    ${count}=      Get Length                     ${fields}
                   Should Be Equal As Integers    4                 ${count}
                   Should Be Equal                ${keyword}        @{fields}[0]
                   Should Be Equal                ${occurrences}    @{fields}[1]
    ${time}=       Replace String                 ${time sum}       .    ${decimal sign}
                   Should Match Regexp            @{fields}[2]      ^${time}
    ${time}=       Replace String                 ${time avg}       .    ${decimal sign}
                   Should Match Regexp            @{fields}[3]      ^${time}
