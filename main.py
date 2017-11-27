import tkinter as tk
import random
from tkinter import ttk
import json


import datetime
import random

import os

os.system("clear")
os.system("cls")

# VAR
WIDTH = 200
HEIGHT = 200



class App(tk.Tk):
    def __init__(self, *argv, **kwargv):
        tk.Tk.__init__(self, *argv, **kwargv)
        # Создаем рабочее окно
        self.geometry("1280x720+300+150")
        self.title("Access")

        # COLORS
        self.C_BG = "#FAFAFA"
        self.C_ELEMENT = "#71A163"
        self.C_ACTIVE = "#DD7374"
        self.C_FONT = "#2E2E2E"
        self.C_FONT_ON_ELEMENT = self.C_BG

        # DATA
        openfile = open("systems.json", "r")
        file_json = openfile.read()
        openfile.close()
        file_json = json.loads(file_json)
        
        self.data_systems = file_json["systems"]


        # STYLE ===========================
        style = ttk.Style()
        # style.configure(".", background=self.C_BG, foreground=self.C_FONT)
        style.configure("text.TLabel", padding=6, relief="flat", background=self.C_BG, foreground=self.C_FONT)
        style.configure("element.TButton", background="red", foreground="blue", width=50, padding=20)
        style.map("element.TButton",
                    background=[('disabled','red'), ('active','green')],
                    font=[('disabled','Arial 14'), ('active','Arial 14 bold')],
                    foreground=[('disabled','white')]
                 )
        # STYLE END =======================

        # Создаем меню
        m = tk.Menu(self) #создается объект Меню на главном окне
        self.config(menu=m) #окно конфигурируется с указанием меню для него
         
        OneMenu = tk.Menu(m, tearoff=0) #создается пункт меню с размещением на основном меню (m)
        m.add_cascade(label="Главна",menu=OneMenu) #пункту располагается на основном меню (m)
        OneMenu.add_command(label="Войти в АИС", command = lambda: self.login_AIS()) #формируется список команд пункта меню
        OneMenu.add_command(label="Список исследуемых объектов, параметров, шаблонов моделей объектов")
        OneMenu.add_command(label="Набор скриптов")
        OneMenu.add_command(label="Планировщик задач", command = lambda: self.planner())
        OneMenu.add_command(label="Данные о текущем состоянии объектов")
        OneMenu.add_command(label="Пользователи")
        OneMenu.add_command(label="Устройства")

        self.planner()
         
        TwoMenu = tk.Menu(m, tearoff=0) #второй пункт меню
        m.add_cascade(label="Дополнительно",menu=TwoMenu)
        TwoMenu.add_command(label="Моделирование объектов")

        WebButton = tk.Menu(m, tearoff=0) #третий пункт меню
        m.add("command", label="WEB-интерфейс")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (CanvasPage, CanvasPage1):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(CanvasPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def login_AIS(self):
        window = tk.Toplevel(self)
        window.geometry("480x240+300+150")
        window.title("Access - Вход АИС")
        window.resizable(False, False)
        window.grab_set()

        titleFrame = tk.Frame(window, bg=self.C_BG)
        loginFrame = tk.Frame(window, bg=self.C_BG)
        passwordFrame = tk.Frame(window, bg=self.C_BG)
        buttonFrame = tk.Frame(window, bg=self.C_BG)

        titleFrame.pack(side="top", fill='both', expand=True)
        loginFrame.pack(side="top", fill='both', expand=True)
        passwordFrame.pack(side="top", fill='both', expand=True)
        buttonFrame.pack(side="top", fill='both', expand=True)

        title = ttk.Label(titleFrame, text="Вход в АИС", anchor='center', font="Arial 14", style="text.TLabel").pack(side="top", fill='both', expand=True)

        title = ttk.Label(loginFrame, text="Логин:", anchor='center', font="Arial 13", style="text.TLabel", width=12).pack(side="left", fill='none', expand=True)
        title = ttk.Entry(loginFrame, width=50).pack(side="left", fill='none', expand=True)
        title = ttk.Label(passwordFrame, text="Пароль:", anchor='center', font="Arial 13", style="text.TLabel", width=12).pack(side="left", fill='none', expand=True)
        title = ttk.Entry(passwordFrame, width=50, show="*").pack(side="left", fill='none', expand=True)
        title = ttk.Button(buttonFrame, text="Вход").pack(side="top", fill='both', expand=True)


    def planner(self):
        window = tk.Toplevel(self)
        window.geometry("720x480+300+150")
        window.title("Access - Планировщик задач")
        window.resizable(False, False)
        window.grab_set()

        confFrame = tk.Frame(window, bg=self.C_BG)
        confFrame.pack(side="top", fill='both', expand=True)

        itemFrame = tk.Frame(window, bg=self.C_BG)
        itemFrame.pack(side="top", fill='both', expand=True)


        tv = ttk.Treeview(itemFrame)
        tv['columns'] = ('work_from', 'work_to', 'after', 'del')

        tv.heading("#0", text='Задача', anchor='center')
        tv.column("#0", anchor="center", width=150)
        
        tv.heading('work_from', text='Работает с')
        tv.column('work_from', anchor='center', width=100)
        
        tv.heading('work_to', text='по')
        tv.column('work_to', anchor='center', width=100)

        tv.heading('after', text='каждые мин.')
        tv.column('after', anchor='center', width=100)

        tv.heading('del', text='Удалить')
        tv.column('del', anchor='center', width=50)
        
        treeview = tv

        try:
            file_plans = open("plans.json", "r", encoding=("utf-8"))
            plans_list = file_plans.read()
            plans_list = json.loads(plans_list)
            file_plans.close()

            for item in plans_list:
                treeview.insert('', 0, text=item[0], values=(item[1], item[2], item[3], "Удалить"))
        except json.decoder.JSONDecodeError as err:
            print("ERROR - ошибка открытия", err)
        
        ButAddPlan = ttk.Button(confFrame, text="Добавить", command= lambda: self.addPlan(treeview)).pack(side="left", fill='both', expand=True)
        tv.pack(side="top", fill="both", expand=True)


    # Создание окна Планировщика задач
    def addPlan(self, planner):
        window = tk.Toplevel(self)
        window.geometry("720x300+300+150")
        window.title("Access - Установить задачу")
        window.resizable(False, False)
        window.grab_set()

        SettingFrame = tk.Frame(window, bg=self.C_BG)
        SettingFrame.pack(side="top", fill='both', expand=True)

        scripts = ["Задача-1", "Задача-2", "Задача-3", "Задача-4", "Задача-5"]
        combobox = ttk.Combobox(SettingFrame, values = scripts, height=5, state="readonly", font="Arial 13")
        combobox.set(scripts[0])
        combobox.pack(side="top", fill="x")

        Lfrom = ttk.Label(SettingFrame, text="Выполнять с:", anchor='center', font="Arial 13", style="text.TLabel").pack(side="top", fill='x', expand=True)
        Efrom = ttk.Entry(SettingFrame, width=20, font="Arial 13")
        Efrom.pack(side="top", fill='none', expand=True)

        LTo = ttk.Label(SettingFrame, text="Выполнять по:", anchor='center', font="Arial 13", style="text.TLabel").pack(side="top", fill='x', expand=True)
        ETo = ttk.Entry(SettingFrame, width=20, font="Arial 13")
        ETo.pack(side="top", fill='none', expand=True)

        LAfter = ttk.Label(SettingFrame, text="Периодичность:", anchor='center', font="Arial 13", style="text.TLabel").pack(side="top", fill='x', expand=True)
        EAfter = ttk.Entry(SettingFrame, width=20, font="Arial 13")
        EAfter.pack(side="top", fill='none', expand=True)


        c1 = combobox
        c2 = Efrom
        c3 = ETo
        c4 = EAfter


        BAddPlan = ttk.Button(SettingFrame, text="Установить", command= lambda: self.beginSetPlan(window, planner, c1, c2, c3, c4)).pack(side="top", fill='both', expand=True)


    def beginSetPlan(self, window, planner, c1, c2, c3, c4):
        try:
            file_plans = open("plans.json", "r", encoding=("utf-8"))
            plans_list = file_plans.read()
            file_plans.close()
            plans_list = json.loads(plans_list)
        except json.decoder.JSONDecodeError as err:
            print("ERROR - ошибка открытия", err)
            plans_list = []

        c1 = c1.get()
        c2 = c2.get()
        c3 = c3.get()
        c4 = c4.get()
        plans_list.append([c1, c2, c3, c4])

        file_plans = open("plans.json", "w", encoding=("utf-8"))
        json.dump(plans_list, file_plans)
        file_plans.close()

        item = planner.insert('', 0, text=c1, values=(c2, c3, c4, "Удалить"))
        window.destroy()






class CanvasPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.data_systems = controller.data_systems
        self.systems_list = [ i for i in self.data_systems.keys()]

        self.Top_views = tk.Frame(self)
        self.Bottom_views = tk.Frame(self)

        self.Top_views.pack(side="top", fill="both", expand=True)
        self.Bottom_views.pack(side="bottom", fill="x", expand=False)

        # создание 4х рабочей области
        self.Systems_views = tk.Frame(self.Top_views, bg=controller.C_BG, bd=1, highlightbackground="#dddddd", highlightcolor="#dddddd", highlightthickness=1)
        self.Subsystems_views = tk.Frame(self.Top_views, bg=controller.C_BG, bd=1, highlightbackground="#dddddd", highlightcolor="#dddddd", highlightthickness=1)
        self.subsys_item_views = tk.Frame(self.Top_views, bg=controller.C_BG, bd=1, highlightbackground="#dddddd", highlightcolor="#dddddd", highlightthickness=1)
        self.Table_views = tk.Frame(self.Bottom_views, bg=controller.C_BG, bd=1, highlightbackground="#dddddd", highlightcolor="#dddddd", highlightthickness=1)

        
        self.Systems_views.pack(side="left", fill="both", expand=True)
        self.Subsystems_views.pack(side="left", fill="both", expand=True)
        self.subsys_item_views.pack(side="left", fill="both", expand=True)
        self.Table_views.pack(side="bottom", fill="x", expand=False)

        self.Systems_views_UI(self.Systems_views)
        self.Subsystems_views_UI(self.Subsystems_views, None)
        self.subsys_item_views_UI(self.subsys_item_views)
        self.Table_views_UI(self.Table_views)


    def Systems_views_UI(self, frame):
        self.system_label = ttk.Label(frame, text="Системы", anchor='center', font="Arial 14", style="text.TLabel", width=30)

        self.combobox = ttk.Combobox(frame, values = self.systems_list, height=5, state="readonly")
        self.combobox.set(self.systems_list[0])

        self.but_status = False
        self.but_activate_system = ttk.Button(frame, text="Подключится", command= lambda: self.Activate_System())
        

        self.system_label.pack(side="top", fill="x")
        self.combobox.pack(side="top", fill="x")
        self.but_activate_system.pack(side="top", fill="x")

    def Activate_System(self):
        if self.but_status:
            self.but_status = False
            self.but_activate_system["text"] = "Подключится"
            self.combobox["state"] = "readonly"

            self.Subsystems_views.destroy()
            self.subsys_item_views.destroy()

            self.Subsystems_views = tk.Frame(self.Top_views, bg="#FAFAFA")
            self.subsys_item_views = tk.Frame(self.Top_views, bg="#FAFAFA")

            self.Subsystems_views.pack(side="left", fill="both", expand=True)
            self.subsys_item_views.pack(side="left", fill="both", expand=True)

            self.Subsystems_views_UI(self.Subsystems_views, None)
            self.subsys_item_views_UI(self.subsys_item_views)


        else:
            self.but_status = True
            self.but_activate_system["text"] = "Отключиться"
            self.combobox["state"] = "disabled"
            self.Subsystems_views_UI(self.Subsystems_views, self.data_systems[self.combobox.get()])



    def Subsystems_views_UI(self, frame, subsys_list):
        if subsys_list != None:
            ttk.Label(frame, text="Подсистемы", anchor='center', font="Arial 14", style="text.TLabel", width=30).grid(row=0, column=0, columnspan=2)
            self.masstab = []
            list = [i for i in subsys_list.keys()]
            for subsys in list:
                ttk.Label(frame, text=subsys, font="Arial 10", style="text.TLabel", anchor="s").grid(row=list.index(subsys)+1, column=0)
                # ttk.Button(frame, text='Показать', command=lambda: self.createTab(subsys_list[subsys], subsys)).grid(row=list.index(subsys), column=1)
                self.createTab(subsys_list[subsys], subsys)
        else:
            ttk.Label(frame, text="Подсистемы", anchor='center', font="Arial 14", style="text.TLabel", width=30).grid(row=0, column=0, columnspan=2)

    def createTab(self, subsys_list, subsystem_name):
        tab = tk.Frame(self.note)

        self.tv = ttk.Treeview(tab)
        self.tv['columns'] = ('client_class', 'user', 'time_ping', 'time_close')

        self.tv.heading("#0", text='Компьютер', anchor='w')
        self.tv.column("#0", anchor="center", width=150)
        
        self.tv.heading('client_class', text='Класс клиента')
        self.tv.column('client_class', anchor='center', width=100)
        
        self.tv.heading('user', text='Пользователь')
        self.tv.column('user', anchor='center', width=150)

        self.tv.heading('time_ping', text='Время открытия')
        self.tv.column('time_ping', anchor='center', width=100)

        self.tv.heading('time_close', text='Время закрытия')
        self.tv.column('time_close', anchor='center', width=100)
        
        self.treeview = self.tv

        for item in subsys_list:
            self.treeview.insert('', 0, text=item["PC"], values=(item["client_class"], item["user"], item["time_ping"], item["time_close"]))
    

        self.tv.pack(side="top", fill="both", expand=True)


        # ttk.Button(tab, text='close', command=tab.destroy).pack(side="bottom", padx=0, pady=10)
        self.note.add(tab, text = subsystem_name, compound="top")

    def subsys_item_views_UI(self, frame):
        self.note = ttk.Notebook(frame, width=40)
        # tab1 = tk.Frame(self.note)
        # tab2 = tk.Frame(self.note)
        # tab3 = tk.Frame(self.note)
        # ttk.Button(tab1, text='Exit', command=tab1.destroy).pack(padx=100, pady=100)


        # self.note.add(tab1, text = "Tab One", compound="top")
        # self.note.add(tab2, text = "Tab Two")
        # self.note.add(tab3, text = "Tab Three")
        self.note.pack(side="top", fill="both", expand=True)

    # таблица оповещений
    def Table_views_UI(self, frame):
        self.tv = ttk.Treeview(frame)
        self.tv['columns'] = ('datetime', 'event', 'description')

        self.tv.heading("#0", text='Тип', anchor='w')
        self.tv.column("#0", anchor="w", width=100)
        
        self.tv.heading('datetime', text='Дата и время')
        self.tv.column('datetime', anchor='center', width=200)
        
        self.tv.heading('event', text='Событие')
        self.tv.column('event', anchor='center', width=500)

        self.tv.heading('description', text='Описание')
        self.tv.column('description', anchor='center', width=500)
        
        self.treeview = self.tv
        self.LoadTable()
        self.tv.pack(side="bottom", fill="x", expand=False)

    def LoadTable(self):
        for i in range(1,100):
            index = random.randint(0,1)
            mass = [["Открытие сессии", "Закрытие сессии"],["Сессия открыта", "Сессия закрыта"]]
            self.treeview.insert('', 0, text="Клиент", values=(str(datetime.datetime.now())[:16], mass[0][index],mass[1][index]))


class CanvasPage1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pass



def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
