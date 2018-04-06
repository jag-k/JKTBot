class PrintLog:
    def __init__(self, default_call=True):
        import time
        self.time_string = time.strftime("%d.%m.%Y %H:%M")
        self.log_file = '.logs/%s.log' % self.time_string
        open(self.log_file, 'w').close()
        self.raw = ''
        self.string = ''
        if default_call:
            self.__call__("Time: \x1b[36;1m%s\x1b[0m" % self.time_string)
            self.__call__("Log file is \x1b[32;1m%s\x1b[0m" % self.log_file)

    @property
    def format_string(self):
        return self.raw

    @property
    def no_decor(self):
        text = ''
        normal = True
        for i in self.raw:
            if i == '\x1b':
                normal = False
            if i == 'm' and not normal:
                normal = True
                continue
            if normal:
                text += i
        return text

    def __call__(self, *args, sep=' ', end='\n', flush=False, print_stdout=True, print_log=True):
        import time
        self.raw = sep.join(map(str, args))+end
        self.string = self.format_string

        if print_stdout:
            print(self.string, sep='', end='', flush=flush)
        if print_log:
            print(time.strftime("[%d.%m.%Y %H:%M:%S]: "), self.no_decor, sep='', end='', flush=flush,
                  file=open(self.log_file, 'a'))


if __name__ == '__main__':
    pl = PrintLog()
    pl('Loooool))')
