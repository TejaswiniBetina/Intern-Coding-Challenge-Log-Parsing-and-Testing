import os.path
import sys
from datetime import datetime
from typing import Union


class TestCaseInfo:
    test_cases_processed = 0
    anomaly_info_to_write_in_list = []

    def __init__(self):
        self.dos_start_time = None
        self.dos_end_time = None
        self.dos_calculated_time = None
        self.is_there_dos = False

    def __eq__(self,other):
        return (self.dos_start_time == other.dos_start_time and self.dos_end_time == other.dos_end_time and
                self.dos_calculated_time == other.dos_calculated_time and self.is_there_dos == other.is_there_dos)


class LineInLogInfo:
    def __init__(self, line_in_log):
        self.line_in_log = line_in_log
        self.status_found_in_line = []
        self.tags_found_in_line = []
        self.timestamp_in_line = None

    def __eq__(self, other):
        return (self.line_in_log == other.line_in_log and self.status_found_in_line == other.status_found_in_line and
                self.tags_found_in_line == other.tags_found_in_line and
                self.timestamp_in_line == other.timestamp_in_line)


def check_if_line_has_tag(log_line_object: LineInLogInfo, look_for_tags_list: list, look_for_status_list: list,
                          delimiter='\t') -> LineInLogInfo:
    """
    Would take in the current line, the tags that needs to be looked in the line and the status that needs to be looked
        in the line and return the results
    :param log_line_object: A LineInLogInfo class object, usually a new initialized object
    :param look_for_tags_list: list of tags like 'Tx', 'Rx' that needs to be checked
    :param look_for_status_list: list of status like 'Instrumentation request' that needs to be checked
    :param delimiter: string split condition/delimiter
    :return: A LineInLogInfo class object
    """
    datetime_format = "%Y-%m-%d %H:%M:%S.%f"
    split_line = log_line_object.line_in_log.split(delimiter)
    for each_tag in look_for_tags_list:
        if each_tag in split_line:
            log_line_object.tags_found_in_line.append(each_tag)
            try:
                log_line_object.timestamp_in_line = datetime.strptime(split_line[0].strip(), datetime_format)

            except ValueError:
                pass
    for each in look_for_status_list:
        if each in split_line[-1]:
            log_line_object.status_found_in_line.append(each)
    return log_line_object


def calculate_time_difference(start_time: datetime, end_time: datetime) -> Union[str, None]:
    """
    Takes in 2 datetime objects and returns the difference between them in string format, if the data type is not
        datetime , returns None
    :param start_time: start time of a request-response communication
    :param end_time: end time of a request-response communication
    :return: time delta of start_time and end_time in string format or None if incompatible datatypes are passed
    """
    if type(start_time) == datetime and type(end_time) == datetime:
        return str(end_time - start_time)[:-3]
    else:
        return None


def write_results_to_file(list_of_anomaly: list, in_log_file_name: str) -> Union[str, None]:
    """
    Would take in the list of anomaly and writes them to the file
    :param list_of_anomaly: list of [anomaly case number,anomaly impacted time]
    :param in_log_file_name: input logfile name/path
    :return: name of the output file the results were saved to if the anomaly list is not empty, None if its empty
    """

    if len(list_of_anomaly)>0:
        _out_file_name = 'results_dos_' + in_log_file_name.split('/')[-1]
        _out_file = open(_out_file_name, 'w')
        for each_anomaly_info in list_of_anomaly:
            _out_file.write(f"Test case #{each_anomaly_info[0]} - Dos time is " + str(each_anomaly_info[1]) + '\n')
        _out_file.close()

        return _out_file_name
    else:
        return None


def process_logfile_return_anomaly_list(in_logfile_name_or_path: str) -> list:
    """
    would take in logfile name , processes the file and returns the list of anomaly detected
    :param in_logfile_name_or_path: input logfile name/path
    :return: list of [anomaly case number,anomaly impacted time]
    """
    _temp_log_file = open(in_logfile_name_or_path, 'r')
    _temp_test_case_info_object = TestCaseInfo()
    look_for_tags = ['Tx', 'Rx']
    look_for_status = ['Instrumentation request', "Attempt", 'Response']

    for each_line in _temp_log_file:

        if len(each_line.strip()) > 10:
            _temp_log_info_object = LineInLogInfo(each_line.strip())
            _temp_log_info_object = check_if_line_has_tag(_temp_log_info_object, look_for_tags, look_for_status)
            is_there_anomaly = check_if_anomaly(_temp_log_info_object, _temp_test_case_info_object)

            if (_temp_test_case_info_object.is_there_dos and _temp_test_case_info_object.dos_start_time is not None and
                    _temp_test_case_info_object.dos_end_time is not None):
                _temp_test_case_info_object = TestCaseInfo()
            elif (_temp_test_case_info_object.dos_start_time is not None and _temp_test_case_info_object.dos_end_time is
                  not None):
                _temp_test_case_info_object = TestCaseInfo()
    _temp_log_file.close()
    return TestCaseInfo.anomaly_info_to_write_in_list


def check_if_anomaly(log_info_object: LineInLogInfo, test_case_info_object: TestCaseInfo) -> bool:
    """
    Would process the line in log file , test case info and adds that to list if anomaly is detected
    :param log_info_object: A LineInLogInfo class object
    :param test_case_info_object: A TestCaseInfo class object
    :return: True is an anomaly is detected and False if no anomaly
    """
    if ('Instrumentation request' in log_info_object.status_found_in_line and
            'Attempt' not in log_info_object.status_found_in_line and 'Tx' in log_info_object.tags_found_in_line):
        test_case_info_object.dos_start_time = log_info_object.timestamp_in_line

    elif ('Response' in log_info_object.status_found_in_line and test_case_info_object.dos_start_time is not None and
          'Rx' in log_info_object.tags_found_in_line):
        test_case_info_object.dos_end_time = log_info_object.timestamp_in_line
        TestCaseInfo.test_cases_processed += 1

        if test_case_info_object.is_there_dos:
            test_case_info_object.dos_calculated_time = calculate_time_difference(test_case_info_object.dos_start_time,
                                                                                  test_case_info_object.dos_end_time)

            TestCaseInfo.anomaly_info_to_write_in_list.append([test_case_info_object.test_cases_processed,
                                                               test_case_info_object.dos_calculated_time])
            return True

    elif 'Tx' in log_info_object.tags_found_in_line and 'Attempt' in log_info_object.status_found_in_line:
        test_case_info_object.is_there_dos = True

    return False


def main(log_filename_path: str) -> None:
    """
    The main function takes in the input file log name and writes the results of the analysis to file
    :param log_filename_path: input logfile name/path
    :return: None
    """
    _temp_result_list = process_logfile_return_anomaly_list(log_filename_path)

    outfile_name=write_results_to_file(_temp_result_list, log_filename_path)
    infile_name = log_filename_path.split('/')[-1]
    print(f'The analysis/results of the {infile_name} is saved to {outfile_name}')

if __name__ == '__main__':
    # checks if system arguments are of length 2
    # # #if yes, program would continue and call the main function
    # # #if no, program would exit execution showing that file does not exist in the current/specified path
    # else program would end indicating on terminal that it needs the parameters to be in the specified format
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            input_logfile_path_name = sys.argv[1]
            main(input_logfile_path_name)

        else:
            print(f"Could not find the file {sys.argv[1]} in the specified path, Please check and rerun")
    else:
        print('Unexpected input format received, The format should be \n'
              'python log_processor.py filename.log')
