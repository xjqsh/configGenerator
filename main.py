import os
from string import Template

import readline
import pandas as pd

from InvUtil import MenuHelper


def run():
    if not os.path.exists('./output'):
        os.makedirs('./output')

    completer = Completer()
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer.comp)

    completer.suf = '.txt'

    while True:
        template_file_name = input('Select the config template(Press TAB to completion):\n')

        try:
            template_file = open(template_file_name, encoding='utf8')
            template = Template(template_file.read())
            template_file.close()
            break
        except FileNotFoundError:
            print(f'No such file: {template_file_name}')

    completer.suf = '.csv'

    while True:
        raw = input('Select inputs(Press TAB to completion):\n')

        try:
            data = pd.read_csv(raw, header=0)
            break
        except FileNotFoundError:
            print(f'No such file: {raw}')

    readline.set_completer()

    t = input('The start and end line of the shop page? (two integer, split by \'-\', press ENTER to use default '
              'value 2-5): \n')

    if t == "":
        inv = MenuHelper()
    else:
        ls, le = t.split('-')
        inv = MenuHelper(line=int(ls) - 1, line_s=int(ls) - 1, line_e=int(le) - 1)

    if input('Use menu mode? (Enter \'y\' to use, otherwise input anything else):\n') == 'y':
        # shop mode
        shop_name = input('Enter the shop name:\n')

        completer.suf = '.txt'
        readline.set_completer(completer.comp)

        footer = None
        while True:
            t = input('Gen shop footer? (ENTER the footer file name, or just press ENTER if not needed):\n')
            if t == "":
                break
            else:
                try:
                    footer_file = open(t, encoding='utf8')
                    footer = Template(footer_file.read())
                    footer_file.close()
                    break
                except FileNotFoundError:
                    print(f'No such file: {raw}')

        output_file = open('.\\output\\' + inv.get_page_idf(shop_name) + ".yml", encoding='utf8', mode='w')
        write_page_basic(footer, inv, output_file, shop_name)

        cnt, page_cnt = 0, 1

        for index, line in data.iterrows():
            tmp = line.to_dict()

            tmp['loc'] = inv.get_idf()
            tmp['inv'] = inv.get_solt()

            output_file.write(template.safe_substitute(tmp) + '\n')
            cnt += 1

            if inv.next():
                output_file = new_shop_page(footer, inv, shop_name)
                page_cnt += 1

        output_file.close()

        print(f'Generation completed. {cnt} entries and {page_cnt} pages in total.')

    else:
        # normal mode
        t = input('Enter the output file name (Press ENTER to use "output.txt" as default):\n')
        if t == "":
            output_file_name = "output.txt"
        else:
            output_file_name = t

        output_file = open('.\\output\\' + output_file_name, encoding='utf8', mode='w')

        cnt = 0

        for index, line in data.iterrows():
            tmp = line.to_dict()

            tmp['loc'] = inv.get_idf()
            tmp['inv'] = inv.get_solt()
            inv.next()

            output_file.write(template.safe_substitute(tmp) + '\n')
            cnt += 1

        output_file.close()

        print(f'Generation completed. {cnt} entries in total.')

    os.system('pause')


def new_shop_page(footer, inv, shop_name):
    output_file = open('.\\output\\' + inv.get_page_idf(shop_name) + '.yml', encoding='utf8', mode='w')
    write_page_basic(footer, inv, output_file, shop_name)
    return output_file


def write_page_basic(footer, inv, output_file, shop_name):
    output_file.write(f'ShopName: {inv.get_page_idf(shop_name)}\n')
    output_file.write(f'DisplayName: {inv.get_page_idf(shop_name)}\n')
    output_file.write('shop:\n')
    if footer is not None:
        output_file.write(footer.safe_substitute(shop_prev=inv.get_page_prev_idf(shop_name),
                                                 shop_next=inv.get_page_next_idf(shop_name)))
        output_file.write('\n')


class Completer:
    suf = ''

    def comp(self, text, state):
        options = [i for i in os.listdir('.') if i.startswith(text) and os.path.splitext(i)[1] == self.suf]
        if state < len(options):
            return options[state]
        else:
            return None


if __name__ == '__main__':
    run()
