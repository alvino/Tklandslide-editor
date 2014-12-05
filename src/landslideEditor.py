#! /usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on 05/12/2014

@author: alvino
'''
 
from Tkinter import *
from tkFileDialog import asksaveasfilename,askopenfilename, asksaveasfile
import tkMessageBox
import subprocess
 
 
#Começa a classe do editor:
class LandslideEditor:
    str_path = ""
    # Aqui fica a função inicial:
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("LandslideEditor")# Aqui é o digito
 
        # "inicia" a scroolbar
        scrollbar = Scrollbar(self.root)
        scrollbar.pack(side=RIGHT, fill=Y)
 
        self.criar_menu()

        # Aqui adicionamos a parte que fica o texto:
        self.text = Text(self.root)
        self.text.pack(expand=YES, fill=BOTH)
 
        #aqui configura o scrollbar
        self.text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text.yview)
        
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))
        # Por Fim, a janela:
        self.root.mainloop()
        
    def novo(self):
        if self.text.get(0.0,END):
            opcao = tkMessageBox.askquestion("Novo", "Deseja apaga tudo")    
            if opcao == "yes":
                self.text.delete(0.0, END)
                self.str_path = ""
        
    def compilarHtml(self): 
        self.compilar_apresentacao(".html")
            
    def compilarPdf(self):
        self.compilar_apresentacao(".pdf")
            
    def compilar_apresentacao(self,sufixo):
        self.salvar() 
        if self.str_path:
            list_path = self.str_path.split("/")[:-1]
            list_path.append("apresentacao" + sufixo)
            source_path = "/".join(list_path)
            retorno = subprocess.check_output(('landslide %s -d %s' % (self.str_path, source_path ) ),  shell=True)
            tkMessageBox.showinfo('Gerando Slide', retorno)
    
    #markdown,slideshow,presentation,rst,,textile
    
    def salvar_arquivo(self):
        return asksaveasfilename(
                             defaultextension='.rst',
                             filetypes=[
                                        ('restructuredtext', '.rst'),
                                        ('markdown', '.md'),
                                        ('textile', '.textile')
                           ]
                )
    
 
    def salvar(self): # Aqui é a função que salva o arquivo:
        fileName = ""
        if not self.str_path:
            fileName = self.salvar_arquivo()
        else:
            fileName = self.str_path
        
        self.str_path = fileName
        self.salva_arquivo(fileName)
            
        
    
    def salvarComo(self): # Aqui é a função que salva o arquivo:
        opcao = tkMessageBox.askquestion("Salvar Como", "Deseja salvar como o arquivo: \n %s" % self.str_path)    
        if opcao == "yes":
            fileName = self.salvar_arquivo()
            self.salva_arquivo(fileName)
            self.str_path = fileName
            
    def salva_arquivo(self, fileName):
        try:
            file = open(fileName, 'w')
            file.write(self.text.get(0.0, END))
            self.root.wm_title("LandslideEditor - %s" % self.str_path )
        except:
            tkMessageBox.showerror('Erro', 'Erro ao salvar o arquivo: \n %s' % fileName )
        finally:
            file.close()    
            
 
    def abrir(self):# Aqui é a função que abre um arquivo
        fileName = askopenfilename()
        try:
            file = open(fileName, 'r')
            contents = file.read()
 
            self.text.delete(0.0, END)
            self.text.insert(0.0, contents)
            self.str_path = fileName
            self.root.wm_title("LandslideEditor - %s" % self.str_path )
        except:
            pass
        finally:
            file.close()
        
        
 
    def sobre(self):# uma pequena função "sobre" :D
        root = Tk()
        root.wm_title("Sobre")
        texto=("PyNotePad: Versão 1.0")
        textONlabel = Label(root, text=texto)
        textONlabel.pack()
        
    def criar_menu(self):
        
        menubar = Menu(self.root)
        #Aqui criamos os menus:
        MENUarquivo = Menu(menubar)
        menubar.add_cascade(label="Arquivo", menu=MENUarquivo)
        MENUarquivo.add_command(label="Novo", command=self.novo)
        MENUarquivo.add_command(label="Salvar", command=self.salvar)
        MENUarquivo.add_command(label="Salvar Como", command=self.salvarComo)
        MENUarquivo.add_command(label="Abrir", command=self.abrir)
        
        MENUlandslide = Menu(menubar)
        menubar.add_cascade(label="Landslide", menu=MENUlandslide)
        MENUlandslide.add_command(label='Gera slide html',  command= self.compilarHtml)
        MENUlandslide.add_command(label='Gera slide pdf',  command= self.compilarPdf)
        
        MENUajuda = Menu(menubar)
        menubar.add_cascade(label="Ajuda", menu=MENUajuda)
        MENUajuda.add_command(label="Sobre", command=self.sobre)
        
        self.root.config(menu=menubar)
 
# inicia o programa:
LandslideEditor()
