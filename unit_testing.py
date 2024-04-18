import log_processor
import unittest
from datetime import datetime


class TestLogProcessor(unittest.TestCase):

    def test_calculate_time_difference_return_timedelta_value(self):
        self.assertEqual(
            log_processor.calculate_time_difference(start_time=datetime(2023, 10, 25, hour=9, minute=00, second=00),
                                                    end_time=datetime(2023, 10, 25, hour=10, minute=00, second=00)),
            '1:00'
            , " calculate_time_difference Test case failed")

    def test_calculate_time_difference_return_none(self):
        self.assertEqual(
            log_processor.calculate_time_difference(start_time=None,
                                                    end_time=datetime(2023, 10, 25, hour=10, minute=00, second=00)),
            None
            , " calculate_time_difference Test case failed")

    def test_check_if_line_has_tag_empty_line(self):
        look_for_tags = ['Tx', 'Rx']
        look_for_status = ['Instrumentation request', "Attempt", 'Response']

        _expected_line_in_log_object = log_processor.LineInLogInfo('')

        _returned_line_in_log_object = log_processor.check_if_line_has_tag(log_processor.LineInLogInfo(''),
                                                                           look_for_tags, look_for_status)

        self.assertEqual(_returned_line_in_log_object, _expected_line_in_log_object, 'check_if_line_has_tag empty '
                                                                                     'line Test case'
                                                                                     'Failed')

    def test_check_if_line_has_tag_Tx_request_line(self):
        _expected_line_in_log_object = log_processor.LineInLogInfo('2021-02-09 13:10:56.012		CAN-FD	1	Tx	'
                                                                   '11111111  	8	02 10 03 00 00 00 00 00            '
                                                                   '     	Instrumentation | Instrumentation after | '
                                                                   'Instrumentation request')
        datetime_format = "%Y-%m-%d %H:%M:%S.%f"
        look_for_tags = ['Tx', 'Rx']
        look_for_status = ['Instrumentation request', "Attempt", 'Response']

        _expected_line_in_log_object.tags_found_in_line = ['Tx']
        _expected_line_in_log_object.status_found_in_line = ['Instrumentation request']
        _expected_line_in_log_object.timestamp_in_line = datetime.strptime('2021-02-09 13:10:56.012', datetime_format)

        _returned_line_in_log_object = log_processor.check_if_line_has_tag(
            log_processor.LineInLogInfo('2021-02-09 13:10:56.012		CAN-FD	1	Tx	'
                                        '11111111  	8	02 10 03 00 00 00 00 00            '
                                        '     	Instrumentation | Instrumentation after | '
                                        'Instrumentation request'),
            look_for_tags, look_for_status)

        self.assertEqual(_returned_line_in_log_object, _expected_line_in_log_object, 'check_if_line_has_tag Tx line '
                                                                                     'Test case'
                                                                                     'Failed')

    def test_check_if_line_has_tag_Rx_response_line(self):
        datetime_format = "%Y-%m-%d %H:%M:%S.%f"
        look_for_tags = ['Tx', 'Rx']
        look_for_status = ['Instrumentation request', "Attempt", 'Response']

        _expected_line_in_log_object = log_processor.LineInLogInfo('2021-02-09 13:10:56.018		CAN-FD	1	Rx	'
                                                                   '99999999  	8	06 50 03 00 64 01 F4 55            '
                                                                   '     	Instrumentation | Response | '
                                                                   'Instrumentation response')

        _expected_line_in_log_object.tags_found_in_line = ['Rx']
        _expected_line_in_log_object.status_found_in_line = ['Response']
        _expected_line_in_log_object.timestamp_in_line = datetime.strptime('2021-02-09 13:10:56.018', datetime_format)

        _returned_line_in_log_object = log_processor.check_if_line_has_tag(
            log_processor.LineInLogInfo('2021-02-09 13:10:56.018		CAN-FD	1	Rx	99999999  	8	06 50 03 00 64 '
                                        '01 F4 55                 	Instrumentation | Response | Instrumentation '
                                        'response'),
            look_for_tags, look_for_status)

        self.assertEqual(_returned_line_in_log_object, _expected_line_in_log_object, 'check_if_line_has_tag Rx line '
                                                                                     'Test case'
                                                                                     'Failed')

    def test_check_if_line_has_tag_Tx_attempt_line(self):
        datetime_format = "%Y-%m-%d %H:%M:%S.%f"
        look_for_tags = ['Tx', 'Rx']
        look_for_status = ['Instrumentation request', "Attempt", 'Response']
        _expected_line_in_log_object = log_processor.LineInLogInfo('2021-02-09 13:10:56.560		CAN-FD	5	Tx	'
                                                                   '11111111  	8	02 10 03 00 00 00 00 00           '
                                                                   '      	Instrumentation | Attempt | '
                                                                   'Instrumentation request')

        _expected_line_in_log_object.tags_found_in_line = ['Tx']
        _expected_line_in_log_object.status_found_in_line = ['Instrumentation request', 'Attempt']
        _expected_line_in_log_object.timestamp_in_line = datetime.strptime('2021-02-09 13:10:56.560', datetime_format)

        _returned_line_in_log_object = log_processor.check_if_line_has_tag(
            log_processor.LineInLogInfo('2021-02-09 13:10:56.560		CAN-FD	5	Tx	'
                                        '11111111  	8	02 10 03 00 00 00 00 00           '
                                        '      	Instrumentation | Attempt | '
                                        'Instrumentation request'),
            look_for_tags, look_for_status)
        self.assertEqual(_returned_line_in_log_object, _expected_line_in_log_object, 'check_if_line_has_tag Tx '
                                                                                     'attempt line'
                                                                                     'Test case'
                                                                                     'Failed')

    def test_check_if_line_has_tag_notes_line(self):
        look_for_tags = ['Tx', 'Rx']
        look_for_status = ['Instrumentation request', "Attempt", 'Response']
        _expected_line_in_log_object = log_processor.LineInLogInfo('2021-02-09 13:11:06.612 EXTERNAL_PC: Executing '
                                                                   'power cycle on a stuck instrumentation, '
                                                                   'instrumentation round 100. Powering off DuT and '
                                                                   'waiting for 5 seconds to boot down.')

        _expected_line_in_log_object.tags_found_in_line = []
        _expected_line_in_log_object.status_found_in_line = []
        _expected_line_in_log_object.timestamp_in_line = None

        _returned_line_in_log_object = log_processor.check_if_line_has_tag(
            log_processor.LineInLogInfo('2021-02-09 13:11:06.612 EXTERNAL_PC: Executing power cycle on a stuck '
                                        'instrumentation, instrumentation round 100. Powering off DuT and waiting for'
                                        ' 5 seconds to boot down.'),
            look_for_tags, look_for_status)
        self.assertEqual(_returned_line_in_log_object, _expected_line_in_log_object, 'check_if_line_has_tag '
                                                                                     'notes line'
                                                                                     'Test case'
                                                                                     'Failed')

    def test_write_results_to_file_empty_anomaly_list(self):
        _expected_filename = None

        _returned_filename = log_processor.write_results_to_file([], 'inputFile.log')

        self.assertEqual(_returned_filename, _expected_filename, 'write_results_to_file empty anomaly list failed')

    def test_write_results_to_file_non_empty_anomaly_list(self):
        _expected_filename = 'results_dos_random_file.log'

        _returned_filename = log_processor.write_results_to_file([[1, '0:00:20.184'], [2, '0:00:03.239']],
                                                                 'random_file.log')

        self.assertEqual(_returned_filename, _expected_filename, 'write_results_to_file non empty anomaly list failed')

    def test_process_logfile_return_anomaly_list_empty_file(self):
        _expected_anomaly_list = []

        _returned_anomaly_list = log_processor.process_logfile_return_anomaly_list('emptyfile.log')

        self.assertEqual(_returned_anomaly_list, _expected_anomaly_list, 'process_logfile_return_anomaly_list empty '
                                                                         'file test case failed')

    def test_process_logfile_return_anomaly_list_non_empty_file(self):
        _expected_anomaly_list = [[5, '0:00:20.184'], [19, '0:00:03.239'], [29, '0:00:03.653'], [204, '0:00:04.706'],
                                  [415, '0:00:20.166'], [465, '0:00:03.247'], [784, '0:00:03.137'],
                                  [1283, '0:00:03.251'], [1395, '0:00:06.080'], [1414, '0:00:03.856']]

        _returned_anomaly_list = log_processor.process_logfile_return_anomaly_list('inputFile.log')

        self.assertEqual(_returned_anomaly_list, _expected_anomaly_list, 'process_logfile_return_anomaly_list '
                                                                         'non empty '
                                                                         'file test case failed')

    def test_check_if_anomaly_Tx_line(self):
        log_processor.TestCaseInfo.test_cases_processed = 0
        log_processor.TestCaseInfo.anomaly_info_to_write_in_list = []
        look_for_tags = ['Tx', 'Rx']
        look_for_status = ['Instrumentation request', "Attempt", 'Response']

        _temp_testcase_info_object = log_processor.TestCaseInfo()

        _expected_is_there_anomaly = False

        _returned_is_there_anomaly = log_processor.check_if_anomaly(log_processor.check_if_line_has_tag(
            log_processor.LineInLogInfo('2021-02-09 '
                                        '13:10:56.453		'
                                        'CAN-FD	5	Tx	'
                                        '11111111  	8	02 10 '
                                        '03 00 00 00 00 00     '
                                        '            	'
                                        'Instrumentation | '
                                        'Instrumentation '
                                        'after | '
                                        'Instrumentation '
                                        'request'), look_for_tags, look_for_status),
            _temp_testcase_info_object)

        self.assertEqual(_returned_is_there_anomaly, _expected_is_there_anomaly, 'check_if_anomaly Tx line Test case '
                                                                                 'failed')

    def test_check_if_anomaly_Rx_line_immediately_after_Tx(self):
        log_processor.TestCaseInfo.test_cases_processed = 0
        log_processor.TestCaseInfo.anomaly_info_to_write_in_list = []
        look_for_tags = ['Tx', 'Rx']
        look_for_status = ['Instrumentation request', "Attempt", 'Response']
        datetime_format = "%Y-%m-%d %H:%M:%S.%f"

        _temp_testcase_info_object = log_processor.TestCaseInfo()

        _temp_testcase_info_object.dos_start_time = datetime.strptime('2021-02-09 13:10:56.453', datetime_format)

        _expected_is_there_anomaly = False

        _returned_is_there_anomaly = log_processor.check_if_anomaly(log_processor.check_if_line_has_tag(
            log_processor.LineInLogInfo(
                '2021-02-09 '
                '13:11:16.637'
                'CAN-FD	5	Rx	'
                '99999999  	8	06 50 '
                '03 00 64 01 F4 55     '
                '            	'
                'Instrumentation | '
                'Response | '
                'Instrumentation '
                'response'), look_for_tags, look_for_status),
            _temp_testcase_info_object)

        self.assertEqual(_returned_is_there_anomaly, _expected_is_there_anomaly, 'check_if_anomaly Tx line Test case '
                                                                                 'failed')

    def test_check_if_anomaly_Rx_line_immediately_not_after_Tx(self):
        log_processor.TestCaseInfo.test_cases_processed = 0
        log_processor.TestCaseInfo.anomaly_info_to_write_in_list = []
        look_for_tags = ['Tx', 'Rx']
        look_for_status = ['Instrumentation request', "Attempt", 'Response']
        datetime_format = "%Y-%m-%d %H:%M:%S.%f"

        _temp_testcase_info_object = log_processor.TestCaseInfo()
        _temp_testcase_info_object.dos_start_time = datetime.strptime('2021-02-09 13:10:56.453', datetime_format)
        _temp_testcase_info_object.is_there_dos = True

        _expected_is_there_anomaly = True

        _returned_is_there_anomaly = log_processor.check_if_anomaly(
            log_processor.check_if_line_has_tag(log_processor.LineInLogInfo('2021-02-09 '
                                                                            '13:11:16.637		'
                                                                            'CAN-FD	5	Rx	'
                                                                            '99999999  	8	06 50 '
                                                                            '03 00 64 01 F4 55     '
                                                                            '            	'
                                                                            'Instrumentation | '
                                                                            'Response | '
                                                                            'Instrumentation '
                                                                            'response'), look_for_tags,
                                                look_for_status),
            _temp_testcase_info_object)

        self.assertEqual(_returned_is_there_anomaly, _expected_is_there_anomaly,
                         'check_if_anomaly Rx line not after Tx '
                         'line Test case'
                         'failed')


if __name__ == '__main__':
    unittest.main()
