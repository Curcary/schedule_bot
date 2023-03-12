from requests import get
import pandas as pd
from time import sleep
import threading as th


class parser:
    def check_current_sheet(self):
        while (True):
            try:
                new_content = get("https://serp-koll.ru/images/ep/k1/rasp1.xlsx").content
                new_sheet = pd.ExcelFile(new_content)
                if (self.content!=new_content):
                    self.book = new_sheet
                    self.update()
            except Exception:
                pass
            sleep(5*60)

    def __findcolumn(self, group_number):
        for i in range(2, 27):
            if (self.book.book.active.cell(row = 2, column = i).value==group_number):
                return i
    def __build_message(self, lessons):
        outles = []
        j = 1
        for i in range(0, len(lessons)-1, 2):
            outles.append((j, lessons[i]))
            outles.append((j, lessons[i+1]))
            j+=1
        i = 1
        while (i<len(outles)):
            if (outles[i][1]==None):
                outles.pop(i)
                i+=1
            else:
                i+=2
        outmessage = 'Расписание на ' + lessons[-1] + '\n\n'
        for i in range(0, len(outles)):
            if (outles[i][1]!=None):
                outmessage+=outles[i][0].__str__() + ". " + outles[i][1] + "\n\n"
            else:
                outmessage+=outles[i][0].__str__() + ". Нет пары\n\n"
        return outmessage

    def parse(self, group_number):
        column = self.__findcolumn(group_number)
        list_of_rows = [14, 15, 27, 28, 40, 41, 53, 54]
        lessons = []
        for i in list_of_rows:
            lessons.append(self.book.book.active.cell(row = i, column = column).value)
        if (self.book.book.active.cell(row = 66, column = column).value!=None):
            lessons.append(self.book.book.active.cell(row = 66, column = column).value)
        elif (self.book.book.active.cell(row = 67, column = column).value!=None):
            lessons.append(self.book.book.active.cell(row = 66, column = column).value)
            lessons.append(self.book.active.cell(row = 67, column = column).value)
        
        lessons.append(self.book.book.active.title)
        return self.__build_message(lessons=lessons)
    def __init__(self, update_handler) -> None:
        self.content = get("https://serp-koll.ru/images/ep/k1/rasp1.xlsx").content
        self.book = pd.ExcelFile(self.content)
        self.update = update_handler
        th.Thread(target=self.check_current_sheet).start( )

def update():
    print("Updated")
if __name__ == "__main__":
    pars = parser()
    
    lessons = pars.parse("1202")
    print(lessons)