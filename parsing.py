from requests import get
import pandas as pd
from time import sleep
import threading as th
import requests.exceptions as exc

GROUP_ROW = 2

class parser:
    def get_groups(self):
        groups = []
        for i in range(2, 40):
            value = self.book.book.active.cell(row = GROUP_ROW, column = i).value
            if  value !='' and value is not None    :
                groups.append(str(self.book.book.active.cell(row = GROUP_ROW, column = i).value))
        return groups
    def check_current_sheet(self):
        while (True):
            try:
                response = get("https://serp-koll.ru/images/ep/k1/rasp1.xlsx")

            except exc.ReadTimeout:
                sleep(60)
            except exc.SSLError:
                sleep(60)
            except ConnectionError:
                sleep(60)
            finally:
                if (response!=None):
                    new_content = response.content
                    if (self.content!=new_content):
                        new_sheet = pd.ExcelFile(new_content)
                        self.content = new_content
                        self.book = new_sheet
                        self.update()
            sleep(5*60)

    def __findcolumn(self, group_number):
        for i in range(2, 35):
            if (str(self.book.book.active.cell(row = GROUP_ROW, column = i).value)==group_number):
                return i
    def __build_message(self, lessons):
        outmessage: str = 'Расписание на ' + lessons[-1] + '\n\n'
        for i in range(0, len(lessons)-1):
            if lessons[i][0] is None:
                outmessage+=str(i+1)+". Нет пары\n"
            else:
                outmessage+=str(i+1)+". "+lessons[i][0]+"\n"
            if lessons[i][1] is None:
                pass
            else:
                outmessage+=str(i+1)+". "+lessons[i][1]+"\n"
        return outmessage

    def parse(self, group_number):
        column = self.__findcolumn(group_number)
        list_of_rows = [14,15, 27,28, 40,41, 53,54, 66,67]
        lessons = []
        for i in range(0, len(list_of_rows), 2):
            row = list_of_rows[i]
            second_row = list_of_rows[i+1]
            lessons.append((self.book.book.active.cell(row = row, column = column).value,
                                  self.book.book.active.cell(row = second_row, column = column).value))       
        lessons.append(self.book.book.active.title)
        return self.__build_message(lessons=lessons)
    def __init__(self, update_handler = None) -> None:
        self.content = get("https://serp-koll.ru/images/ep/k1/rasp1.xlsx").content
        self.book = pd.ExcelFile(self.content)
        self.update = update_handler
        th.Thread(target=self.check_current_sheet).start( )

def update():
    print("Updated")
if __name__ == "__main__":
    pars = parser(update)
    
    lessons = pars.parse("1202")
    print(lessons)