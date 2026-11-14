import csv
import tkinter as tk
from datetime import datetime, date
from tkinter import ttk, messagebox

FAJLNEV = 'idopontok.csv'
DATUM_FORMA = '%Y.%m.%d'
HONAPOK = ['január', 'február', 'március', 'április', 'május', 'június',
           'július', 'augusztus', 'szeptember', 'október', 'november', 'december']
NAPOK = ['H', 'K', 'Sze', 'Cs', 'P', 'Szo', 'V']
SZINEK = {'ZH': 'orange', 'vizsga': 'tomato'}


def szbg_datum_atalakitas(szoveg):
    try:
        return datetime.strptime(szoveg.strip(), DATUM_FORMA).date()
    except ValueError:
        return None


def szbg_hatralevo_napok(datum):
    return (datum - date.today()).days


def szbg_mentes(idopontok, fajlnev=FAJLNEV):
    with open(fajlnev, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['datum', 'targy', 'tipus'])
        for datum, targy, tipus in idopontok:
            writer.writerow([datum.strftime(DATUM_FORMA), targy, tipus])


def szbg_betoltes(fajlnev=FAJLNEV):
    idopontok = []
    try:
        with open(fajlnev, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for sor in reader:
                if len(sor) != 3:
                    continue
                datum = szbg_datum_atalakitas(sor[0])
                if datum is None:
                    continue
                idopontok.append((datum, sor[1], sor[2]))
    except FileNotFoundError:
        return []
    idopontok.sort()
    return idopontok


class SzbgVizsgaNaptar:
    def __init__(self, root):
        self.root = root
        self.root.title('VizsgaNaptár')
        self.root.geometry('800x490')
        self.idopontok = szbg_betoltes()
        self.kivalasztott = 0
        self.ev = date.today().year
        self.honap = date.today().month

        self.cim_cimke = ttk.Label(root, text='VizsgaNaptár – ZH- és vizsganyilvántartó', font='Arial 16 bold')
        self.cim_cimke.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.targy_cimke = ttk.Label(root, text='Tantárgy:')
        self.targy_cimke.grid(row=1, column=0, padx=10, pady=5)
        self.targy = tk.StringVar()
        self.targy_be = ttk.Entry(root, textvariable=self.targy, width=22)
        self.targy_be.grid(row=1, column=1, padx=10, pady=5)

        self.tipus_cimke = ttk.Label(root, text='Típus (ZH / vizsga):')
        self.tipus_cimke.grid(row=2, column=0, padx=10, pady=5)
        self.tipus = tk.StringVar(value='ZH')
        self.tipus_be = ttk.Entry(root, textvariable=self.tipus, width=22)
        self.tipus_be.grid(row=2, column=1, padx=10, pady=5)

        self.datum_cimke = ttk.Label(root, text='Dátum (ÉÉÉÉ.HH.NN):')
        self.datum_cimke.grid(row=3, column=0, padx=10, pady=5)
        self.datum = tk.StringVar(value=date.today().strftime(DATUM_FORMA))
        self.datum_be = ttk.Entry(root, textvariable=self.datum, width=22)
        self.datum_be.grid(row=3, column=1, padx=10, pady=5)

        self.hozzaadas_gomb = ttk.Button(root, text='Hozzáadás', command=self.hozzaadas)
        self.hozzaadas_gomb.grid(row=4, column=0, padx=10, pady=5)
        self.torles_gomb = ttk.Button(root, text='Törlés', command=self.torles)
        self.torles_gomb.grid(row=4, column=1, padx=10, pady=5)

        self.kovetkezo_gomb = ttk.Button(root, text='Következő időpont', command=self.kovetkezo_idopont)
        self.kovetkezo_gomb.grid(row=5, column=0, padx=10, pady=5)
        self.kilepes_gomb = ttk.Button(root, text='Kilépés', command=root.destroy)
        self.kilepes_gomb.grid(row=5, column=1, padx=10, pady=5)

        self.adatok_cimke = ttk.Label(root, text='', font='Arial 12')
        self.adatok_cimke.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.sugo_cimke = ttk.Label(root, text='← → : lépkedés az időpontok között\nEgérgörgő: hónap váltása')
        self.sugo_cimke.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

        self.vaszon = tk.Canvas(root, width=420, height=400, bg='white')
        self.vaszon.grid(row=1, column=2, rowspan=7, padx=10, pady=5)

        self.root.bind('<Left>', self.lepes_balra)
        self.root.bind('<Right>', self.lepes_jobbra)
        self.root.bind('<MouseWheel>', self.gorgetes)
        self.vaszon.bind('<Button-1>', self.fokusz_elvetel)

        self.kovetkezo_idopont()

    def hozzaadas(self):
        targy = self.targy.get().strip()
        tipus = self.tipus.get().strip().lower()
        datum = szbg_datum_atalakitas(self.datum.get())

        if targy == '':
            messagebox.showerror('Hiba', 'Adja meg a tantárgy nevét!')
            return
        if tipus == 'zh':
            tipus = 'ZH'
        elif tipus != 'vizsga':
            messagebox.showerror('Hiba', 'A típus csak ZH vagy vizsga lehet!')
            return
        if datum is None:
            messagebox.showerror('Hiba', 'A dátum formátuma: ÉÉÉÉ.HH.NN, például 2026.12.15')
            return

        uj = (datum, targy, tipus)
        if uj in self.idopontok:
            messagebox.showwarning('Figyelem', 'Ez az időpont már szerepel a nyilvántartásban!')
            return

        self.idopontok.append(uj)
        self.idopontok.sort()
        self.mentes()
        self.targy.set('')
        self.root.focus_set()
        self.kivalasztas(self.idopontok.index(uj))

    def torles(self):
        if len(self.idopontok) == 0:
            messagebox.showwarning('Törlés', 'Nincs törölhető időpont!')
            return
        datum, targy, tipus = self.idopontok[self.kivalasztott]
        valasz = messagebox.askyesno('Törlés', f'Biztosan töröljem?\n{targy} – {tipus}')
        if not valasz:
            return
        del self.idopontok[self.kivalasztott]
        self.mentes()
        if self.kivalasztott >= len(self.idopontok):
            self.kivalasztott = max(len(self.idopontok) - 1, 0)
        self.kivalasztas(self.kivalasztott)

    def mentes(self):
        try:
            szbg_mentes(self.idopontok)
        except OSError:
            messagebox.showerror('Hiba', 'Nem sikerült a mentés!')

    def kovetkezo_idopont(self):
        index = max(len(self.idopontok) - 1, 0)
        for i in range(len(self.idopontok)):
            if szbg_hatralevo_napok(self.idopontok[i][0]) >= 0:
                index = i
                break
        self.kivalasztas(index)

    def kivalasztas(self, index):
        self.kivalasztott = index
        if len(self.idopontok) > 0:
            datum = self.idopontok[index][0]
            self.ev = datum.year
            self.honap = datum.month
        self.adatok_kiirasa()
        self.naptar_rajzolas()

    def lepes_balra(self, event):
        self.lepes(event, -1)

    def lepes_jobbra(self, event):
        self.lepes(event, 1)

    def lepes(self, event, irany):
        if isinstance(event.widget, ttk.Entry):
            return
        if len(self.idopontok) == 0:
            return
        index = self.kivalasztott + irany
        if 0 <= index < len(self.idopontok):
            self.kivalasztas(index)

    def gorgetes(self, event):
        if event.delta > 0:
            self.honap -= 1
        else:
            self.honap += 1
        if self.honap == 0:
            self.honap = 12
            self.ev -= 1
        elif self.honap == 13:
            self.honap = 1
            self.ev += 1
        self.naptar_rajzolas()

    def fokusz_elvetel(self, event):
        self.root.focus_set()

    def adatok_kiirasa(self):
        if len(self.idopontok) == 0:
            self.adatok_cimke.config(text='Még nincs felvett időpont.')
            return
        datum, targy, tipus = self.idopontok[self.kivalasztott]
        napok = szbg_hatralevo_napok(datum)
        if napok > 0:
            hatra = f'Még {napok} nap van hátra'
        elif napok == 0:
            hatra = 'Ma van!'
        else:
            hatra = f'{-napok} napja elmúlt'
        szoveg = f'{self.kivalasztott + 1}. időpont a {len(self.idopontok)} közül\n'
        szoveg += f'Tantárgy: {targy}\n'
        szoveg += f'Típus: {tipus}\n'
        szoveg += f'Dátum: {datum.strftime(DATUM_FORMA)}\n'
        szoveg += hatra
        self.adatok_cimke.config(text=szoveg)

    def naptar_rajzolas(self):
        self.vaszon.delete('all')
        self.vaszon.create_text(210, 20, text=f'{self.ev}. {HONAPOK[self.honap - 1]}', font='Arial 14 bold')
        for i in range(7):
            self.vaszon.create_text(30 + i * 60, 50, text=NAPOK[i], font='Arial 10 bold')

        elso_nap = date(self.ev, self.honap, 1)
        if self.honap == 12:
            kovetkezo_honap = date(self.ev + 1, 1, 1)
        else:
            kovetkezo_honap = date(self.ev, self.honap + 1, 1)
        napok_szama = (kovetkezo_honap - elso_nap).days

        jelolt_napok = {}
        for datum, targy, tipus in self.idopontok:
            if datum.year == self.ev and datum.month == self.honap:
                if tipus == 'vizsga' or datum.day not in jelolt_napok:
                    jelolt_napok[datum.day] = tipus

        kivalasztott_nap = 0
        if len(self.idopontok) > 0:
            datum = self.idopontok[self.kivalasztott][0]
            if datum.year == self.ev and datum.month == self.honap:
                kivalasztott_nap = datum.day

        ma = date.today()
        oszlop = elso_nap.weekday()
        sor = 0
        for nap in range(1, napok_szama + 1):
            x = oszlop * 60
            y = 65 + sor * 50
            szin = 'white'
            if nap in jelolt_napok:
                szin = SZINEK[jelolt_napok[nap]]
            self.vaszon.create_rectangle(x + 3, y + 3, x + 57, y + 47, fill=szin, outline='gray')
            if nap == kivalasztott_nap:
                self.vaszon.create_rectangle(x + 3, y + 3, x + 57, y + 47, outline='blue', width=3)
            betu = 'Arial 11'
            if date(self.ev, self.honap, nap) == ma:
                betu = 'Arial 11 bold underline'
            self.vaszon.create_text(x + 30, y + 25, text=str(nap), font=betu)
            oszlop += 1
            if oszlop == 7:
                oszlop = 0
                sor += 1

        self.vaszon.create_rectangle(20, 375, 40, 390, fill=SZINEK['ZH'], outline='gray')
        self.vaszon.create_text(60, 383, text='ZH')
        self.vaszon.create_rectangle(110, 375, 130, 390, fill=SZINEK['vizsga'], outline='gray')
        self.vaszon.create_text(160, 383, text='vizsga')
        self.vaszon.create_rectangle(220, 375, 240, 390, outline='blue', width=3)
        self.vaszon.create_text(285, 383, text='kiválasztott')


if __name__ == '__main__':
    root = tk.Tk()
    app = SzbgVizsgaNaptar(root)
    root.mainloop()
