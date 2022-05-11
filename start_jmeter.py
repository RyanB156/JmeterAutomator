import os, sys, getopt, pandas, glob
from datetime import datetime
from pathlib import Path

command_line_usage = 'start_jmeter.py -t <testfile> -l <logfolder> -c <x,y,z,...>'


def main(argv):
    temp_test_file = r'.\temp_test.jmx'
    jmeter_path = Path(r'.\jmeter\bin\jmeter.bat').absolute()
    test_file = ''
    log_folder = ''
    verbose = False
    # defaults to one, specify as a string of numbers separated by commas with no spaces
    #  e.g. 1,5,10
    user_counts = ['1']
    try:
        opts, args = getopt.getopt(argv, "hvt:l:c:", ["test-file=", "log-folder=", "user-counts="])
    except getopt.GetoptError:
        print(command_line_usage)
        sys.exit(2)
        
    print('')
    for opt, arg in opts:
        print(opt, arg)
        if opt == '-h':
            print(command_line_usage)
            sys.exit()
        elif opt == '-v':
            verbose = True
        elif opt in ("-t", "--test-file"):
            test_file = arg
        elif opt in ("-l", "--log-file"):
            log_folder = arg
        elif opt in ("-c", "--user-counts"):
            user_counts = arg.split(',')
            for count in user_counts:
                if int(count) < 1:
                    print('The user counts must be >= 1')
                    sys.exit(2)

    # Exit if no test or log file name provided
    if not test_file:
        print('Unable to find the test file\n')
        print(command_line_usage)
        sys.exit(2)
    if not log_folder:
        print('Unable to find the log folder\n')
        print(command_line_usage)
        sys.exit(2)

    if verbose:
        print('')
        print(f'Disabling listeners. Writing results to {temp_test_file}.')
    disable_listeners(test_file, temp_test_file, verbose)

    if verbose:
        print('')
        print(f'Input file is {test_file}')
        print(f'Output folder is {log_folder}')
        print('')

    # Get name of test from the test file path
    test_name = test_file.split('\\')[-1].split('.')[0]
    current_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    # Add current date and time to the file name for unique logs
    test_name_unique = test_name + '_' + current_time
    log_file_base = os.path.join(log_folder, test_name_unique)
    # Get current time

    if verbose:
        print(f'log_file_base: {log_file_base}')

    for count in user_counts:
        print('')
        # jmeter -Jthreads=1000 -n -t test.jmx -l result.csv
        # JMeter convention calls for '.jtl' log files, but for now use .csv to use Excel
        # Write logs into a new folder with name '<testname>_<year>_<month>_<day>_<hour>_<minute>_<second>'
        temp_log_file = os.path.join(log_file_base, f'{test_name_unique}_users_{count}.csv')
        if verbose:
            print(f'Running jmeter script with {count} user{"s" if int(count) > 1 else ""}')
            print(f'Logging to {temp_log_file}')
            print(f'Running command "{jmeter_path} -Jthreads={count} -n -t {temp_test_file} -l {temp_log_file}"')
            print('')
        os.system(f'"{jmeter_path} -Jthreads={count} -n -t {temp_test_file} -l {temp_log_file}"')

    create_excel_workbook(log_folder, test_name_unique, verbose)


def disable_listeners(file_path, temp_test_path, verbose):
    """
    Create a temporary test file with all listeners disabled to save memory
    :param string file_path: the path to the test file
    :param string temp_test_path: the location of the temporary file with all listeners disabled
    :param bool verbose: whether or not to log listeners disabled
    :return: None
    """
    with open(file_path) as test_file:
        # Create temporary test file for writing
        with open(temp_test_path, 'w') as temp_test_file:
            for line in test_file:
                # Disable ResultCollector elements (listeners)
                if 'ResultCollector' in line:
                    if verbose:
                        print(f'Disabling {line}')
                    line = line.replace('enabled="true"', 'enabled="false"')
                temp_test_file.write(line)
    print('')


def create_excel_workbook(log_folder, log_name, verbose):
    """
    Open the log files created and create an excel file containing the results on different pages
    :param string log_folder: the directory containing the logs
    :param string log_name: the name of the logs. e.g. test_2022_2_28_17_26_30_users_1, test_2022_2_28_17_26_30_users_5
    :return: None
    """
    # Store dataframes for all log files
    excel_file_path = os.path.join(log_folder, log_name, log_name + '.xlsx')
    if verbose:
        print(f'excel_file_path: {excel_file_path}')
        print('Opening log files')
    excel_file = pandas.ExcelWriter(excel_file_path)
    for f in glob.glob(f'{log_folder}/{log_name}/*.csv'):
        if verbose:
            print(f'Loading {f} into .xlsx file')
        user_count = f.split('users_')[1].replace('.csv', '')
        tab_name = 'Users_' + user_count
        frame = pandas.read_csv(f)
        frame.to_excel(excel_file, sheet_name=tab_name, index=False)
    excel_file.save()


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        args = ['test', '-v', '-t', 'jmeter\\bin\\test_scripts\\DeviceSearch\\VerifyDeviceSearch.jmx', '-l',
                'jmeter\\bin\\test_scripts\\DeviceSearch\\', '-c', '1,5,10,50,100,250,500,750,1000']
        # print(command_line_usage)
        # sys.exit(2)
    print('')
    print('Args: ', sys.argv)
    main(sys.argv)

