import re


def get_sign_items(sign_items):
    my_items = []
    for item in sign_items:
        i = {}
        sign_info = item.text_content()
        m = re.search(r'Ф.И.О: ([\w ]+)\(', sign_info)
        if m:
            i['sign_specialist_name'] = m.group(1)
        m = re.search(r'Специальность:\s*([\w .-]+)\s*Ф.И.О', sign_info)
        if m:
            i['sign_specialist_role'] = m.group(1)
        m = re.search(r'Дата:\s*([0-9]{1,2}.[0-9]{1,2}.[0-9]{4}) ([0-9]{1,2}:[0-9]{2})', sign_info)
        if m:
            i['sign_date'] = m.group(1)
            i['sign_time'] = m.group(2)
        l = item.xpath('./a[contains(text(), "Отменить запись")]')
        l = l[0].xpath('@href')
        if l:
            m = re.search(r'obj=(\d+)&', l[0])
            if m:
                i['obj'] = m.group(1)
            m = re.search(r'kw=(\d+)&', l[0])
            if m:
                i['id'] = m.group(1)
            m = re.search(r'd=(\d+)&', l[0])
            if m:
                i['date'] = m.group(1)
            m = re.search(r't=([\d]{2}:[\d]{2})', l[0])
            if m:
                i['time'] = m.group(1)
        my_items.append(i)
    return my_items
