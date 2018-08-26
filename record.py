import pandas as pd

class CommentRecord:
    # keeps track of all the comments encountered already

    def __init__(self):
        try:
            file = 'comment_ids.csv'
            self._st = pd.read_csv(file, header=None).values.flatten().tolist()
        except FileNotFoundError:
            self._st = []

    def add_comment(self, id):
        self._st.append(id)          # list to store all comment ids

    def contains(self, id):
        if id in self._st:
            return True
        return False

    def save_comments(self):
        df = pd.Series(data=self._st)
        df.to_csv('comment_ids.csv', index=False, header=False)

    def get_list(self):
        return self._st

if __name__ == '__main__':
    test = CommentRecord()
    print(test.get_list())
    test.add_comment('lol')
    print(test.get_list())
    test.save_comments()