from lxml.html import parse
import sys


def xxx(url):
    doc_tree = parse(url)
    doc = doc_tree.getroot()
    table = doc.xpath(
        '//h2[contains(text(), "Расписание работы специалистов на текущую неделю")]/following-sibling::table')
    table = table[0]
    tr = table.iterchildren()
    personal = []
    item = {}
    speciality = ''
    for t_row in tr:
        if t_row.xpath('@class="table-border-light"'):
            speciality = t_row.text_content()
            continue
        elif t_row.xpath('@class="table-border-title"'):
            continue

        tds = t_row.xpath('td')

        if len(tds) == 8:
            if item:
                personal.append(item)
            item = {}
            fio = tds[0].text_content()
            item['fio'] = fio
            item['speciality'] = speciality
        else:
            if tds[0].xpath('@colspan="8" and contains(@style, "background:#f3e9dd;")'):
                item['info'] = tds[0].text_content()
            else:
                print(t_row.text_content)
    personal.append(item)
    print('Количество: ', len(personal))
    for i in personal:
        print(i)
        print('#'*40, '\n')


if __name__ == '__main__':
    xxx(sys.argv[1])
