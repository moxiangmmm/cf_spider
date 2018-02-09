# coding=utf-8
import datetime

# 除了名字还有其他内容的用这个
def read_company1(csv):
    company_list = []
    with open(csv, 'r') as f:
        c_list = f.readlines()
    for c in c_list:
        com = c.strip()
        if com:
            com_list = com.split(',')
            try:
                company = com_list[2]
            except Exception as e:
                with open('log/ss_log.log', 'a') as f:
                    now = str(datetime.datetime.now())
                    f.write(now + ',' + str(e) + ',' + '' +',' + '失信信息' + '\n')
                continue
            company_list.append(company)
    return company_list

# 只有名字的csv用这个
def read_company2(csv):
    company_list = []
    with open(csv, 'r') as f:
        c_list = f.readlines()
    for c in c_list:
        company = c.strip()
        if company:
            company_list.append(company)
    return company_list


if __name__ == '__main__':
    read_company1('company/监理类公司.csv')

