class DefaultObjectManager:

    def __init__(self, model):
        self.model = model

    def get(self):
        # get 1
        print('called GET')
        pass

    def all(self):
        print('ALL')

    def add(self, obj):
        #
        pass

    def select(self):
        # TODO: implement autojoin fk
        pass
