# Eksploracja danych #
autorzy: Andrzej Burban, Agnieszka Job
# Algorytm do wyszukiwania końca linii w reflektogramach optycznych #

#### Cel projektu

Celem projektu było stworzenie algorytmu do wykrywania końca linii światłowodowej na podstawie pomiaru wykonanego reflektometrycznym. Tworzony algorytm byłby wykorzystywany w systemie monitoringu pasywnego opartego o pomiary włókien światłowodowych.
Przed algorytmem było postawione kilka istotnych wymagań odnośnie jego wydajności oraz skuteczności działania:
- Szybkość działania działania maksymalnie 1 sekunda, optymalnie poniżej 0.5 sekundy
- Możliwość pracy wyłącznie w oparciu o jeden rdzeń procesora (wynika ze struktury sprzętowej platformy docelowej)
- Powtarzalność wyników dla pomiarów różniących się wyłącznie na poziomie szumu optycznego(nawet jeśli wynik jest błędny to musi być powtarzalny)

Algorytm ma zwracać jedną liczbę typu całkowitoliczbowego oznaczającą wartość końca linii. Dla przypadków linii krótkich(<4000 m) ma zwrócić wartość 4000

#### Generowanie danych

Danymi używanymi do prac nad algorytmem były zrzuty baz danych powstające w trakcie prac R&D nad systemem monitoringu pasywnego w firmie FCA. Pierwotnym przeznaczeniem baz nie było zbieranie danych do dalszych analiz, lecz backup w przypadku awarii sprzętu lub w celu szybkiego wypełnienia nowej jednostki testowej jakimikolwiek danymi. Przez to dane cechowały się posiadaniem niespójności w strukturze bazy danych. Dodatkowo bazy pochodzą z różnych stadiów rozwoju systemu(w tym algorytmów przetwarzających surowe odczyty z układu reflektometrycznego), co powoduje że pomiary wykonane w różnym czasie mogą mieć różny charakter oraz być istotnie różne od pomiarów wykonywanych przez docelową konfigurację systemu.
Dlatego dane należało poddać obróbce o oczyszczeniu w celu posiadania unikalnych i możliwie najbardziej zbliżonych danych do tych na których będzie działał algorytm.

#### Dane surowe

Pierwszym etapem prac polegającym na zaprowadzeniu porządku pomiędzy wieloma zrzutami bazy danych było połączenie ich w jedną, nową dużą bazę danych. W tym kroku każdy pomiar uzyskał nowy unikalny identyfikator aby pomiary się na siebie nie nakładały. Dodatkowo podczas łączenia baz udało się wyeliminować pomiary które miały w jakikolwiek sposób niespójny opis w bazie danych. W celu przeprowadzenia tej procedury stworzony został skrypt w języku Python, który przepisywał każdy pomiar do nowej bazy danych. Cały proces migracji baz trwał około 30 godzin.
Po wykonaniu tego zadania posiadaliśmy już dane, które były poprawne technicznie lecz w dalszym ciągu wymagały obróbki i czyszczenia aby uzyskać dobry i poprawy zbiór danych do tworzenia i testowania tworzonego algorytmu.

#### Dane poprawne technicznie

W posiadanych danych istniały zasadniczo dwa rodzaje pomiarów:
- z długością impulsu pomiarowego 1000 ns
- z długością impulsu pomiarowego 20000 ns

Każda z długości impulsu wymaga odrębnego algorytmu, gdyż istotnie różni się charakter pomiaru reflektometrycznego.
Do dalszej pracy wybraliśmy dane z impulsem o długości 20000 ns. Wybór był spowodowany głównie tym iż jest to dużo częściej stosowany impuls w praktycznych implementacjach systemu, dla którego jest opracowywany algorytm.
Spośród pomiarów o zadanych impulsie istniały pomiary o różnych docelowych długościach linii pomiarowej. Dla systemu ostatecznie wybrana została długość 120 km i tylko pomiary o tej długości zostały zakwalifikowanego do dalszej pracy.

#### Czyszczenie danych

Czyszczenie danych rozpoczęło się od usunięcia danych nie spełniających założeń opisanych w poprzednim akapicie. Po wykonaniu tej operacji nastąpił etap usuwania zduplikowanych pomiarów oraz pomiarów zawierających błędy, bądź w widoczny sposób odbiegających swoim charakterem od pomiarów z charakterystyką docelowej platformy sprzętowej.
Do wykonania tego zadania wykorzystane zostało narzędzie do wizualizacji wykresów, pochodzące z docelowego produktu(w uproszczonej formie).
Prace czyszczące były wykonywane ręcznie poprzez znalezienie pojedynczych(lub całych zakresów) pomiarów, które nie nadawały się do dalszej obróbki, i usuwanie ich z bazy danych. Zadanie to zajęło około 10 godzin.
Po wykonaniu tego zadania ostatecznie pozostało 126 pomiarów, które nadawały się do opracowania i testowania algorytmu. Początkowa liczba pomiarów wynosiła blisko 2000.

#### Analiza danych

Proces analizy oczyszczonych danych został rozpoczęty od sprawdzenia jak zmieniają się niektóre statystyki i/lub wielkości dla różnych fragmentów reflektogramu. Były one badane średnią kroczącą, wariancją odcinkową, odcinkowym linearyzowaniem oraz obliczaniem współczynników autokorelacji. Ze wszystkich wymienionych metod(oraz ich różnych modyfikacji) jedynym, który wykazywał wysoką użyteczność do wykrywania końca linii w reflektogramie optycznym była wariancja odcinkowa. Szum występujący w reflektogramie poza badanym torem optycznym wykazywał się bardzo wysoką wartością wariancji w stosunku do reszty toru optycznego. Pozostałymi jeszcze miejscami o wysokiej wariancji były miejsca charakteryzujace sie występowaniem zjawisk optycznych(odbicia Fresnela). Jednak z analizy różnych reflektogramów zauważono że szum nie ma wartości powyżej 12 decybeli. Wynikło z tego iż początek szumu znajduje się zawsze poniżej wartości 12 decyle(właściwie najczęściej poniżej 10dB). Również poniżej tej wartości nigdy nie występują inne zjawiska optyczne o wysokiej wariancji. Dlatego dla celów algorytmu zdecydowaliśmy o wycięciu wartości większych od 12dB. Zostały one zamienione na wartość 12dB. Dzięki temu pierwszą wartością która miała wyraźnie niezerową wartość wariancji był początek szumu za torem optycznym. Zauważono również że zawsze na początku występowała bardzo wysoka szpilka wariancji, której należało się pozbyć. Była to szpilka wynikająca z istnienia na wykresie silnie opadającego zbocza strefy martwej reflektometru. Aby go wyeliminować zamieniono wartość wyszystkich punktów powyżej średniej wartości na wartość mediany. Cechą charakterystyczną reflektometru dla którego opracowywany jest algorytm jest szerokość strefy martwej, która wynosi 3,2 km. Wynika z tego iż znaleziony punkt, w początku wysokiej wariancji jest tak naprawdę oddalony od faktycznego punktu końca linii o 3,2 km. Również podczas testów zauważono iż nie należy uznawać pierwszego punktu o niezerowej wariancji jako punktu końca linii lecz dopiero punkt wykazujący się wartością wyraźnie wyższą od zera. Po przeglądnięciu wykresów wariancji dla wielu różnych przykładów uznano empirycznie iż dobrą wartością jest co najmniej ćwierć wartości maksymalnej wariancji na linii optycznej.
Z przeprowadzonej analizy utworzony został następujący algorytm detekcji końca linii:
- Wartości >12dB zamień na wartość 12dB
- Obliczyć wariancję dla odcinków szerokości 10 próbek i zamienić wartość tych próbek na wartość obliczonej wariancji
- Zamień szpilki wariancji na wartość mediany wariancji
- Znajdź maksymalną wartość wariancji
- Znajdź pierwszy punkt większy niż 0.25*max(wariancja)
- Od znalezionego punktu odjąć wartość 3200 i to jest wynik końcowy algorytmu

Poniżej przedstawiony zostanie krok po kroku przebieg algorytmu dla przykładowego pomiaru.

Jest to pomiar dla którego koniec linii optycznej znajduje się w punkcie 21090 metrów.
Oryginalny wygląd pomiaru:
![Original image](/ed_original.png)

Pomiar po usunięciu wartośći >12dB:
![Original image](/ed_12db.png)

Pomiar po obliczeniu wariancji:
![Original image](/ed_wariancja_high.png)

Wariancja po usunięciu szpilek wariancji:
![Original image](/ed_wariancja.png)

Zwrócony wynik przez algorytm: 20095
Różnica między wynikiem zwróconym a faktycznym końcem linii jest mniejsza niż 1200 więc wynik jest poprawny.

Stworzony algorytm został następnie poddany testom w celu sprawdzenia go na różnych zestawach próbek.

#### Testy

Do testów algorytmu wybranych zostało 48 pomiarów. Zostały one zgrupowane w 4 zbiory każdy po 12 pomiarów. 1 ze zbiorów został potraktowany jako zbiór uczący a 3 pozostałe jako zbiory testowe. Zbiór uczący został wybrany “manualnie” przez człowieka jako zbiór najbardziej reprezentatywnych i różnych przypadków testowych. Jeden zbiór testowy został również wybrany ręcznie aby mieć podobny charakter do zbioru uczącego. Pozostałe dwa zbiory zostały wylosowane.
W poniższej tabeli znajdują się wyniki skuteczności algorytmu dla każdej z grup testowych. Za wynik poprawny uznany był taki gdzie znaleziony koniec linie znajdował się maksymalnie 1200 metrów od prawdziwego końca linii. Wartość ta pochodzi została uznana za wystarczającą dokładność przez zespół R&D w firmie FCA.

| Grupa  | Skuteczność  |
|---|---|
| Ucząca  |  75% |
|  Test 1 |  58% |
|  Test 2 | 50%  |
|  Test 3 | 50%  |
| średnia  | 58,25%  |

Z powyższych wyników widać że algorytm nie cechuje się wysoką skutecznością. Należy wziąć jednak pod uwagę że w zbiorze 126 pomiarów znajduje się wyjątkowo dużo pomiarów bardzo nietypowych i rzadko występujących w rzeczywistych sytuacjach. Natomiast w przypadkach “typowych” algorytm wykazuje się skutecznością około 90%. Dodatkowo testy pokazały że dla przypadków różniących się wyłącznie szumem algorytm wykazywał się całkowitą powtarzalnością wyników.
Dodatkowo podczas analizy wyników błędnych zauważono iż większość z tych pomiarów znacznie różniła się charakterem szumu poza torem pomiarowym, który to szum był istotnym elementem działania algorytmu. Jest to spowodowane tym iż wyniki pomiarów pochodzą z różnego etapu prac nad systemem i również algorytmy obróbki surowych danych reflektometrycznych ulegały zmianom.


#### Podsumowanie

Z przeprowadzonych testów wynika że na obecnym poziomie dojrzałości algorytmu nie jest on jeszcze gotowy aby mógł zostać użyty w finalnej wersji produktu. Może on zostać użyty jako narzędzie służące jako heurystyka wyznaczania końca linii, gdyż jego dokładność pozwala bardzo mocno ograniczyć przedział poszukiwań. W tym przedziale mógłby działać algorytm dotychczas stworzony przez firmę FCA, który jest skuteczny lecz działa bardzo wolno(2 sekundy) dla całego reflektogramu. Wiadomo natomiast iż w przypadku działania na krótkim przedziale jest on  odpowiednio szybki aby sprostać wymaganiom stawianym algorytmowi.
W celu stworzenia dokładniejszej wersji algorytmu należałoby się wrócić do etapu czyszczenia danych i usunąć pomiary, których charakter znacząco różni się od docelowych pomiarów.
W miarę możliwości należałoby również zwiększyć bazę poprawnych pomiarów.






