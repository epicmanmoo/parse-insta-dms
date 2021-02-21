import os
import json
import tkinter as tk
import datetime


class DisplayMessages(tk.Tk):

    def __init__(self, _msgs, _p1, _p2):
        tk.Tk.__init__(self)

        self._msgs = _msgs
        self._p1 = _p1
        self._p2 = _p2
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.participant1 = tk.Listbox(self, yscrollcommand=self.y_scroll_1)
        self.participant2 = tk.Listbox(self, yscrollcommand=self.y_scroll_2)
        self.info1 = tk.Listbox(self, yscrollcommand=self.y_scroll_3)
        self.info2 = tk.Listbox(self, yscrollcommand=self.y_scroll_4)

        self.info1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.info2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.participant1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.participant2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.info1.configure(justify=tk.RIGHT)
        self.info2.configure(justify=tk.LEFT)

        self.scrollbar.config(command=self.y_view)

        line = 0
        while line < len(self._msgs):
            num_spaces = 0
            while line < len(_msgs) and _msgs[line]['sender_name'] == self._p1:
                p1_cur_msg = _msgs[line]
                p1_timestamp_ms = p1_cur_msg['timestamp_ms']
                p1_timestamp_dt = datetime.datetime.fromtimestamp(p1_timestamp_ms // 1000).replace(microsecond=0)
                p1_timestamp_dt_parts = str(p1_timestamp_dt).split()
                p1_timestamp_date = p1_timestamp_dt_parts[0]
                p1_timestamp_date_final = datetime.datetime.strptime(p1_timestamp_date, '%Y-%m-%d')
                p1_timestamp_date_final = p1_timestamp_date_final.strftime('%B %d, %Y')
                p1_timestamp_time = p1_timestamp_dt_parts[1]
                p1_timestamp_time_final = datetime.datetime.strptime(p1_timestamp_time, '%H:%M:%S')
                p1_timestamp_time_final = p1_timestamp_time_final.strftime('%I:%M:%S %p')
                p1_datetime_final = p1_timestamp_date_final + " (" + p1_timestamp_time_final + ")"
                self.participant1.insert(tk.END, p1_cur_msg['content'])
                self.info1.insert(tk.END, str(self._p1)[0:3] + "... on " + p1_datetime_final)
                line += 1
                num_spaces += 1
            for i in range(num_spaces):
                self.participant2.insert(tk.END, '')
                self.info2.insert(tk.END, '')
            num_spaces = 0
            while line < len(self._msgs) and _msgs[line]['sender_name'] == self._p2:
                p2_cur_msg = _msgs[line]
                p2_timestamp_ms = p2_cur_msg['timestamp_ms']
                p2_timestamp_dt = datetime.datetime.fromtimestamp(p2_timestamp_ms // 1000).replace(microsecond=0)
                p2_timestamp_dt_parts = str(p2_timestamp_dt).split()
                p2_timestamp_date = p2_timestamp_dt_parts[0]
                p2_timestamp_date_final = datetime.datetime.strptime(p2_timestamp_date, '%Y-%m-%d')
                p2_timestamp_date_final = p2_timestamp_date_final.strftime('%B %d, %Y')
                p2_timestamp_time = p2_timestamp_dt_parts[1]
                p2_timestamp_time_final = datetime.datetime.strptime(p2_timestamp_time, '%H:%M:%S')
                p2_timestamp_time_final = p2_timestamp_time_final.strftime('%I:%M:%S %p')
                p2_datetime_final = p2_timestamp_date_final + " (" + p2_timestamp_time_final + ")"
                self.participant2.insert(tk.END, p2_cur_msg['content'])
                self.info2.insert(tk.END, str(self._p2)[0:3] + "... on " + p2_datetime_final)
                line += 1
                num_spaces += 1
            for i in range(num_spaces):
                self.participant1.insert(tk.END, '')
                self.info1.insert(tk.END, '')

    def y_scroll_1(self, *args):
        if self.participant2.yview() != self.participant1.yview():
            self.participant2.yview_moveto(args[0])
        if self.info2.yview() != self.participant1.yview():
            self.info2.yview_moveto(args[0])
        self.scrollbar.set(*args)

    def y_scroll_2(self, *args):
        if self.participant1.yview() != self.participant2.yview():
            self.participant1.yview_moveto(args[0])
        self.scrollbar.set(*args)

    def y_scroll_3(self, *args):
        if self.info2.yview() != self.info1.yview():
            self.info2.yview_moveto(args[0])
        if self.participant2.yview() != self.info1.yview():
            self.participant2.yview_moveto(args[0])
        self.scrollbar.set(*args)

    def y_scroll_4(self, *args):
        if self.info1.yview() != self.info2.yview():
            self.info1.yview_moveto(args[0])
        self.scrollbar.set(*args)

    def y_view(self, *args):
        self.participant1.yview(*args)
        self.participant2.yview(*args)
        self.info1.yview(*args)
        self.info2.yview(*args)


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

for msgs in range(len(all_msgs_as_json)):
    p1 = all_msgs_as_json[msgs][0][0]['name']
    p2 = all_msgs_as_json[msgs][0][1]['name']
    root = DisplayMessages(all_msgs_as_json[msgs][1], p1, p2)
    root.state('zoomed')
    root.title("Messages " + str(msgs + 1))
    root.mainloop()
