import pandas as pd
from src import FileFormatter as fileForm, fileDownload as fdw
import os
import shutil

filename = 'origin.txt'

#region Pobieranie pliku i przygotowanie go w katalogu
print("Otwieranie zautomatyzowanej przeglądarki...")
#os.chdir("../")
fileDownloader = fdw.FileDownloader(os.getcwd())
print("Pobieranie pliku...")
fileDownloader.goTo('https://s1.wcy.wat.edu.pl/ed1/')
fileDownloader.download()

os.remove(filename)
oldFileName = max([f for f in os.listdir()], key=os.path.getctime)
#shutil.move(oldFileName, os.path.join(filename))
os.rename(oldFileName, filename)
#endregion
print("Pobrano plik.")

#region Filtrowanie pól i ich zamiana
#fileChecker = fch.fileChecker(filename)
# jesli trzeba dodaj wiecej podobnych linii wg wzoru nizej
# fileChecker.replace(pattern RegEx, substitution RegEx)
#endregion
print("Przefiltrowano pola.")

print("Formatowanie pliku...")
#region Formatowanie pól wg wzorca dla kalendarza Google
original = pd.read_csv(filename, encoding="ISO-8859-1")

modified = pd.DataFrame
temp = pd.DataFrame

# wycinanie potrzebnych kolumn
modified = original.loc[:,
           ['Temat', 'Lokalizacja', 'Data rozpoczêcia', 'Czas rozpoczêcia', 'Data zakoñczenia', 'Czas zakoñczenia']]

#region Pobieranie wierszy z innego pliku planu, np. innej grupy
# moze sie przydac gdy trzeba bedzie pobierac plan z wiecej niz jednego pliku
# Y6 = Y6original.loc[:,['Temat','Lokalizacja','Data rozpoczêcia','Czas rozpoczêcia','Data zakoñczenia','Czas zakoñczenia']]
# Y6 = Y6[Y6['Temat'].str.contains("In¿ynieria oprogramowania \(L\)")]
#endregion

file_formatter = fileForm.FileFormatter(modified)

# zmiana formatu daty
column_name = "Data rozpoczêcia"
format_string = '%m/%d/%Y'
modified[column_name] = file_formatter.format_data_column(column_name, format_string)
column_name = "Data zakoñczenia"
modified[column_name] = file_formatter.format_data_column(column_name, format_string)

# zmiana formatu czasu
column_name = "Czas rozpoczêcia"
format_string = "%I:%M %p"
modified[column_name] = file_formatter.format_time_column(column_name, format_string)
column_name = "Czas zakoñczenia"
modified[column_name] = file_formatter.format_time_column(column_name, format_string)

# zmiana nazw kolumn
modified.columns = ['Subject', 'Location', 'Start date', 'Start time', 'End date', 'End time']
#endregion

#region Zapis wybranych wierszy do plików
# zapis calosci do pliku
modified.to_csv("Output_files\Wszystko.csv", index=False, encoding="ISO-8859-1")
temp = modified

# usuwanie niepotrzebnych przedmiotów
modified = temp[~temp['Subject'].str.contains("Jezyk obcy")]

# dodanie zajęć z innego pliku
# temp = temp.append(Y6, ignore_index = False)

#poczatkowa liczba wierszy w pliku przed podziałem
rows = len(temp.index)
rowsSum = 0
# filtrowanie kolumn zawierajacych (w)-wyklady i zapis do pliku
temp = modified[modified['Subject'].str.contains("\(w\)")]
temp.to_csv('Output_files\Wyklady.csv', index=False, encoding="ISO-8859-1")
rowsSum += len(temp.index)

# filtrowanie kolumn zawierajacych (c) i (L)- cwiczenia i labo i zapis do pliku
temp = modified[modified['Subject'].str.contains("\(L\)|\(c\)|\(p\)")]
temp.to_csv('Output_files\Lab_i_cw.csv', index=False, encoding="ISO-8859-1")
rowsSum += len(temp.index)

# filtrowanie kolumn zawierajacych (E)- egzaminy itp. i zapis do pliku
temp = modified[modified['Subject'].str.contains("\(E\)|\(Zp\)|\(SO\)|\(Ep\)|\(Zal\)")]
temp.to_csv('Output_files\Egzaminy_itp.csv', index=False, encoding="ISO-8859-1")
rowsSum += len(temp.index)
#endregion

# suma kontrolna wierszy
print("Zakończono formatowanie.")
if rows == rowsSum:
    print("Suma wierszy sie zgadza")
else:
    print("Brakuje wierszy")

print("Wciśnij dowolny klawisz aby zakończyć")
input()
