class ResponseParser:
    def __init__(self):
        self.start = ""
        self.title = []
        self.context = []
        self.end = ""
        self.resp_lines = None

    def load_response(self, response):
        self.resp_lines = response.split('\n')

    def parse_response(self, keyword):
        try:
            for idx, line in enumerate(self.resp_lines):
                if line != '':
                    data = line.split(':')
                    if idx == 0:
                        self.start = data[1].strip(' \n\t\r')
                    elif idx == len(self.resp_lines) - 1:
                        self.end = data[1].strip(' \n\t\r')
                    else:
                        if len(data[1]) < 32:
                            self.title.append(data[1].strip(' \n\t\r'))
                        else:
                            self.context.append(data[1].strip(' \n\t\r'))

            paragraph = []
            for idx in range(len(self.title)):
                tmp = []
                tmp.append(self.title[idx])
                tmp.append(self.context[idx])
                paragraph.append(tmp)
            return [[f'"{keyword}"', self.start], paragraph, [self.end, f'"{keyword}"']]
        except:
            print ("====== load failed ======")
            return False

                
        