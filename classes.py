class Item(object):
    def __init__(self, itemid, name, description, category):
        self.itemid = itemid
        self.name = name
        self.description = description
        self.category = category

class Category(object):
    def __init__(self, categoryid, name):
        self.categoryid = categoryid
        self.name = name

class WebPageViewModel(object):
    def __init__(self, logintext, loginlink, isLoggedIn):
        self.logintext = logintext
        self.loginlink = loginlink
        self.isLoggedIn = isLoggedIn