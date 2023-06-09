# This is the Editor. It is used by the user to create the game.
# Copyright (C) 2023 Marius Angermann
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import tkinter as tk
from tkinter import filedialog
import os
import customtkinter as ctk
from PIL import Image
import shutil
import subprocess
import sys

openfile = open("prcopen.info", "r")
readfile = openfile.readlines()
project_name = readfile[0]
openfile.close()

if project_name == "":
	sys.exit()

scenes = []








#default costumtkinter setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
ctk.set_widget_scaling(1.5)  
app = ctk.CTk()
app.geometry("1920x1080")
app.after(0, lambda:app.state('zoomed'))
app.title("Artix Engine - Project:>" + project_name)
app.iconbitmap("src/icon.ico")

def openprcmanager():
	script_dir = os.path.dirname(os.path.realpath(__file__))
	subprocess.Popen('cmd /c cd /d "{}" &'.format(script_dir), shell=True)
	subprocess.Popen('python project_manager.py', shell=True)
	sys.exit()



#adding a menubar
menu_font = ("Arial", 12)
menu_bar = tk.Menu(app, font=menu_font)
app.config(menu=menu_bar)

#adding a file menu into menubar
file_menu = tk.Menu(menu_bar, tearoff=False, font=menu_font)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New Scene")
file_menu.add_command(label="Save")
file_menu.add_command(label="Save as")
file_menu.add_command(label="Project Settings")
file_menu.add_separator()
file_menu.add_command(label="Project Manager", command=openprcmanager)
file_menu.add_command(label="Quit", command=app.quit)

#adding a edit menu into menubar
edit_menu = tk.Menu(menu_bar, tearoff=False, font=menu_font)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Paste")
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")
edit_menu.add_command(label="Editor Settings")

#adding a selection menu into menubar
selection_menu = tk.Menu(menu_bar, tearoff=False, font=menu_font)
menu_bar.add_cascade(label="Selection", menu=selection_menu)
selection_menu.add_command(label="Select all")
selection_menu.add_command(label="Clear Selection")

#Creating the file Manager
file_manager_frame = ctk.CTkFrame(app,750,230,fg_color="#172a38",border_color="#000000")
file_manager_frame.pack()
file_manager_frame.place(x=270,y=430)

file_manager_heading = ctk.CTkFrame(app,750,30,border_width=0,fg_color="#2b2b2b",border_color="#000000")
file_manager_heading.pack()
file_manager_heading.place(x=270,y=430)

file_manager_label = ctk.CTkLabel(file_manager_heading, text="File Manager", fg_color="transparent")
file_manager_label.pack()
file_manager_label.place(relwidth=1,relheight=1)
file_manager_label.lift()


class FileManager:
	def __init__(self):
		self.menu = tk.Menu(app, tearoff=0)
		self.menu.add_command(label="Delete", command=self.delete_file, font=("",15))
		self.displayed_files = []
		self.files_list = []
		self.button_file_map = {}
		self.FileLoader()

	def FileLoader(self):
		self.files_list.clear()
		openfile = open("projects/"+project_name+"/files.txt", "r")
		readfile = openfile.readlines()
		openfile.close()
		for lines in readfile:
			line = lines.rstrip("\n")
			self.files_list.append(line)

	def display_files(self):
		currentindex = 0
		self.displayed_files = []
		lastbuttonpos = []
		lastlabelpos = []
		attempts = 0
		numberinline = 0
		newline = False
		for lines in self.files_list:
			testimg = ctk.CTkImage(dark_image=Image.open("src/icons/image_icon.png"),size=(50,60))
			button = ctk.CTkButton(file_manager_frame, text="", image=testimg, width=50, height=60)
			button.bind("<Button-3>", self.open_menu)
			name_label = ctk.CTkLabel(file_manager_frame, text=lines, fg_color="transparent")
			self.button_file_map[button] = lines
			self.displayed_files.append(testimg)
			self.displayed_files.append(button)
			self.displayed_files.append(name_label)
		for objects in self.displayed_files:
			if currentindex == 3:
				currentindex = 0
				attempts += 1
				numberinline += 1
			if currentindex == 0:
				if numberinline == 7:
					numberinline = 0
					attempts = 0
					newline = True
					lastbuttonpos = [10,lastbuttonpos[1]+100]
					lastlabelpos = [2,lastlabelpos[1]+100]
				currentindex += 1
				continue
			elif currentindex == 1:
				objects.pack(padx=0,pady=30)
				if attempts == 0:
					if newline:
						objects.place(x=lastbuttonpos[0],y=lastbuttonpos[1],relwidth=0.1,relheight=0.3)
					else:
						objects.place(x=10,y=40,relwidth=0.1,relheight=0.3)
						lastbuttonpos = [10,40]
				else:
					objects.place(x=lastbuttonpos[0]+100,y=lastbuttonpos[1],relwidth=0.1,relheight=0.3)
					lastbuttonpos = [lastbuttonpos[0]+100,lastbuttonpos[1]]
			elif currentindex == 2:
				objects.pack(padx=0,pady=30)
				if attempts == 0:
					if newline:
						objects.place(x=lastlabelpos[0],y=lastlabelpos[1],relwidth=0.12,relheight=0.07)
					else:
						objects.place(x=2,y=110,relwidth=0.12,relheight=0.07)
						lastlabelpos = [2,110]
				else:
					objects.place(x=lastlabelpos[0]+100,y=lastlabelpos[1],relwidth=0.12,relheight=0.07)
					lastlabelpos = [lastlabelpos[0]+100,lastlabelpos[1]]
			currentindex += 1
	

	def update(self):
		currentindex = 0
		for objects in self.displayed_files:
			if currentindex == 3:
				currentindex = 0
			if currentindex == 0:
				currentindex += 1
				continue
			objects.destroy()
			currentindex += 1
		self.displayed_files.clear()
		self.FileLoader()
		self.display_files()

	def binddelete(self):
		currentindex = 0
		attempts = 0
		for buttons in self.displayed_files:
			if currentindex == 3:
				currentindex = 0
				attempts += 1
			if currentindex == 0:
				currentindex += 1
				continue
			if currentindex == 1:
				currentindex += 1
				continue
			currentindex += 1
	def delete_file(self, file_name):
		print("deleted file "+file_name)
		openfile = open("projects/"+project_name+"/files.txt", "r")
		readfile = openfile.readlines()
		openfile.close()
		removed = []
		for lines in readfile:
			removed.append(lines.rstrip("\n"))
		removed.remove(file_name)
		writefile = open("projects/"+project_name+"/files.txt", "w")
		for lines in removed:
			if len(removed) > 1:
				writefile.writelines(lines+"\n")
			else:
				writefile.writelines(lines)
		writefile.close()
		self.update()

	def open_menu(self, event):
		label = event.widget
		button = label.master
		file = self.button_file_map[button]
		self.menu.entryconfig(0, command=lambda: self.delete_file(file))
		self.menu.post(event.x_root, event.y_root)

	

fm = FileManager()
fm.display_files()
fm.update()





def import_file():
	filename = filedialog.askopenfilename(initialdir=os.path.expanduser("~/Documents"), title="Import File", filetypes=(("png files","*.png"),("jpeg files","*.jpg")))
	file_name = os.path.basename(filename)
	if file_name != "":
		with open("projects/"+project_name+"/files.txt", "r") as openfile:
			readfile = openfile.readlines()
			readfile.append(file_name.strip() + "\n")  
		with open("projects/"+project_name+"/files.txt", "w") as openfile:
			openfile.writelines(readfile)
		fm.update()





file_manager_button = ctk.CTkButton(file_manager_heading, text="Import", command=import_file)
file_manager_button.pack()
file_manager_button.place(relwidth=0.2,relheight=1)




def AttributesWindow():
	root = ctk.CTk()
	root.geometry("800x600")
	root.title("Attributes")
	root.iconbitmap("src/icon.ico")
	root.mainloop()

def EventSystemWindow():
	root = ctk.CTk()
	root.geometry("800x600")
	root.title("Event System")
	root.iconbitmap("src/icon.ico")
	root.mainloop()

scenetreeframe = ctk.CTkFrame(app,width=265,height=420,border_width=0,fg_color="#666666")
scenetreeframe.pack()
scenetreeframe.place(x=2,y=10)

scenetreeheading = ctk.CTkFrame(app,width=265,height=40,border_width=0,fg_color="#3d3d3d",corner_radius=0)
scenetreeheading.pack()
scenetreeheading.place(x=2,y=4)

scenenamelabel = ctk.CTkLabel(scenetreeheading,text="DefaultScene",font=("",20))
scenenamelabel.pack()
scenenamelabel.place(x=20,y=0,relheight=1,relwidth=1)

scenetreecanvas = ctk.CTkCanvas(scenetreeframe,bg="#666666",scrollregion=(0, 0, 500, 1000))
scenetreecanvas.pack()
scenetreecanvas.place(x=0,y=0,relwidth=1,relheight=1)

hbar = ctk.CTkScrollbar(scenetreeframe,button_color="#a3a3a3")
hbar.pack()
hbar.place(x=250,y=30,relheight=0.93)


scenetreecanvas.configure(yscrollcommand=hbar.set)
hbar.configure(command=scenetreecanvas.yview)

def general_update(preset="startup"):
	scenes.clear()
	print("general")
	currentindex = 0
	for i in scenetree.registeredscenes:
		scenetemp = Scene(i,link=scenes)
		scenes.append(scenetemp)
		openfile = open("projects/"+project_name+"/Scenes/"+i+".txt", "r")
		print("opened " + "projects/"+project_name+"/Scenes/"+i+".txt")
		readfile = openfile.readlines()
		print(readfile)
		openfile.close()
		for objs in readfile:
			scenes[currentindex].objects.append(scenetemp.Sprite2D(objs))
		currentindex += 1
	if preset == "startup":
		scenetree.load_scene(scenetree.registeredscenes[0])
	else:
		scenetree.load_scene(scenetree.currentscene)

	print(scenes[0].objects)

class SceneTree:
	def __init__(self,link=[],general_update=[]):
		self.menu = tk.Menu(app, tearoff=0)
		self.menu.add_command(label="Delete", command=self.delete_object, font=("",15))
		self.button_file_map = {}
		self.general_update = general_update

		self.sceneslink = link
		self.currentscene = ""
		self.displayed_objects = []
		self.registeredscenes = []
		openfile = open("projects/"+project_name+"/scenes.txt", "r")
		readfile = openfile.readlines()
		openfile.close()
		for lines in readfile:
			self.registeredscenes.append(lines.rstrip("\n"))

	def load_scene(self, name=""):
		search = 0
		self.currentscene = name
		currentscene = name
		for each in self.sceneslink:
			if each.name == name:
				search = self.sceneslink.index(each)
				self.currentsceneindex = search
				break
		scenenamelabel.configure(text=self.sceneslink[search].name)
		currentindex = 0
		lastpos = [25, 70]
		for each in self.sceneslink[search].objects:
			temp = []
			if each.type != "Camera2D":
				temp.append(each.name)
				var = temp[0].rstrip("\n")
			if each.type == "Camera2D":
				button = ctk.CTkButton(scenetreecanvas, text=each.type, font=("", 15), fg_color="#252626")
			else:
				button = ctk.CTkButton(scenetreecanvas, text=var, font=("", 15), fg_color="#252626")

			if each.type != "Camera2D":
				button.bind("<Button-3>", self.open_menu)
				self.button_file_map[button] = var
			self.displayed_objects.append(button)
			

			if currentindex == 0:
				button_width = int(scenetreecanvas.winfo_width() * 0.8)
				button_height = int(scenetreecanvas.winfo_height() * 0.1)
				button_window = scenetreecanvas.create_window(lastpos[0], lastpos[1], anchor="nw", width=button_width, height=button_height, window=button)
			else:
				button_width = int(scenetreecanvas.winfo_width() * 0.8)
				button_height = int(scenetreecanvas.winfo_height() * 0.1)
				button_window = scenetreecanvas.create_window(lastpos[0], lastpos[1] + 80, anchor="nw", width=button_width, height=button_height, window=button)
			if currentindex != 0:
				lastpos = [lastpos[0], lastpos[1] + 80]
			currentindex += 1
		canvas_width = scenetreecanvas.winfo_width()
		canvas_height = lastpos[1] + 60
		scenetreecanvas.configure(scrollregion=(0, 0, canvas_width, canvas_height))




	def update(self):
		print("updated")
		for objects in self.displayed_objects:
			objects.destroy()
			print("destroyed")
		self.displayed_objects.clear()
		self.load_scene(self.currentscene)
		
		

	def delete_object(self, objectname=""): #objectname is for example player\n
		for scenes in self.sceneslink:
			print("another")
			if scenes.name == self.currentscene:
				for objs in scenes.objects:
					if objs.type != "Camera2D":
						if objs.name == objectname or objs.name == objectname+"\n":
							print(objs.name)
							print("removed")
							scenes.objects.remove(objs)
							break

		openfile = open("projects/"+project_name+"/Scenes/"+self.currentscene+".txt", "r")
		readfile = openfile.readlines()
		openfile.close()
		exlist = []
		exlist.append(objectname)
		readfile.remove(exlist[0].rstrip("\n")+"\n")

		writefile = open("projects/"+project_name+"/Scenes/"+self.currentscene+".txt", "w")
		for lines in readfile:
			writefile.writelines(lines)
		writefile.close()
		self.update()
		


	def open_menu(self, event):
		label = event.widget
		button = label.master
		objects = self.button_file_map[button]
		self.menu.entryconfig(0, command=lambda: self.delete_object(objects))
		self.menu.post(event.x_root, event.y_root)

	

scenetree = SceneTree(link=scenes,general_update=general_update)


class Scene:
	def __init__(self,name="untitled",link=[]):
		self.name = name
		self.link = link
		self.objects = []
		camera = self.Camera2D()
		self.objects.append(camera)
	def add_object(self, type="", name=""):
		if type == "Sprite2D":
			self.objects.append(self.Sprite2D(name=name))
		scenetree.update()
	class Camera2D:
		def __init__(self):
			self.pos = [0,0]
			self.type = "Camera2D"
	class Sprite2D:
		def __init__(self, name="Untitled"):
			self.name = name
			self.type = "" 


def add_sprite():
	dialog = ctk.CTkInputDialog(text="Sprite Name:", title="Create Sprite")
	value = dialog.get_input()
	currentindex = 0
	for i in scenes:
		if scenetree.currentscene == i.name:
			break
		currentindex += 1
	if value != "":
		openfile = open("projects/"+project_name+"/Scenes/"+scenes[currentindex].name+".txt", "r")
		readfile = openfile.readlines()
		openfile.close()
		objectstemp = []
		for objs in readfile:
			objectstemp.append(objs.rstrip("\n"))
		objectstemp.append(value)
		writefile = open("projects/"+project_name+"/Scenes/"+scenes[currentindex].name+".txt", "w")
		for i in objectstemp:
			writefile.writelines(i+"\n")
		scenes[scenetree.currentsceneindex].objects.append(Scene.Sprite2D(value))
	scenetree.update()





def add_menu(event):
	addmenu.post(addbutton.winfo_rootx(), addbutton.winfo_rooty() + addbutton.winfo_height())

addbutton = ctk.CTkButton(scenetreeheading, text="+", fg_color="#5f9467", font=("",20))
addbutton.pack()
addbutton.place(x=5,y=5,relwidth=0.2,relheight=0.7)

addmenu = tk.Menu(app, tearoff=0)
addmenu.add_command(label="Sprite",font=("",15),command=add_sprite)

addbutton.bind("<Button-1>", add_menu)

properties_panel_frame = ctk.CTkFrame(app,width=255,height=655,border_width=0,fg_color="#666666",corner_radius=0)
properties_panel_frame.pack()
properties_panel_frame.place(x=1022,y=4)

properties_panel_heading = ctk.CTkFrame(app,width=255,height=40,border_width=0,fg_color="#3d3d3d",corner_radius=0)
properties_panel_heading.pack()
properties_panel_heading.place(x=1022,y=4)

properties_panel_canvas = ctk.CTkCanvas(properties_panel_frame,bg="#666666")
properties_panel_canvas.pack()
properties_panel_canvas.place(x=0,y=0,relwidth=1,relheight=1)

properties_panel_label = ctk.CTkLabel(properties_panel_heading,text="Properties",font=("",20))
properties_panel_label.pack()
properties_panel_label.place(relwidth=1,relheight=1)








viewport = ctk.CTkCanvas(app,width=1100,height=630)
viewport.pack()
viewport.place(x=415,y=5)

event_system_button = ctk.CTkButton(viewport,text="Event System",corner_radius=0, fg_color="#5f6670", font=("",20),command=EventSystemWindow)
event_system_button.pack()
event_system_button.place(x=0,y=0,relwidth=0.2,relheight=0.1)

attributes_button = ctk.CTkButton(viewport,text="Attributes",corner_radius=0, fg_color="#5f6670", font=("",20),command=AttributesWindow)
attributes_button.pack()
attributes_button.place(x=150,y=0,relwidth=0.2,relheight=0.1)

viewporttools = ctk.CTkSegmentedButton(viewport,values=["Move","Scale","Rotate"])
viewporttools.pack()
viewporttools.place(x=0,y=45)


class Viewport:
	def __init__(self):
		pass






general_update("startup")


app.mainloop()

print("press enter to quit> ")