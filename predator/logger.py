import os
import sys
import datetime
import linecache


class Logger:

    def __init__(self):
        self.__now = datetime.datetime.now()

        self.__log_dir = os.getcwd() + '/logs/'

        self.__info_log_file_name = 'INFO_' + str(self.__now.month) + \
                                str(self.__now.day) + str(self.__now.year)

        self.__error_log_file_name = 'ERROR_' + str(self.__now.month) + \
                                  str(self.__now.day) + str(self.__now.year)

        self.__trace_log_file_name = 'TRACE' + str(self.__now.month) + \
                                  str(self.__now.day) + str(self.__now.year)

        self.__info_log_file = self.__log_dir + self.__info_log_file_name
        self.__error_log_file = self.__log_dir + self.__error_log_file_name
        self.__trace_log_file = self.__log_dir + self.__trace_log_file_name

        self.ERROR = 'ERROR'
        self.WARNING = 'WARNING'
        self.TRACE = 'TRACE'
        self.INFO = 'INFO'
        self.DEBUG = 'DEBUG'

    def set_log_dir(self, user_name):
        self.__log_dir = os.getcwd() + '/logs' + '/'+user_name+'/'
        self.__info_log_file = self.__log_dir + self.__info_log_file_name
        self.__error_log_file = self.__log_dir + self.__error_log_file_name
        self.__trace_log_file = self.__log_dir + self.__trace_log_file_name
        print(self.__log_dir)

    def log(self, log_message, log_level='INFO'):
        log_message = str(log_message)
        if not os.path.exists(self.__log_dir):
            os.mkdir(self.__log_dir)

        if log_level == self.ERROR:
            self.__write_log(self.__error_log_file, self.ERROR, log_message)
        elif log_level == self.TRACE:
            self.__write_log(self.__trace_log_file, self.TRACE, log_message)
        elif log_level == self.INFO:
            self.__write_log(self.__info_log_file, self.INFO, log_message)

    def __write_log(self, file_name, verbose_str, log_message):
        with open(file_name, 'a') as logs:
            try:
                if not log_message.endswith('\r\n'):
                    log_message += '\r\n'
            except:
                pass
            log_message = str(datetime.datetime.now()) + '\t[' + verbose_str + ']\t' + str(log_message)

            logs.write(log_message)

    def get_exception(self):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        line_no = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, line_no, f.f_globals)
        return exc_obj, 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, line_no, line.strip(), exc_obj)





