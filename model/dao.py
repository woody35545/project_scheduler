from environment import enviroment as env
from view.consoleView import *
from datetime import datetime

dao_p_name = [""] * env.MAX_DATA_SIZE  # project name
dao_p_start = [""] * env.MAX_DATA_SIZE
dao_p_end = [""] * env.MAX_DATA_SIZE
dao_p_content = [""] * env.MAX_DATA_SIZE
dao_p_isdone = [""] * env.MAX_DATA_SIZE
data_file_path = env.DATA_FILE_PATH
data_loads = 0
dao_p_marks =  [0] * env.MAX_DATA_SIZE

def get_data():
    global data_loads

    file_ = open(env.DATA_FILE_PATH, 'r', encoding='UTF8')
    isEOF = False
    while (isEOF != True):
        line_ = str(file_.readline().strip("\n"))
        if line_ == "":
            isEOF = True
        else:
            if line_ == env.DATA_START:
                isDataSetEnd = False
                while (isDataSetEnd != True):
                    line_ = str(file_.readline().strip("\n"))
                    if line_ == env.DATA_END:
                        data_loads += 1
                        isDataSetEnd = True
                    else:
                        tokens = line_.split(" ")
                        fd_ = tokens[0][1:-1].strip("\n")
                        fd_data = str(line_[len(tokens[0]) + 1:])
                        if fd_ == env.FD_NAME:
                            # print(f"{fd_} => {fd_data}")
                            dao_p_name[data_loads] = fd_data
                        if fd_ == env.FD_START:
                            # print(f"{fd_} => {fd_data}")
                            dao_p_start[data_loads] = fd_data
                        if fd_ == env.FD_END:
                            # print(f"{fd_} => {fd_data}")
                            dao_p_end[data_loads] = fd_data
                        if fd_ == env.FD_ISDONE:
                            # print(f"{fd_} => {fd_data}")
                            dao_p_isdone[data_loads] = fd_data
                        if fd_ == env.FD_CONTENT:
                            # print(f"{fd_} => {fd_data}")
                            dao_p_content[data_loads] = fd_data


def show_project(_project_index):

    arg_width = 20

    number_ = str(_project_index + 1)
    if dao_p_marks[_project_index]==1:
        name_ = "★-" + dao_p_name[_project_index]
    else:
        name_ = dao_p_name[_project_index]

    start_ = dao_p_start[_project_index]
    end_ = dao_p_end[_project_index]
    isdone_ = dao_p_isdone[_project_index]
    content_ = dao_p_content[_project_index]

    remaining_string_, remaining_day_, remaining_hour_, remaining_minutes_ = get_date_diff(get_now(), end_)
    if remaining_string_ != "Expire" and remaining_string_ != "ERROR" and int(remaining_day_) == 0:
        remaining_string_ = ("[!] " +str(remaining_string_))

    remaining_ = remaining_string_.strip()

    printstr = arg_l(number_, 6,".") + arg_l(name_, 40) + arrange_fmt_l(start_ + "," + end_ + "," + isdone_,
                                                                     arg_width,) + arg_l(content_, 60) + arg_l(
        remaining_, 30)
    pl(printstr)


def show_projects():
    arg_width = 20
    printstr = arg_l("[No.]", 6) + arg_l("[project_name]", 40) + arrange_fmt_l("[start_date],[end_date],[status]",
                                                                                arg_width) + arg_l("[content]",
                                                                                                   60) + arg_l(
        "[remaining]", 30)
    pl(printstr)
    pl("-" * 230)
    for i in range(data_loads):
        show_project(i)


def add_project():
    global data_loads
    p("[+] project name > ")
    _name = str(input()).strip()
    if _name.strip("\n") == "":
        _name = "-"
    p("[+] start date > ")
    _start_date = str(input()).strip()
    if _start_date.strip("\n") == "":
        _start_date = "-"
    p("[+] end date > ")
    _end_date = str(input()).strip()
    if _end_date.strip("\n") == "":
        _end_date = "-"
    p("[+] contents > ")
    _content = str(input()).strip()
    if _content.strip("\n") == "":
        _content = "-"
    set_project(data_loads, _name, _start_date, _end_date, "X", _content)
    pl("[@] add complete!")
    data_loads += 1
    sort_by_expire_date()
    update_data()
    show_projects()


def set_project(_index, _name, _start_date, _end_date, _isdone, _content):
    dao_p_name[_index] = str(_name)
    dao_p_start[_index] = str(_start_date)
    dao_p_end[_index] = str(_end_date)
    dao_p_isdone[_index] = str(_isdone)
    dao_p_content[_index] = str(_content)
    update_data()


def set_project_name(_project_number, _name):
    dao_p_name[_project_number - 1] = str(_name).strip()
    update_data()


def set_project_status(_project_number, _status):
    dao_p_isdone[_project_number - 1] = str(_status).strip()
    update_data()


def set_project_start_date(_project_number, _date):
    dao_p_start[_project_number - 1] = str(_date).strip()
    update_data()


def set_project_end_date(_project_number, _date):
    dao_p_end[_project_number - 1] = str(_date).strip()
    update_data()


def set_project_content(_project_number, _content):
    dao_p_content[_project_number - 1] = str(_content).strip()
    update_data()


def modify_project_name(_project_number,_project_name):
    if str(_project_number) == "" or  str(_project_name) == "":
        p("[~] 이름을 변경할 프로젝트의 번호를 입력해주세요 > ")
        project_number_ = int(input())
        p("[~] 이름을 입력해주세요 > ")
        name_ = str(input())
        set_project_name(project_number_, name_)
    else:
        set_project_name(int(_project_number),str(_project_name))
    show_projects()


def modify_project_status(_project_number,_project_status):
    if str(_project_number) == "" or str(_project_status) =="":
        p("[~] 상태를 변경할 프로젝트의 번호를 입력해주세요 > ")
        project_number_ = int(input())
        p("[~] 상태를 입력해주세요 > ")
        status_ = str(input())
        set_project_status(project_number_, status_)
    else:
        set_project_status(int(_project_number),str(_project_status))
    show_projects()


def modify_project_start_date(_project_number,_start_date):
    if str(_project_number) == "" or str(_start_date) =="":
        p("[~] 시작 날짜를 변경할 프로젝트의 번호를 입력해주세요 > ")
        project_number_ = int(input())
        p("[~] 시작 날짜를 입력해주세요 > ")
        date_ = str(input())
        set_project_start_date(project_number_, date_)
    else:
        set_project_start_date(int(_project_number),str(_start_date))

    show_projects()


def modify_project_end_date(_project_number , _end_date):
    if str(_project_number) == "" or str(_end_date) =="":
        p("[~] 마감 날짜를 변경할 프로젝트의 번호를 입력해주세요 > ")
        project_number_ = int(input())
        p("[~] 마감 날짜를 입력해주세요 > ")
        date_ = str(input())
        set_project_end_date(project_number_, date_)
    else:
        set_project_end_date(int(_project_number), str(_end_date))

    show_projects()

def modify_project_content(_project_number,_project_content):
    if str(_project_number) == "" or str(_project_content) == "":
        p("[~] 내용을 변경할 프로젝트의 번호를 입력해주세요 > ")
        project_number_ = int(input())
        p("[~] 내용을 입력해주세요 > ")
        content_ = str(input())
        set_project_content(project_number_, content_)
    else:
        set_project_content(int(_project_number), str(_project_content))

    show_projects()

def modify_mark(_project_number):
    try:
        switch_mark(int(_project_number)-1)
    except:
        print("type error")

    show_projects()
def delete_project(_param = "None"):

    global data_loads
    if _param == "None":
        p("[-] 삭제할 project 번호를 입력해주세요 > ")
        project_number = int(input())
        iter_range = (data_loads - (project_number - 1) - 1)
        for i in range(project_number - 1, iter_range):
            dao_p_name[i] = dao_p_name[i + 1]
            dao_p_start[i] = dao_p_start[i + 1]
            dao_p_end[i] = dao_p_end[i + 1]
            dao_p_isdone[i] = dao_p_isdone[i + 1]
            dao_p_content[i] = dao_p_content[i + 1]
        data_loads -= 1
        update_data()
        show_projects()
    else:
        project_number = int(_param)
        iter_range = (data_loads - (project_number - 1) - 1)
        for i in range(project_number - 1, iter_range):
            dao_p_name[i] = dao_p_name[i + 1]
            dao_p_start[i] = dao_p_start[i + 1]
            dao_p_end[i] = dao_p_end[i + 1]
            dao_p_isdone[i] = dao_p_isdone[i + 1]
            dao_p_content[i] = dao_p_content[i + 1]
        data_loads -= 1
        update_data()
        show_projects()



def update_data():
    file_ = open(env.DATA_FILE_PATH, 'w', encoding="UTF8")
    for i in range(data_loads):
        file_.write("{\n")
        file_.write("*name: " + str(dao_p_name[i]) + "\n")
        file_.write("*start: " + str(dao_p_start[i]) + "\n")
        file_.write("*end: " + str(dao_p_end[i]) + "\n")
        file_.write("*isdone: " + str(dao_p_isdone[i]) + "\n")
        file_.write("*content: " + str(dao_p_content[i]) + "\n")
        file_.write("}\n")


def init():
    get_data()
    load_env_data()


def get_date_diff(date1, date2):
    date1 = "20" + \
            str(date1).replace(".", "")
    date2 = "20" + str(date2).replace(".", "")
    if date1 > date2:
        res, res_day, res_hour, res_minutes = "Expire", 0, 0, 0

        return res, res_day, res_hour, res_minutes
    else:
        try:
            timedelta_ = (datetime.strptime(date2, "%Y%m%d%H%M") - datetime.strptime(date1, "%Y%m%d%H%M"))
            days = divmod(timedelta_.total_seconds(), 86400)  # Get days (without [0]!)
            hours = divmod(days[1], 3600)  # Use remainder of days to calc hours
            minutes = divmod(hours[1], 60)  # Use remainder of hours to calc minutes
            seconds = divmod(minutes[1], 1)  # Use remainder of minutes to calc seconds
            res = "%d일 %d시간 %d분 " % (days[0], hours[0], minutes[0])
            res_day = int(days[0])
            res_hour = int(hours[0])
            res_minutes = int(minutes[0])
            return res, res_day, res_hour, res_minutes
        except:
            res, res_day, res_hour, res_minutes = "ERROR", 0, 0, 0
            return res, res_day, res_hour, res_minutes


def get_now():
    year_ = str(datetime.now().year)[2:]
    month_ = str(datetime.now().month)
    if int(month_) < 10:
        month_ = "0" + month_
    day_ = str(datetime.now().day)

    if int(day_) < 10:
        day_ = "0" + day_

    hour_ = str(datetime.now().hour)

    minute_ = str(datetime.now().minute)
    if int(minute_) < 10:
        minute_ = "0"+minute_
    res = str(year_ + month_ + day_ + hour_ + minute_)
    return res

def sort_by_expire_date():
    res = [0] * (data_loads)
    for i in range (len(res)):
        res[i] = dao_p_end[i]

    for size in reversed(range(len(res))):
        for i in range(size):
            if "20" + str(res[i]).replace(".", "") > "20" + str(res[i + 1]).replace(".", ""):
                swap(res, i+1, i)
                swap_data(i+1,i)


def swap(x, i, j):
    x[i], x[j] = x[j], x[i]

def swap_data(i,j):
    global dao_p_name,dao_p_isdone,dao_p_end,dao_p_start,dao_p_content
    swap(dao_p_name,i,j)
    swap(dao_p_isdone,i,j)
    swap(dao_p_end,i,j)
    swap(dao_p_start,i,j)
    swap(dao_p_content,i,j)
    update_data()
def set_marks(_index,_mark):
    global  dao_p_marks
    dao_p_marks[_index] = _mark
    update_env_data()
def switch_mark(_index):
    if dao_p_marks[_index] == 0:
        set_marks(_index,1)
    else:
        set_marks(_index,0)
def load_env_data():
    file_ = open(env.ENV_DATA_FILE_PATH,"r",encoding= "UTF8")
    readline_ = file_.readline().strip("\n")
    marks_load =0
    while (readline_ != ""):
        set_marks(marks_load, int(readline_))
        marks_load += 1
        readline_ = file_.readline()

def update_env_data():
    file_ = open(env.ENV_DATA_FILE_PATH,"w",encoding='UTF8')
    for i in range(env.MAX_DATA_SIZE):
        file_.write(str(dao_p_marks[i])+"\n")
    file_.close()
def show_team_projects():
    print_project_title_bar()
    for i in range(data_loads):
       if isTeamProject(i):
           show_project(i)
def show_solo_projects():
    print_project_title_bar()
    for i in range(data_loads):
        if isTeamProject(i) == False:
            show_project(i)
def show_solo_undone_projects():
    print_project_title_bar()
    for i in range(data_loads):
        if isTeamProject(i) == False and isUndone(i):
            show_project(i)

def show_solo_undone_marked_projects():
     print_project_title_bar()
     for i in range(data_loads):
         if isTeamProject(i) == False and isUndone(i) and isMarked(i):
             show_project(i)

def show_undone_project():
    print_project_title_bar()
    for i in range (data_loads):
        if isUndone(i):
            show_project(i)
def show_marked_project():
    print_project_title_bar()
    for i in range (data_loads):
        if isMarked(i):
            show_project(i)

def isUndone(i):
    if str(dao_p_isdone[i]) == "X" or str(dao_p_isdone[i]) == "x" or str(dao_p_isdone[i]) == "-" or str(
        dao_p_isdone[i]) == "~":
        return True
    else:
        return False

def isMarked(i):
    if dao_p_marks[i] == 1:
        return True
    else:
        return False
def isTeamProject(i):
    if dao_p_name[i][0] == "<":
        return True
    else:
        return False