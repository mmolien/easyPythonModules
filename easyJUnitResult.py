#!/usr/bin/python

'''
@author: michael.molien
@version: 1.0.0
Create Date: 06.05.2013
'''

__author__ = "Michael Molien"
__version__ = "1.0.0"
__license__ = "New-style BSD"

from xml.dom import minidom
import os
import xml.etree.ElementTree as ET

class easyJUnitResult:
    '''Opens and writes to an XML file for JUnit style test results'''

    def create_xml (self,):
        # This will open the file for appending, or create it if it's not there
        try:
            with open("test_results.xml", "a+") as f:
                read_data = f.read()
                # check if there is any data in the file, if not, initialize it, otherwise it should be ready to write.
                if read_data == '':
                    f.write("<?xml version='1.0' encoding='utf-8'?><testsuites></testsuites>")
                    f.seek(0)
                    return f.read()
                else:
                    return read_data
        except( IOError ):
            print( "There was an IO Error, please check your permissions." )
            return False

    def add_results_to_xml(self, test_suite_results, test_case_results):
        '''Take the results and add it to XML.  Required a change to qaicandy so
            the results are passed to qaxml after the test script runs.'''
        # open xml results file
        data = self.create_xml()
        if data != False:
            tree = ET.parse("test_results.xml")
            root = tree.getroot()
            test_suite_attributes = {"errors": "{0}".format('0'), "failures":"{0}".format(test_suite_results['failures']), "name":"{0}".format(test_suite_results['name']), "tests":"{0}".format(test_suite_results['test_count']) }
            test_suite = ET.SubElement(root, "testsuite", test_suite_attributes)
            for test_case_result in test_case_results:
                test_case_attributes = {"classname":"{0}".format(str(test_case_result['test_suite'])), "name":"{0}".format(test_case_result['label'] + "_" + test_case_result['key']), "time":"{0}".format(test_case_result["time"]), }
                test_case = ET.SubElement(test_suite, "testcase", attrib=test_case_attributes)
                if test_case_result['result'] == 'fail':
                    test_case_attributes = {"type":"exceptions.AssertionError", "message":"Expected: {0}\n Received: {1}\n When comparing the: {2}".format(test_case_result['expected_result'], test_case_result['actual_result'], test_case_result['key'])}
                    error = ET.SubElement(test_case, "failure", attrib=test_case_attributes)

            tree.write("test_results.xml")

        else:
            print( "Couldn't open XML results." )
