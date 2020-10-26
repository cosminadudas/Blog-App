class Pagination:

    def __init__(self, page_number, last_page):
        self.limit = 5
        self.first_page = 0
        self.page_number = page_number
        self.last_page = last_page
