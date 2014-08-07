#!/bin/bash

cp todo.desktop /usr/share/applications/

if [[ ! -d "/usr/share/todo" ]]; then
	mkdir /usr/share/todo
fi

cp todo.py /usr/share/todo/todo.py

if [[ ! -f "$HOME/.config/.ToDoList" ]]; then
	touch $HOME/.config/.ToDoList
	chown $USER:$USER $HOME/.config/.ToDoList
fi

exit
