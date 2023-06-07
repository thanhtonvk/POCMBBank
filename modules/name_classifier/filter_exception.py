def read_file(path):
  file = open(path)
  data = file.read()
  data_to_list_ = data.split("/n")
  data_to_list = (list(set(data_to_list_)))
  file.close()
  return data_to_list
tien_to_hau_to_1_word = read_file('data/name_classifier/rule_files/tiento_hauto_1word.txt')
tien_to_hau_to_mutil_word = read_file('data/name_classifier/rule_files/tiento_hauto_multi-word.txt')

ngoai_le_ca_nhan_mutil_word = read_file('data/name_classifier/rule_files/ngoai_le_ca_nhan_mutil_word.txt')
ngoai_le_ca_nhan_one_word = read_file('data/name_classifier/rule_files/ngoai_le_ca_nhan_one_word.txt')

special_name = read_file('data/name_classifier/rule_files/special_person_name.txt')
non_person = read_file('data/name_classifier/rule_files/non_person')


ngoai_le_one_word = ['codekhongsudung','code','inactive', "notuser", "notuserkhongdung", "notused","khongsudung","test","notuse","nouser",
                    "noname", "huy+cmt", "huycode", "huydotrungcode", "huy-", "-huy",'noteusedd3','dbc.','ckd.','alm#','ht.','fghh','notused.','ptn',
                     "upload cmnd",'da tat toan tai khoan','test o boarding','mot used','lam viec khac','khong dang ky']
ngoai_le_mutil_word = ['huy code','huy do trung so', 'huy do trung code','huy do trung thong tin','trung code','code huy', "not used", "not use",
                       "khong sudung","khongsu dung", "huy +","- huy"
                      "no name", "khong su dung", "khong dang dung", "huy co do trung", "huy do kh 2", "huy do trung cmnd", "huy -", "golive payroll","golive khcn","not be used",
                      ]
list_tap_mo_multi_word = ["chua xac minh", "chuyen sang code", "code online", "code trung","ho va ten:"]
list_tap_mo_one_word = [".com", "gmail", "khcn-vat-out", "gmail.com"]
# mutil word
def loc_khtc2(text):
    is_khtc = False
    for word in tien_to_hau_to_mutil_word:
        if word in text:
            is_khtc = True
            break
    return is_khtc

# one word
def loc_khtc1(text):
    words = text.split()
    is_khtc = False
    for word in words:
        if word in tien_to_hau_to_1_word:
       
            is_khtc = True
            break
    return is_khtc

# loc ten ngoai le
def loc_ngoai_le_one_word(text):
    words = text.split()
    is_ngoai_le = False
    for word in words:
        if word in ngoai_le_one_word:
            is_ngoai_le = True
            break
    return is_ngoai_le
def loc_ngoai_le_mutil_word(text):
    is_ngoai_le = False
    for word in ngoai_le_mutil_word:
        if word in text:
            is_ngoai_le = True
            break
    return is_ngoai_le


# lọc ngoại lệ tên người
def loc_ngoai_le_ca_nhan_one_word(text):
    words = text.split()
    is_ngoai_le = False
    for word in words:
        if word in ngoai_le_ca_nhan_one_word:
         
            is_ngoai_le = True
            break
    return is_ngoai_le

def loc_ngoai_le_ca_nhan_mutil_word(text):
    is_ngoai_le = False
    for word in ngoai_le_ca_nhan_mutil_word:
        if word in text:
            is_ngoai_le = True
            break
    return is_ngoai_le
        

def has_special_char(s):
    for c in s:
        if not (c.isalpha() or c == ' '):
            return True
    return False


def has_one_word(s):
    if " " not in s:
        return True
    return False

def has_is_full_number(s):
    return s.isdigit()

def has_over_2number(s):
    is_over_2number = False
    if any(c.isalpha() for c in s) and any(c.isdigit() for c in s) and sum(c.isdigit() for c in s) >= 2:
        is_over_2number = True
    return is_over_2number

def check_person_name(s):
    is_person_name = False
    for name in special_name:
        if s == name:
            is_person_name = True
    return is_person_name

# loc tap mo
def loc_tapmo_one_word(text):
    words = text.split()
    is_tapmo = False
    for word in words:
        if word in list_tap_mo_one_word:
            is_tapmo = True
            break
    return is_tapmo
def loc_tapmo_mutil_word(text):
    is_tapmo = False
    for word in list_tap_mo_multi_word:
        if word in text:
            is_tapmo = True
            break
    return is_tapmo