'''
Python application for a simple TODO list with GTK+3
Copyright (C) 2014 Kyle Hopkins

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from gi.repository import Gtk
import os


class ToDoList(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='To Do List')
        self.set_border_width(10)
        self.set_default_size(500, 200)
        self.numItems = 0
        self.lastItem = None
        self.listItems = list()
        self.filePath = os.path.expanduser('~/.config/.ToDoList')
        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(15)
        self.add(self.grid)
        # starting widgets
        headerLabel = Gtk.Label('To Do:', xalign=0)

        self.itemEntry = Gtk.Entry()
        self.itemEntry.set_max_length(40)
        self.itemEntry.set_hexpand(True)
        self.itemEntry.connect('activate', self.addClick)

        btnAddItem = Gtk.Button(label='Add Item')
        btnAddItem.set_halign(Gtk.Align.END)
        btnAddItem.connect('released', self.addClick)

        # add them in the grid
        self.grid.add(headerLabel)
        self.grid.attach_next_to(self.itemEntry, headerLabel, Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(btnAddItem, self.itemEntry, Gtk.PositionType.RIGHT, 1, 1)
        self.lastItem = headerLabel

        self.programLoad()

    def addItem(self, value):
        '''Adds a new task to the end of the list'''
        newBox = Gtk.Box()
        newLabel = Gtk.Label(value, xalign=0)
        newButton = Gtk.CheckButton()
        newButton.set_halign(Gtk.Align.END)
        #newButton.connect('released', self.btnChange)

        newBox.pack_start(newLabel, True, True, 15)
        newBox.pack_start(newButton, True, True, 0)

        self.numItems += 1
        self.listItems.append(newBox)

        self.grid.attach_next_to(newBox, self.lastItem, Gtk.PositionType.BOTTOM, 3, 1)
        newBox.show_all()
        self.lastItem = newBox

    def addClick(self, widget):
        entryText = self.itemEntry.get_text()
        if entryText:
            self.addItem(entryText)
            self.itemEntry.set_text('')

    def updateList(self):
        for parent in self.listItems:
            children = parent.get_children()
            if children[1].get_active():
                self.listItems.remove(parent)

    def programLoad(self):
        if self.fileCheck():
            with open(self.filePath, encoding='utf-8') as openFile:
                for line in openFile:
                    self.addItem(line.strip())

    def programSave(self, something, somethingElse):
        self.updateList()
        with open(self.filePath, mode='w', encoding='utf-8') as openFile:
            for i in range(0, len(self.listItems)):
                openFile.write(self.listItems[i].get_children()[0].get_text())
                openFile.write('\n')
                Gtk.main_quit()

    def fileCheck(self):
        try:
            with open(self.filePath, encoding='utf-8'):
                pass
                return True
        except:
            return False

if __name__ == '__main__':
    win = ToDoList()
    win.connect('delete-event', win.programSave)
    win.show_all()
    Gtk.main()
