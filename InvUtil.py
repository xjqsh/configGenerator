from typing import Optional


class MenuHelper:

    def __init__(self, col: int = 1, line: int = 1, line_s: int = 1, line_e=4):
        self.col = col
        self.line = line
        self.line_start = line_s
        self.line_end = line_e
        self.cur_page = 0

    def next(self) -> bool:
        """
        bool :return True if turn to a new page, False otherwise.
        """
        self.col += 1
        if self.col > 9:
            self.col = 1
            self.line += 1
        if self.line > self.line_end:
            self.line = self.line_start
            self.cur_page += 1
            return True
        return False

    def get_idf(self) -> str:
        return chr(ord('a') + self.line) + str(self.col)

    def get_solt(self) -> int:
        return self.col + self.line * 9

    def get_cur_page(self) -> int:
        return self.cur_page

    def get_page_idf(self, shop_name: str) -> str:
        if self.get_cur_page() == 0:
            return shop_name
        else:
            return shop_name + '_' + str(self.cur_page)

    def get_page_prev_idf(self, shop_name: str) -> Optional[str]:
        if self.get_cur_page() == 0 in (0, 1):
            return shop_name
        else:
            return shop_name + '_' + str(self.cur_page - 1)

    def get_page_next_idf(self, shop_name: str) -> str:
        return shop_name + '_' + str(self.cur_page + 1)
