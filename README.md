# Run app

With installed python
```
python main.py
```

# Badana funkcja: Himmelblau
Funkcja Himmelblaua, zdefiniowana dla dwóch zmiennych i posiadająca wiele globalnych minimów. Charakterystyczny kształt z czterema minimami lokalnymi sprawia, zakres poszukiwań [−5,5].

![image](https://github.com/user-attachments/assets/7c10eb02-8dbc-4fab-85c7-619f0a6dd1d8)

![image](https://github.com/user-attachments/assets/080f9f07-80ab-4df1-80b1-9b2d45508d9c)

# Schemat algorytmu genetycznego
Idea algorytmu: osobniki populacji w kolejnych itearcjiach krzyzujemy z nadzieją ze po wymianie ich kodu genetycznegom uzyskamy lepsze osobniki, a nassze rozwiązanie będzie się z czasem poprawiać. 
Genotyp (reprezentacja osobnika) - ciąg binarny.
Fentotyp - zakodowana wartość genotypu.
Długość genu - określa jaka w zdadanym przedziale jest konieczna dokładność
 

![image](https://github.com/user-attachments/assets/c43f5f7b-eb04-4e49-947b-60c69104caca)

# Założenia

Poszukujemy rozwiązania zadanej funkcji. Ograniczamy się do pewnego zakresu. Szukamy pary x i f(x). Osobnik = chromosom. Gen = wartość (x,y), Allel = wartość genu f(x,y). 

1. Inicjalizacja populacji
2. Ewaluacja
3. Selekcja
     - najlepszych osobników (procent wybranych osobników np 30%)
     - turniejowa (podział na n turniejów i n osobników, zwycęzca grupy turniejowej idzie do krzyzowania, najlepiej wybrać 3 albo 5)
     - rankingowa (na podstawie funkcji celu przyznajemy rangi osobnikom)
     - koła ruletki, nakierowana na problem maksymalizacji, minimalizacjia = odwrotność funkcji celu,  (w zalezności od dospasowania, dany osobnik zajmuje większe pole w kole ruletki i ma wieksze szanse na wylosowanie: obliczenie sumy osobników i prawdopodobieństwo ich wylosowania, losowanie na podstawie dystrybuanty (aktualnej sumie prawdopodobienstw, na koncu nie moze przekroczyć jedynki)
4. Krzyżowanie - wprowadzanie zmienności w wybranych osobnikach z selekcji
     - jednopunktowe - określenie w jakim miejscu w ciągu bitów osobniki się krzyzują i wymiana ich genów, skupia się na pojednyńczych genach nie na blokach genów, 
       ![image](https://github.com/user-attachments/assets/c68644dc-28ec-4cb0-9df5-20880a940876)

     - dwupunktowe

       ![image](https://github.com/user-attachments/assets/490aa58a-3922-4bf5-bac0-bdee8865b573)
     - równomierne (jednorodne), skupia się na pojedyńczych genach nie na blokach genów, itaracyjne przejście po bitach osobnika, ustawienie progu zamiany domyślnie p = 0.5, dla kazdego bitu losujemy α i jeśli p < α to zamieniamy bity
       ![image](https://github.com/user-attachments/assets/56b91b48-ec31-43d3-9902-7a7dd9f463eb)

5. Mutacja - przed krzyzowaniem losujemy liczbę, jesli jest mniejsza niz np 0.9 to nie mutujemy, a jeśli większa to mutujemy, prawdopodobieństwo mutacji ma być niewielkie, mutacja to zamiana kilku bitów na przeciwną wartość
     - jednopunktowa, losujemy gen podlegajacy mutacji i go zamieniamy
       ![image](https://github.com/user-attachments/assets/324730ee-08df-4bd7-a172-f30f67a96b5b)

     - dwupunktowa
       ![image](https://github.com/user-attachments/assets/a60a190c-286f-4510-bb00-7946f99167e3)

6. Inwersja - forma muacji pojedyńczego osobnika nie pary osobników, losowanie dwóch punktów i zamiana bitów między nimi, prawdopodobieństwo inwersji 10%, 20%
   ![image](https://github.com/user-attachments/assets/dacf684a-a3dc-4338-a9a3-6c759989ab2b)

# Strategia elitarna
Gdy na samym początku ewolucji przypadkiem uzyskamy najlepszego osobnikam, przenoszę go do kolejnych iteracji i mam gwarancję ze na samym końcu będę miał najlepszego  

   
