# Gravitačná sila F = m · g

Aplikácia v Pythone (Tkinter + matplotlib).

## Funkcie
- generuje 50 náhodných hmotností (1–100 kg),
- operácie s poľom: zoradenie, minimum, maximum, priemer,
- výpočet sily F = m · g (g = 9,81 m/s²),
- jeden graf s pôvodnými (m) aj vypočítanými (F) hodnotami,
- GUI: tlačidlá, vstupné pole, popisky; výpočet F pre ľubovoľné číslo.

## Spustenie
```
pip install -r requirements.txt
python main.py
```

## Vytvorenie .exe (Windows)
```
pyinstaller --onefile --windowed main.py
```
Výsledok: `dist/main.exe`
