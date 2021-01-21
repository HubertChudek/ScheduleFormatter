import pandas as pd
import fileChecker as fch, fileDownload as fdw
import os
import shutil

filename = 'origin.txt'

print("Otwieranie zautomatyzowanej przeglądarki...")
fileDownloader = fdw.FileDownloader()
print("Pobieranie pliku...")
fileDownloader.goTo('https://s1.wcy.wat.edu.pl/ed1/')
fileDownloader.download()

os.remove(filename)
oldFileName = max([f for f in os.listdir()], key=os.path.getctime)
shutil.move(oldFileName, os.path.join(filename))

print("Pobrano plik.")

fileChecker = fch.fileChecker(filename)
# jesli trzeba dodaj wiecej podobnych linii wg wzoru nizej
# fileChecker.replace(pattern RegEx, substitution RegEx)
print("Filtrowanie pliku pod kątem pól powodującyh problemy...")

print("Formatowanie pliku...")
original = pd.read_csv(filename, encoding="ISO-8859-1")

modified = pd.DataFrame
temp = pd.DataFrame

# wycinanie potrzebnych kolumn
modified = original.loc[:,
           ['Temat', 'Lokalizacja', 'Data rozpoczêcia', 'Czas rozpoczêcia', 'Data zakoñczenia', 'Czas zakoñczenia']]

# moze sie przydac gdy trzeba bedzie pobierac plan z wiecej niz jednego pliku
# Y6 = Y6original.loc[:,['Temat','Lokalizacja','Data rozpoczêcia','Czas rozpoczêcia','Data zakoñczenia','Czas zakoñczenia']]
# Y6 = Y6[Y6['Temat'].str.contains("In¿ynieria oprogramowania \(L\)")]

# zmiana formatu daty
temp = modified['Data rozpoczêcia'].astype(str)
temp = pd.to_datetime(temp).apply(lambda x: x.strftime('%m/%d/%Y'))
modified['Data rozpoczêcia'] = temp
temp = modified['Data zakoñczenia'].astype(str)
temp = pd.to_datetime(temp).apply(lambda x: x.strftime('%m/%d/%Y'))
modified['Data zakoñczenia'] = temp

# zmiana formatu czasu
temp = pd.to_datetime(modified['Czas rozpoczêcia'])
modified['Czas rozpoczêcia'] = temp.dt.strftime('%I:%M %p')
temp = pd.to_datetime(modified['Czas zakoñczenia'])
modified['Czas zakoñczenia'] = temp.dt.strftime('%I:%M %p')

# zmiana nazw kolumn
modified.columns = ['Subject', 'Location', 'Start date', 'Start time', 'End date', 'End time']

# ---------------Y6------------------------------do usunięcia potem
# temp = Y6['Data rozpoczêcia'].astype(str)
# temp = pd.to_datetime(temp).apply(lambda x:x.strftime('%m/%d/%Y'))
# Y6['Data rozpoczêcia'] = temp
# temp = Y6['Data zakoñczenia'].astype(str)
# temp = pd.to_datetime(temp).apply(lambda x:x.strftime('%m/%d/%Y'))
# Y6['Data zakoñczenia'] = temp
# print(Y6)
#
# temp = pd.to_datetime(Y6['Czas rozpoczêcia'])
# Y6['Czas rozpoczêcia'] = temp.dt.strftime('%I:%M %p')
# temp = pd.to_datetime(Y6['Czas zakoñczenia'])
# Y6['Czas zakoñczenia'] = temp.dt.strftime('%I:%M %p')
#
# Y6.columns = ['Subject','Location','Start date','Start time','End date','End time']
# ---------------Y6------------------------------

# zapis calosci do pliku
modified.to_csv("Output_files\Wszystko.csv", index=False, encoding="ISO-8859-1")
temp = modified

# usuwanie niepotrzebnych przedmiotów
temp = temp[~temp['Subject'].str.contains("Jêzyk obcy")]
modified = temp
# temp = temp.append(Y6, ignore_index = False)
# dodanie zajęć z innego pliku

rows = len(temp.index)
rowsSum = 0
# filtrowanie kolumn zawierajacych (w)-wyklady i zapis do pliku
temp = modified[modified['Subject'].str.contains("\(w\)")]
temp.to_csv('Output_files\Wyklady.csv', index=False, encoding="ISO-8859-1")
rowsSum += len(temp.index)

# filtrowanie kolumn zawierajacych (ć) i (L)- cwiczenia i labo i zapis do pliku
temp = modified[modified['Subject'].str.contains("\(L\)|\(c\)|\(p\)")]
temp.to_csv('Output_files\Lab_i_cw.csv', index=False, encoding="ISO-8859-1")
rowsSum += len(temp.index)

# filtrowanie kolumn zawierajacych (E)- egzaminy itp. i zapis do pliku
temp = modified[modified['Subject'].str.contains("\(E\)|\(Zp\)|\(SO\)|\(Ep\)|\(Zal\)")]
temp.to_csv('Output_files\Egzaminy_itp.csv', index=False, encoding="ISO-8859-1")
rowsSum += len(temp.index)

# suma kontrolna wierszy
print("Zakończono formatowanie.")
if rows == rowsSum:
    print("Suma wierszy sie zgadza")
else:
    print("Brakuje wierszy")

print("Wciśnij dowolny klawisz aby zakończyć")
input()
