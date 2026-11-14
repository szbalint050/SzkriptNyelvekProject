VizsgaNaptár – ZH- és vizsganyilvántartó

Név: Szabó Bálint Gábor
Neptun-kód: DMA0SH

Feladat leírása

Interaktív grafikus alkalmazás, amely nyilvántartja, hogy mely napokon lesz ZH vagy vizsga, és az időpontokat havi naptárban jeleníti meg.

A program funkciói:

- ZH-k és vizsgák felvétele: tantárgy, típus (ZH vagy vizsga) és dátum megadása beviteli mezőkből
- Az időpontok nyilvántartása dátum szerint rendezve
- Lépkedés az egyes időpontok között a ← és → nyilakkal
- A kiválasztott időpont adatainak kiírása: tantárgy, típus, dátum és a hátralévő napok száma
- Havi naptár kirajzolása, a ZH- és vizsganapok eltérő színű jelölésével
- Gombok: Hozzáadás, Törlés, Következő időpont, Kilépés
- Hónapok léptetése a naptárban az egérgörgővel
- Hibás vagy hiányos adat esetén hibaüzenet
- Az időpontok mentése az `idopontok.csv` fájlba és betöltése a program indulásakor

Felhasználói leírás

- Telepíteni semmit nem kell, a program csak a Python beépített moduljait használja.
- Indítás: `python main.py`
- A dátumot `ÉÉÉÉ.HH.NN` formában kell megadni, pl.: `2026.12.15`.
- A típus mezőbe `ZH` vagy `vizsga` lehet írni.
- A ← és → nyilakkal lépked.

Felépítés

Modulok

- `main.py` – a program indítása, létrehozza az ablakot és az `app` objektumot
- `szbg_modul.py` – saját modul, ebben van a program teljes működése
- Felhasznált beépített modulok: `tkinter` (grafika, eseménykezelés), `datetime` (dátumok kezelése), `csv` (fájlkezelés)

Függvények

- `szbg_datum_atalakitas(szoveg)` – a beírt szövegből dátumot készít, hibás formátum esetén `None`-t ad vissza
- `szbg_hatralevo_napok(datum)` – megadja, hány nap van hátra a dátumig
- `szbg_mentes(idopontok, fajlnev)` – az időpontokat CSV fájlba menti
- `szbg_betoltes(fajlnev)` – betölti és dátum szerint rendezi a mentett időpontokat

Osztály

`SzbgVizsgaNaptar` – a program ablaka és működése. Metódusai:

- `hozzaadas` – új időpont felvétele ellenőrzés után
- `torles` – a kiválasztott időpont törlése megerősítés után
- `mentes` – az időpontok fájlba írása
- `kovetkezo_idopont` – a mai naphoz legközelebbi időpont kiválasztása
- `kivalasztas` – egy időpont kijelölése és a kijelző frissítése
- `lepes_balra`, `lepes_jobbra`, `lepes` – lépkedés az időpontok között a nyílbillentyűkkel
- `gorgetes` – hónap váltása az egérgörgővel
- `fokusz_elvetel` – a naptárra kattintva kiveszi a kurzort a beviteli mezőből
- `adatok_kiirasa` – a kiválasztott időpont adatainak megjelenítése
- `naptar_rajzolas` – a havi naptár kirajzolása
