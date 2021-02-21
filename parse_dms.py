import os
import json
import tkinter as tk


class MultipleScrollingListbox(tk.Tk):

    def __init__(self, _first, _p1, _p2):
        tk.Tk.__init__(self)

        self.scrollbar = tk.Scrollbar(self, orient='vertical')
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.list1 = tk.Listbox(self, yscrollcommand=self.y_scroll_1)
        self.list2 = tk.Listbox(self, yscrollcommand=self.y_scroll_2)
        self.list1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.list2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.y_view)

        line = 0
        while line < len(_first):
            if _first[line]['sender_name'] == _p1:
                num_spaces = 0
                while line < len(_first) and _first[line]['sender_name'] == _p1:
                    self.list1.insert(tk.END, _first[line]['content'])
                    line += 1
                    num_spaces += 1
                for i in range(num_spaces):
                    self.list2.insert(tk.END, '')
            elif _first[line]['sender_name'] == _p2:
                num_spaces = 0
                while line < len(_first) and _first[line]['sender_name'] == _p2:
                    self.list2.insert(tk.END, _first[line]['content'])
                    line += 1
                    num_spaces += 1
                for i in range(num_spaces):
                    self.list1.insert(tk.END, '')

    def y_scroll_1(self, *args):  # for this method and below 2 methods: https://stackoverflow.com/questions/4066974/scrolling-multiple-tkinter-listboxes-together
        if self.list2.yview() != self.list1.yview():
            self.list2.yview_moveto(args[0])
        self.scrollbar.set(*args)

    def y_scroll_2(self, *args):
        if self.list1.yview() != self.list2.yview():
            self.list1.yview_moveto(args[0])
        self.scrollbar.set(*args)

    def y_view(self, *args):
        self.list1.yview(*args)
        self.list2.yview(*args)


def gather_paths():
    json_files = []

    base_dir = ''

    for (dir_path, dir_names, file_names) in os.walk('A_DM_CHAT'):
        base_dir = dir_path
        for file_name in file_names:
            file_ext = os.path.splitext(file_name)[1]
            if file_ext == '.json':
                json_files.append(file_name)
        break

    json_files_path = []

    for json_file in json_files:
        json_files_path.append(base_dir + '/' + json_file)

    return json_files_path


def get_all_msgs_as_json(the_paths):
    all_msgs = []

    for path in the_paths:
        cur_contents = open(path, 'r')
        cur_json_obj = json.loads(cur_contents.read())
        cur_file_participants = cur_json_obj['participants']
        cur_file_messages = cur_json_obj['messages']
        msgs_as_json = []

        for message_info_index in range(len(cur_file_messages) - 1, -1, -1):
            try:
                cur_json_msg = cur_file_messages[message_info_index]
                cur_json_msg['content'] = str(cur_json_msg['content']).encode('latin-1').decode('utf-8')
                msgs_as_json.append(cur_json_msg)
            except KeyError:
                # do something about these
                pass
        all_msgs.append([cur_file_participants, msgs_as_json])
        cur_contents.close()

    return all_msgs


paths = gather_paths()
paths.sort(reverse=True)
all_msgs_as_json = get_all_msgs_as_json(paths)

first = all_msgs_as_json[0][1]
participants = all_msgs_as_json[0][0]
p1 = participants[0]['name']
p2 = participants[1]['name']
root = MultipleScrollingListbox(first, p1, p2)
root.mainloop()
