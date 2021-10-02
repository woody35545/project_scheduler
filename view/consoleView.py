import collections as ct
import string
from view import color
import ctypes

def pl(_msg = ""):
    print(str(_msg))


def p(_msg):
    print(str(_msg), end="")


def arg_l(_str, _arrange_width, _fill_str=" "):
    # 한 필드당 공간을 _width 만큼 잡아줌.

    str_width_ = int(get_width_of_string(_str))
    if _arrange_width < str_width_:
        res = _str.strip()
    else:
        res = str(_str + str(_fill_str) * (_arrange_width - str_width_))
    return res
def arg_r(_str, _arrange_width, _fill_str=" "):
    # 한 필드당 공간을 _width 만큼 잡아줌.

    str_width_ = int(get_width_of_string(_str))
    if _arrange_width < str_width_:
        res = _str.strip()
    else:
        res = str(str(_fill_str) * (_arrange_width - str_width_)+ _str )
    return res






def arg_c(_str, _arrange_width, _fill_str=" "):
    str_width_ = int(get_width_of_string(_str))
    if _arrange_width < str_width_:
        res = _str
        return res
    else:
        # (_arrange_width - (get_width_of_string(_str)))/2
        fill_count = int(round((_arrange_width - str_width_) / 2, 0))
        res = (_fill_str * fill_count + str(_str) + _fill_str * fill_count)
        return res
def arrange_fmt_l(_format_str, _arrage_width, _fill_str = ""):
    strs = str(_format_str).split(",")
    res = ""
    for i in range (len(strs)):
        res += arg_l(strs[i],_arrage_width)
    return res

def arrange_fmt_c(_format_str, _arrage_width, _fill_str = ""):
    strs = str(_format_str).split(",")
    res = ""
    for i in range(len(strs)):
        res += arg_c(strs[i], _arrage_width)
    return res

def get_width_of_string(_string):
    _string = str(_string)
    #width_of_kor = 1.57
    width_of_kor = 2.0
    width_of_others = 1
    count_eng_upper = sum(c.isupper() for c in _string)
    count_eng_lower = sum(c.islower() for c in _string)
    count_number = sum(c.isdigit() for c in _string)
    count_space = sum(c.isspace() for c in _string)
    count_special_char = sum(v for k, v in ct.Counter(_string).items() if k in string.punctuation)
    count_not_kor = (count_eng_upper + count_eng_lower + count_number + count_space + count_special_char)
    count_kor = len(_string) - count_not_kor
    temp_res = (count_kor * width_of_kor) + (count_not_kor * width_of_others)
    res = round(temp_res, 0)
    return int(res)

def inputStr():
    res = input()
    return str(res)
def inputInt():
    while True:
        res = input()
        if type(res) == type("a"):
            pl("[!] 정수값을 입력해주세요.")
        else:
            break
    return res

def print_help_msg():
    pl("* [ls]: view data\n* [add] Add data\n* [del] Delete data\n* [mod] modify")

def reset_default():
    res = str()

def red(_text):
    res = color._red_ +" "+ _text  +" "+ color._default_
    return str(res)

def blue(_text):
    res = color._blue_  +" "+_text  +" "+ color._default_
    return str(res)


std_out_handle = ctypes.windll.kernel32.GetStdHandle(color.STD_OUTPUT_HANDLE)


def set_color(color, handle=std_out_handle):
    bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return bool



def command_analyize(_input):
    user_input = str(_input).strip()
    tokens_ = user_input.split(" ")
    command_ = ""
    param1_ = ""
    param2_ = ""
    contents_ = ""
    try:
        command_ = str(tokens_[0])
        param1_ = str(tokens_[1])
        param2_ = str(tokens_[2])
        temp = ""
        for i in range(3,len(tokens_)):
            temp += tokens_[i] + " "
        contents_ = temp.strip()


    except:
        None
    return command_,param1_,param2_,contents_

def print_project_title_bar():
    arg_width = 20
    printstr = arg_l("[No.]", 6) + arg_l("[project_name]", 40) + arrange_fmt_l("[start_date],[end_date],[status]",
                                                                               arg_width) + arg_l("[content]",
                                                                                                  60) + arg_l(
        "[remaining]", 30)
    pl(printstr)
    pl("-" * 230)