from pathlib import Path
from openpyxl import Workbook, load_workbook

#記録の追加・保存
class RecordManager:
    def __init__(self):
        self.records, self.mine, self.enemy = [], [], []
        self.items = ["You", "Enemy", "Fir(1)/Sec(0)", "Win(1)/Lose(0)"]
    
    def record(self):
        VALUES = 4
        finished = False

        while True:
            if len(self.mine) > 0:
                print("----------")
                print("mine")
                for value, item in enumerate(self.mine, 1):
                    print(f"{value}. {''.join(item)}")
                print("----------")
                print()
            if len(self.enemy) > 0:
                print("----------")
                print("enemy")
                for value, item in enumerate(self.enemy, 1):
                    print(f"{value}. {''.join(item)}")
                print("----------")
                print()

            temp = [x.strip() for x in input("> ").split(",")]
            if temp[0] == 'finish':
                break
            if len(temp) > VALUES:
                print("error: the number of elements exceeded the limit.")
                continue
            else:
                for i in range(len(temp), VALUES):
                    data = input(f"{self.items[i]}: ")
                    if data == 'finish':
                        finished = True
                        break
                    temp.append(data)
                
                if finished:
                    break

                if temp[0].isdigit():
                    num = int(temp[0]) - 1
                    if not 0 <= num < len(self.mine):
                        print("error: string index out of range(mine)")
                        continue
                    temp[0] = self.mine[num]
                if temp[1].isdigit():
                    num = int(temp[1]) - 1
                    if not 0 <= num < len(self.enemy):
                        print("error: string index out of range(enemy)")
                        continue
                    temp[1] = self.enemy[num]
                if temp[2] not in ("0", "1") or temp[3] not in ("0", "1"):
                    print("error: first/second and win/lose must be 1 or 0")
                    continue

                self.records.append(temp)
                if temp[0] not in self.mine:
                    self.mine.append(temp[0])
                if temp[1] not in self.enemy:
                    self.enemy.append(temp[1])

            temp = []


#記録の閲覧・絞り込み
class ViewManager:
    def __init__(self, record):
        self.record = record

    def view(self):
        if len(self.record.records) == 0:
            print("no data") 
        else:
            self.row(lists = self.record.records)  
        
            while True:
                print("here are options.")
                print("filter(mine): 1, filter(enemy): 2, win only: 3, lose only: 4, first: 5, second: 6, end: 0")
                command = str(input("command(view): "))

                if command in ["0", "end"]:
                    break
                elif command in ["1", "mine"]:
                    self.player_filter(1, list(self.record.mine))
                elif command in ["2", "enemy"]:
                    self.player_filter(2, list(self.record.enemy))
                elif command in ["3", "win"]:
                    self.result_filter("1", None)
                elif command in ["4", "lose"]:
                    self.result_filter("2", None)
                elif command in ["5", "first"]:
                    self.result_filter(None, "1")
                elif command in ["6", "second"]:
                    self.result_filter(None, "2")
                
                else:
                    print(f"error: it is not supported: {command}")
    
    def winlose_adjustment(self, win_or_lose):
        if win_or_lose == "1":
            return "1"
        elif win_or_lose == "2":
            return "0"
        else:
            return None

    def firsec_adjustment(self, fir_or_sec):
        if fir_or_sec == "1":
            return "1"
        elif fir_or_sec == "2":
            return "0"
        else:
            return None

    def player_filter(self, plr, lists):
        player = "You" if plr == 1 else "Enemy"
        print(f"here are lists({player}).")
        lists = list(lists)
        for value, deck in enumerate(lists, 1):
            print(f"{value}. {deck}")
        print("end: 0")

        while True:
            flt_com = input("> ")
            if not flt_com.isdigit():
                print(f"error: it is not supported: {flt_com}")
                break

            num = int(flt_com) - 1
            if num >= len(lists):
                print("error: string index out of range")
                continue
            if num < 0:
                break
            
            flt_player = lists[num]

            print("Don't display: 0")
            TF_rst = input("win(1) or lose(2): ").strip()
            TF_rst = self.winlose_adjustment(TF_rst)
            TF_odr = input("first(1) or second(2): ").strip()
            TF_odr = self.firsec_adjustment(TF_odr)
            
            self.row(result = TF_rst, order = TF_odr, player = flt_player, side = 0 if plr == 1 else 1, lists = self.record.records)
            break
    
    def result_filter(self, win_or_lose, fir_or_sec):
        TF_rst = self.winlose_adjustment(win_or_lose)
        TF_odr = self.firsec_adjustment(fir_or_sec)

        player = None
        while True:
            plr_filter = input("mine: 1,enemy: 2, Not filter: 0 > ")
            select = ["mine", "1", "enemy", "2", "not", "0"]
            if plr_filter not in select:
                print(f"error: it is not supported: {plr_filter}")
                continue

            if plr_filter in ["mine", "1"] or plr_filter in ["enemy", "2"]:
                player = "You" if plr_filter in ["mine", "1"] else "Enemy"
                lists = self.record.mine if plr_filter in ["mine", "1"] else self.record.enemy
                print(f"here are lists({player}).")
                lists = list(lists)
                for value, deck in enumerate(lists, 1):
                    print(f"{value}. {deck}")

                while True:
                    flt_com = input("> ")
                    if not flt_com.isdigit():
                        print(f"error: it is not supported: {flt_com}")
                        continue

                    num = int(flt_com) - 1
                    if not 0 <= num < len(lists):
                        print("error: string index out of range")
                        continue
                    
                    player = lists[num]
                    break
                    
            self.row(result = TF_rst, order = TF_odr, player = player, side = 0 if plr_filter in ["mine", "1"] else 1, lists = self.record.records)
            break
    
    def row(self, result = None, order = None, player = None, side = None, lists = None):
        lst = []
        print("----------")
        for value, item in enumerate(lists, 1):
            if result is not None and item[3] != result:
                continue
            if order is not None and item[2] != order:
                continue
            if player is not None and item[side] != player:
                continue

            disp = list(item)
            disp[2] = "First" if item[2] == "1" else "Second"
            disp[3] = "Win" if item[3] == "1" else "Lose"

            print(f"{value}. {', '.join(disp)}")
            lst.append(list(item))

        total = len(lst)
        print()
        print(f"battles: {total}")

        if order is None:
            first = sum(1 for it in lst if it[2] == "1")
            fir_rate = (first / total) if total > 0 else 0
            print(f"first rate: {fir_rate:.2%}")
        if result is None:
            win = sum(1 for it in lst if it[3] == "1")
            win_rate = (win / total) if win > 0 else 0
            print(f"win rate: {win_rate:.2%}")
        print("----------")


#データのロード・保存
class FileManager:
    HEADER = ["You", "Enemy", "Fir(1)/Sec(0)", "Win(1)/Lose(0)"]
    LOAD = False
    FILENAME = ''

    def __init__(self, folder = "data"):
        self.folder = Path(__file__).parent / folder
        self.folder.mkdir(parents = True, exist_ok = True)

    def load_file(self, Record, name):
        path = self.folder / self.make_filename(name)
        if not path.exists():
            print(f"error: file not found: {path}")
            return
        wb = load_workbook(path)
        ws = wb.active

        Record.records, Record.mine, Record.enemy = [], [], []
        for row in ws.iter_rows(min_row = 2, values_only = True):
            row = [str(c) for c in row]
            Record.records.append(row)
            
            if row[0] not in Record.mine:
                Record.mine.append(row[0])
            if row[1] not in Record.enemy:
                Record.enemy.append(row[1])
        
        print(f"Succeed to load file: {path.name}")
        print(f"battles: {len(Record.records)}")
        self.LOAD = True
        self.FILENAME = path.name

    def save_file(self, record, name = "", overwrite = False):
        path = self.folder / self.make_filename(name)
        if path.exists() and not overwrite:
            if not ask_yn(f"{path.name} already exists. overwrite?(y/n): "):
                path = self.unique_filename(path.name)
            
        wb = Workbook()
        ws = wb.active
        ws.append(self.HEADER)
        for row in record.records:
            ws.append(row)
        wb.save(path)
        print(f"succeed to save: {path.name}")

    def make_filename(self, name):
        name = Path(name.strip()).stem
        if not name:
            name = "data"
        return name + ".xlsx"

    def unique_filename(self, name):
        path = self.folder / name
        stem, suffix = path.stem, path.suffix

        i = 1
        while path.exists():
            path = self.folder / f"{stem}_{i}{suffix}"
            i += 1
        return path
        

#答えを聞く関数
def ask_yn(message):
    while True:
        ans = input(message).strip().lower()
        if ans in ['y', 'n']:
            return ans == 'y'
        print("error: please enter y or n")

Record = RecordManager()
View = ViewManager(Record)
File = FileManager()

#メイン処理
while True:
    print("here are options")
    print("record: 1, view: 2, file(load): 3, end: 0")
    command = str(input("command: "))

    if command in ["record", "1"]:
        print("If you want to finish taking notes, write [finish] in command.")
        Record.record()
    elif command in ["view", "2"]:
        View.view()
    elif command in ["load", "3"]:
        if Record.records:
            if not ask_yn("current data will be replaced. do you want to continue?(y/n)> "):
                continue
            if ask_yn("do you want to save?(y/n)> "):
                if File.LOAD:
                    File.save_file(Record, File.FILENAME, overwrite = True)
                else:
                    File.save_file(Record, input("file name(empty: data)> "))

        File.load_file(Record, input("file name: "))
    elif command in ["end", "0"]:
        break
    
    else:
        print(f"error: it is not supported: {command}")

#終了処理
while True:
    if ask_yn("do you want to save?(y/n): "):
        if File.LOAD:
            name = File.FILENAME
            File.save_file(Record, name, overwrite = True)
        else: 
            File.save_file(Record, input("file name(empty: data)> "))
        break
    if ask_yn("really?(y/n): "):
        break
