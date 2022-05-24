import re

# 电话号码正则表达式
tel_pattern = r'([\u4e00-\u9fa5]+[:：](\d*-\d{7,8}|\d{7,8}([,， ]*\d)*))'
# 所属组织正则表达式
org_pattern = r'([\u4e00-\u9fa5]*)(\u53a6\u95e8)([\u4e00-\u9fa5]*)'


# 正则表达式
def find_tel(str2) -> list:
    result = []
    next_str = re.search(tel_pattern, str2, re.U)
    if not next_str:
        return []
    ss = next_str.group()
    while True:
        result.append(ss)
        str2 = str2[next_str.span()[1]:]
        if re.search(tel_pattern, str2, re.U) is None:
            break
        next_str = re.search(tel_pattern, str2, re.U)
        ss = next_str.group()
    return result


def find_org(str):
    org = re.search(org_pattern, str, re.U)
    if org:
        return org.group()
    return None


def main():
    str = input()
    str2 = str
    # 找到组织
    org = find_org(str)
    # 找到对应的电话号码列表
    tel_list = find_tel(str2)
    print(org, end=' ')
    for item in tel_list:
        print(item, end=' ')
    print()


if __name__ == '__main__':
    main()
