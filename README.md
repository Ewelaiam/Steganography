# Steganography

1. Temat projektu

Zadaniem jest napisanie dwóch skryptów, jeden, który ukrywa dane (może być zwykły tekst) w pliku .zip i/lub .rar, i drugi, który te dane przywraca. Pliki nie powinny być wykrywane przez Windows Defendera jako szkodliwe. Do projektu trzeba dołączyć dokumentację wyjaśniającą jak i co zostało zrobione. Można się wspierać: https://github.com/gromnitsky/zipography .

2. Budowa pliku ZIP

ZIP to jeden z najczęściej używanych formatów kompresji bezstratnej i archiwizacji danych na platformie PC.

Archiwum ZIP składa się z:
* lokalnych nagłówków plików,
* lokalnych plików,
* katalogu centralnego (na końcu pliku Zip)

Aplikacja zip (taka jak np. WinZip lub FilZip) rozpoczyna od odczytania katalogu centralnego. Po wyodrębnieniu pliku, odczytane zostanie przesunięcie z wpisu w katalogu. Następnie plik lokalny zostanie odczytany i nieskompresowany.

Ważne jest, aby plik były w katalogu centralnym, ponieważ jeśli nie jest, to nie będzie wymieniony w aplikacji Zip.

3. Steganografia dla plików ZIP

Steganografia jest techniką ukrywania informacji w innych danych tak, aby obserwatorzy nie byli świadomi istnienia ukrytej wiadomości. Jest to często używane narzędzie w celu ochrony poufności danych.

Projekt skupia się na steganografii plików zip. Istnieją różne podejścia do realizacji projektu:
* Wstawienie pliku przed pierwszym nagłówkiem katalogu centralnego i zmiana wskaźnika w końcu katalogu centralnego tak, aby wskazywał na początek katalogu centralnego.
* Wstawienie pliku w dowolnym miejscu, wraz z brakiem informacji w katalogu centralnym

Projekt został zrealizowany zgodnie z podejściem w podpunkcie 1. 

4. Realizacja

Program został zaimplementowany w języku Python. Składa się z 3 plików py.

eocd.py

Klasa ta przechowuje i wyświetla informacje o strukturze katalogu centralnego z archiwum ZIP, zawartych w bloku End of Central Directory (EOCD).
* eocd
Tablica bajtów zawierająca dane bloku EOCD.
* eocd_pos
Pozycja w pliku, gdzie zaczyna się blok EOCD.
* self.total_num_of_cd_records
Liczba całkowita reprezentująca łączną liczbę rekordów central directory, wyciągnięta z 11. i 12. bajtu bloku EOCD.
* self.size_of_cd
Liczba całkowita reprezentująca rozmiar central directory w bajtach, wyciągnięta z bajtów od 13 do 16 bloku EOCD.
* self.offset_of_cd
Liczba całkowita reprezentująca przesunięcie, od początku archiwum ZIP, do początku central directory, wyciągnięta z bajtów od 17 do 20 bloku EOCD.

Dodatkowo posiada metodę print_EOCD_info, która wypisuje powyższe informację na dany moment.

Informację o danych przechowywanych na wybranych pozycjach bloków EOCD przypisano na podstawie tabeli https://en.wikipedia.org/wiki/ZIP_(file_format).

inject.py

Skrypt, który odpowiada za odczytanie argumentów wejściowych, pobraniu rekordu EOCD z pliku ZIP, a następnie ukryciu tajnego pliku w nowym pliku ZIP. Modyfikuje on bajty tajnego pliku, zapisuje jego długość, kopiuje nagłówki centralnego katalogu. Aktualizuje offset centralnego katalogu w nagłówku EOCD, i zapisuje wszystko w wyjściowym pliku ZIP.

extract.py

Ten skrypt odczytuje argumenty wejściowe, pobiera rekord EOCD z pliku ZIP i wyodrębnia ukryty plik z pliku ZIP. Odczytuje długość tajnego pliku, kopiuje jego zawartość, usuwa przesunięcie bajtowe z każdego bajtu i zapisuje wynikowy plik w określonym miejscu docelowym (domyślnie output.txt).

common.py
Plik pomocniczy do lokalizowania i tworzenia obiektu "End of Central Directory" (EOCD) w pliku ZIP.

parser.py

Plik pomocniczy pozwalający na przyjmowanie parametrów wejściowych z poziomu konfiguracji dla skryptu inject.py oraz extract.py

 5. Testy

Do przeprowadzenia testów przygotowano:
* folder z plikiem tekstowym, który skompresowano do formatu .zip

<img width="854" alt="Screenshot 2024-08-29 at 21 21 01" src="https://github.com/user-attachments/assets/55678ed5-212a-42db-a864-705283de4eeb">

* plik tekstowy z tajna wiadomością, który ma być “schowany” w utworzonym wcześniej folderze zip w sposób niewidoczny.

<img width="856" alt="Screenshot 2024-08-29 at 21 21 22" src="https://github.com/user-attachments/assets/431cc13a-281e-4167-b8e4-74a9c9400f67">


Na początku wywołano skrypt inject.py z zip_file.zip oraz secret_file.txt jako parametrami wejściowymi. Jako wynik utworzył plik output.zip.

<img width="856" alt="Screenshot 2024-08-29 at 21 21 44" src="https://github.com/user-attachments/assets/b7e825d5-7328-4342-928c-9fd411ea539c">

Po rozpakowaniu folderu output.zip, widoczny jest tylko plik randomfile.txt, bez secret_file.txt

<img width="854" alt="Screenshot 2024-08-29 at 21 22 10" src="https://github.com/user-attachments/assets/822ff21a-ae56-40c7-ab46-1e7187e2a849">

Jednak rozpakowanie folderu output.zip za pomocą skryptu extract.py, wydobyło ukrytą wiadomość i umieściło ją w pliku wynikowym output.txt

<img width="858" alt="Screenshot 2024-08-29 at 21 22 40" src="https://github.com/user-attachments/assets/f746bd29-66f9-4689-af35-7e0aedd89aa8">

Przy wykonywaniu operacji inject i extract, pliki nie były uważane za szkodliwe - caly proces przebiegł bez żadnych błędów czy ostrzeżeń.
Po otworzeniu obu folderów ZIP w edytorze tekstowym, można zauważyć, że w surowych danych binarnych folder output.zip przechowuje zaszyfrowaną wiadomość tekstową.

<img width="823" alt="Screenshot 2024-08-29 at 21 23 08" src="https://github.com/user-attachments/assets/3c2f6feb-a13f-40e2-bc0e-65936c1c4fa4">

<img width="844" alt="Screenshot 2024-08-29 at 21 23 21" src="https://github.com/user-attachments/assets/279e45c1-30a8-41b9-8534-aeb1bb5759a9">

Dodatkowo przeprowadzono zaproponowany przez prowadzącego test przesłania folderu ZIP pocztą i zbadania zachowania po tej operacji. Komunikacja pocztowa nie zmieniła formatu - po rozpakowaniu otrzymanego folderu ZIP, wiadomość tekstowa była niewidoczna, lecz w edytorze tekstowym można ją wychwycić.

6. Wnioski

Zadanie pokazało, że ukrywanie danych w plikach archiwów ZIP/RAR jest praktyczną i działającą metodą, szczególnie jeśli nie zawiera szkodliwego oprogramowania, co zmniejsza ryzyko wykrycia przez narzędzia antywirusowe. Proces ten jest relatywnie prosty do wdrożenia i użytkowania, pod warunkiem odpowiedniego zabezpieczenia danych.

7. Bibliografia

Wikipedia ZIP:

https://en.wikipedia.org/wiki/ZIP_(file_format)

Alternatywne podejście niż zaprezentowane w projekcie do steganografii plików skompresowanych

https://www.codeproject.com/Articles/13808/Steganography-16-Hiding-additional-files-in-a-ZIP
  
