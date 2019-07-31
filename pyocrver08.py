# -*- coding: utf-8 -*-
"""
Programa Livre desenvolvido por Gabriel Caritá

gabrielcarita@gmail.com

"""
import cv2
import numpy as np
import pytesseract
from PIL import *
import PIL
from pytesseract import image_to_string
import os, subprocess
import time

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
TESSDATA_PREFIX = 'C:/Program Files/Tesseract-OCR'



pdftoppm_path = r"C:\Program Files\poppler-0.68.0\bin\pdftoppm.exe"

#def pdftoimage():  
	#path = os.path.dirname(root.filename)
#	global basename
#	basename = os.path.basename(root.filename)
#	
#	print(basename)
#	pdf_dir = r"%s" % (os.path.dirname(root.filename))
#	print(pdf_dir)
#	os.chdir(pdf_dir)
#	for pdf_file in os.listdir(pdf_dir):
#		if pdf_file.endswith(str(basename)):
#			subprocess.Popen('"%s" -jpeg %s out' % (pdftoppm_path, pdf_file))
			#s = "Passo 1 Completo"
#	text.delete(0,END)
#	text.insert(0,"Descompactar OK!")

def imgread():
	#path = os.path.dirname(root.filename)
	global basename
	basename = os.path.basename(root.filename)
	
	print(basename)
	pdf_dir = r"%s" % (os.path.dirname(root.filename))
	print(pdf_dir)
	os.chdir(pdf_dir)
	for pdf_file in os.listdir(pdf_dir):
		if pdf_file.endswith(str(basename)):
			subprocess.Popen('"%s" -jpeg %s out' % (pdftoppm_path, pdf_file))
			#s = "Passo 1 Completo"
	text.delete(0,END)
	text.insert(0,"Descompactar OK!")
	time.sleep(1)
	text.delete(0,END)
	text.insert(0,"Realizando Leitura!")
	try:
		num = numbpages()
	except:
		messagebox.showinfo("Erro", "Leitura incorreta!")
	else:
		for i in range(1,num+1):
			if num < 1000 :
				f = ('{0:0>3}'.format(i))
			if num < 100 :
				f = ('{0:0>2}'.format(i))
			if num < 10 :
				f = ('{0:0>1}'.format(i))
			#print(f)
			text.delete(0,END)
			text.insert(0,"Lendo Página %s !" % (i))
			global percent
			percent = (i/(num))*100
			progressbar["value"] = percent
			progressbar.update()
			# tipando a leitura para os canais de ordem RGB
			try:
				imagem = PIL.Image.open('out-' + str(f) +'.jpg').convert('RGB')
			except:
				messagebox.showinfo("Erro", "Número de Páginas Incorreto! Confira o Número de Páginas do PDF!")
			else:
				# convertendo em um array editável de numpy[x, y, CANALS]
				npimagem = np.asarray(imagem).astype(np.uint8)  
				# diminuição dos ruidos antes da binarização
				npimagem[:, :, 0] = 0 # zerando o canal R (RED)
				npimagem[:, :, 2] = 0 # zerando o canal B (BLUE)
				# atribuição em escala de cinza
				im = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY) 
				# aplicação da truncagem binária para a intensidade
				# pixels de intensidade de cor abaixo de 127 serão convertidos para 0 (PRETO)
				# pixels de intensidade de cor acima de 127 serão convertidos para 255 (BRANCO)
				# A atrubição do THRESH_OTSU incrementa uma análise inteligente dos nivels de truncagem
				ret, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) 

				# reconvertendo o retorno do threshold em um objeto do tipo PIL.Image
				binimagem = PIL.Image.fromarray(thresh) 

				# chamada ao tesseract OCR por meio de seu wrapper
				
				x = str(basename [:-4])
				
				# impressão do resultado
				pagina_fim = '\n-------------------------------Fim Folha ' + str(i) + '-------------------------------\n\n'
				pagina_in = '\n-------------------------------Início Folha ' + str(i) + '-------------------------------\n\n'
				pdf = pytesseract.image_to_pdf_or_hocr('out-' + str(f) +'.jpg',lang="por+eng", config='', nice=0,extension='pdf' )
				openpdf = open('%s%s.pdf' % (x,str(i)) , 'w+b')
				openpdf.write(bytearray(pdf))
				j ='out-' + str(f) +'.jpg'
				os.remove(j)
				openpdf.close()
			text.delete(0,END)
			text.insert(0,"Leitura Finalizada Com Sucesso")
		messagebox.showinfo("Pronto", "Leitura Realizada Com Sucesso")
		merging()
	
    
    
    
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter.ttk import Progressbar
from tkinter import messagebox

root = Tk()

root.title("PyOCR - v0.8")

def browsefunc():
	root.filename = filedialog.askopenfilename(initialdir = "./", title = "Escolha a Pasta",filetypes=[('pdf files', '.pdf')])
	pathlabel.config(text=root.filename)
	text.delete(0,END)
	text.insert(0,"Arquivo Selecionado Com Sucesso")
	
 

 
#def run_1():
#	pdftoimage()
def run_2():
	imgread()
text = Entry(root, bd=1,width =48)
text.pack()

	
	
def merging():
	from PyPDF2 import PdfFileMerger
	pdfs = []
	num = numbpages()
	x = str(basename [:-4])
	for i in range(1 ,num+1):
		f = str(x) + str(i) + '.pdf'
		pdfs.append(f)

	
	merger = PdfFileMerger()

	for pdf in pdfs:
		merger.append(pdf)

	merger.write("%sfinal.pdf" %(x))
	merger.close()
	for i in range(1 , num+1):
		f = str(x) + str(i) + '.pdf'
		os.remove(f)
	
def numbpages():
	from PyPDF2 import PdfFileReader
	x = str(basename [:-4])
	pdf = PdfFileReader(open(str(x) + '.pdf','rb'))
	numero = pdf.getNumPages()
	return numero


### função browsebutton buscar arquivos na pasta!
browsebutton = Button(root, text="Escolher a Pasta", command=browsefunc)
browsebutton.pack()

### mostrar a pasta que está sendo executada
pathlabel = Label(root)
pathlabel.pack()


### botão de início
Start_read = Button(root, text="Iniciar Leitura", command=run_2)
Start_read.pack()


## progressbar
percent = 0
progressbar = Progressbar(root, orient="horizontal" , length = 200, mode = "determinate")
progressbar.pack()
progressbar["maximum"] = 100


### instruções para o usuário
help = Label(text="Instruções de uso : \n 1 - Selecione o arquivo a ser escaneado. \n 2 - Clique em 'Iniciar Leitura' e aguarde. ", fg = "red")
help.pack()


root.iconbitmap('pyocr.ico')

root.mainloop()

