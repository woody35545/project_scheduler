from view.consoleView import *
from model import dao
import environment.enviroment as env
import os
dao.init()
user_input = ""

COMMAND_TOKENS = {'ls'}
def compare(str1,str2):
    if str(str1).strip() == str(str2).strip():
        return True
    else:
        return False


while True:
    command_, param1_, param2_, param3_ = "","","",""
    p(("command > "))
    user_input = str(input()).strip()
    command_,param1_,param2_,contents_ = command_analyize(user_input)
    pl()
    if compare(command_,""):
        dao.show_projects()
    if compare(command_,"ls"):
        if str(param1_) == "-m":
            dao.show_marked_project()
        elif str(param1_) == "-u":
            dao.show_undone_project()
        elif str(param1_) == "-t":
            dao.show_team_projects()
        elif str(param1_) == "-s":
            dao.show_solo_projects()
        elif str(param1_) == "-su":
            dao.show_solo_undone_projects()
        elif str(param1_) == "-sum":
            dao.show_solo_undone_marked_projects()
        else:
            dao.show_projects()
        pl()
    if compare(command_,"lsm"):
        dao.show_marked_project()
    if compare(command_,"add"):
        dao.add_project()
    if compare(command_,"del"):
        if param1_ != "":
            dao.delete_project(param1_)
        else:
            dao.delete_project()
    if compare(command_,"mod"):
        if param1_ == "status":
            dao.modify_project_status(str(param2_),str(contents_))
        elif param1_ == "name":
            dao.modify_project_name(str(param2_),str(contents_))


        elif param1_ =="start_date":
            dao.modify_project_start_date(str(param2_),str(contents_))
        elif param1_ =="end_date":
            dao.modify_project_end_date(str(param2_),str(contents_))
        elif param1_ =="content":
            dao.modify_project_content(str(param2_),str(contents_))

    if compare(command_,"help"):
        print_help_msg()
        pl(f"DATA: {dao.data_loads}/{env.MAX_DATA_SIZE}")
    if compare(command_,"sort"):
        dao.sort_by_expire_date()
    if compare(command_,"clear"):
        os.system("cls")

    if compare(command_,"mark"):
        dao.modify_mark(param1_)
    if compare(command_,"marked"):
        dao.show_marked_project()
    if compare(command_,"shell"):
        p("shell command > ")
        input_shell_command = str(input())
        os.system(str(input_shell_command))