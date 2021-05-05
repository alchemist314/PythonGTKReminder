#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import gtk
import time
from threading import Timer
import gobject

from PIL import Image, ImageDraw
from PIL import ImageFont

path_to_ttf='/home/PYTHON_BIN/remider/OpenSans-Regular.ttf'
path_to_png="/home/PYTHON_BIN/reminder/reminder.png"
path_to_txt='/home/PYTHON_BIN/reminder/reminder.txt'

class SystrayIconApp:
    def __init__(self):

	self.viewed_array=[]
	self.tray = gtk.StatusIcon()
	self.tray.set_from_file(path_to_png) 
	self.tray.connect('popup-menu', self.on_right_click)
        self.val = 0
        self.globalform()

	#10min =(10*60000)
        gobject.timeout_add((60*60000), self.timeout)

    def on_right_click(self, icon, event_button, event_time):
	self.make_menu(event_button, event_time)

    def make_menu(self, event_button, event_time):
	menu = gtk.Menu()

	# show edit dialog
	edit = gtk.MenuItem("Edit")
	edit.show()
	menu.append(edit)
	edit.connect('activate', self.show_edit_dialog)

	# add quit item
	quit = gtk.MenuItem("Quit")
	quit.show()
	menu.append(quit)
	quit.connect('activate', gtk.main_quit)

	menu.popup(None, None, gtk.status_icon_position_menu, event_button, event_time, self.tray)

    def show_edit_dialog(self, widget):
	#set path to editor
	os.system("/usr/bin/mate-terminal --window --working-directory=\"~/\" --command=\"/usr/bin/mcedit "+path_to_txt+"\"");

    def timeout(self):
        self.val += 1
        self.globalform()
        return True

    def show_window(self):
	global message_window
        widget = gtk.DrawingArea()
        widget.show()

        message_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        message_window.set_title(str(self.today_date))
        message_window.set_default_size(550, 120)
        message_window.set_position(gtk.WIN_POS_CENTER)

        col = gtk.gdk.Color('#0f0')
        col1 = gtk.gdk.Color('#ffff11')

        message_window.present()
        widget.modify_bg(gtk.STATE_NORMAL, col)
        message_window.modify_bg(gtk.STATE_NORMAL, col1)

        fixed = gtk.Fixed()

        lbl = gtk.Label("")
	btn = gtk.Button("OK")

        btn.connect("button_press_event", self.btn_pressed, self.viewed_array)

        fixed.put(lbl, 10,20)
        fixed.put(btn, 10,80)

	message_window.add(fixed)
	lbl.set_markup("<span color='#000'><b>"+self.message+"</b></span>"); 

        message_window.show_all()
        message_window.set_keep_above(True)

    def btn_pressed(self, widget, viewed_array, date):
	self.viewed_array.append(self.date)
	message_window.destroy()

    def globalform(self):

	reminderFile = path_to_txt
	fileName = open(reminderFile, 'r') 
	today = time.strftime('%Y%m%d') 
	self.today_date = time.strftime('%d.%m.%Y') 
	flag = 0
	for line in fileName: 
    	    if today in line: 
		    found_flag=0
		    for x in self.viewed_array:
			if x in line:
			    found_flag=1
		    if found_flag==0:
        		    line = line.split(';') 
        		    flag =1
			    self.message=line[1] 
			    self.date=line[0] 
			    self.show_window()

	    img = Image.new('RGB', (20, 20), color = (255, 252, 29))

	d = ImageDraw.Draw(img)
	font = ImageFont.truetype(path_to_ttf, 12)
	d.text((6,2), str("R"), fill=(0,0,0),font=font)
	img.save(path_to_png)

	self.tray.set_from_file(path_to_png) 

if __name__ == "__main__":
	SystrayIconApp()
gtk.main()