# Stein Schere Papier – Softwareprojekt

## Projektübersicht

Das Projekt „Stein Schere Papier“ ist ein interaktives Zwei-Spieler-Spiel, das im Rahmen eines Softwareprojekts an der Hochschule entwickelt wird. Ziel ist es, ein funktionales, benutzerfreundliches Spiel mit klar definierten Anforderungen, modularer Architektur und nachvollziehbaren Abläufen zu entwerfen und umzusetzen.

## Motivation

Das Spiel soll nicht nur unterhalten, sondern auch exemplarisch zeigen, wie ein vollständiger Softwareentwicklungsprozess von der Planung bis zur Testung durchgeführt wird. Besonderer Wert wird auf Nutzerführung, Interfacegestaltung und eine skalierbare Codebasis gelegt.

---

## Funktionsweise

- Zwei Spieler treten gegeneinander an
- Auswahl über Buttons: 🪨 Stein, ✂️ Schere, 📄 Papier
- Auswertung erfolgt pro Runde, mit Live-Anzeige der Lebenspunkte
- Spiel endet bei 0 Lebenspunkten eines Spielers

---

## Benutzeroberfläche

- **Lebensbalken** für beide Spieler (Healthbar)
- **Auswahlbuttons** für Stein, Schere, Papier
- **Rundenanzeige** und Ergebnis-Feedback
- **Reset-Button** zur Wiederholung des Spiels

---

## Softwarearchitektur

| Komponente     | Beschreibung                                                   |
|----------------|----------------------------------------------------------------|
| `GameEngine`   | Logik zur Auswertung der Spielzüge, Punktezählung              |
| `UI`           | Steuerung und Anzeige aller Bedienelemente                     |
| `Player`       | Zustandsobjekt für Spielerauswahl und Lebenspunkte             |
| `Controller`   | Bindeglied zwischen UI und Logik, Events und Reaktionen        |
| `Tests`        | Automatisierte Unit-Tests zur Prüfung der Spiellogik           |

---

## Anforderungsanalyse (aus Interview)

- Spiel muss intuitiv und schnell verständlich sein
- Benutzer sollen visuelles Feedback erhalten
- Wichtig war dem Kunden ein „klassisches Spielgefühl mit moderner Oberfläche“
- Zukunftsidee: Integration eines Turniermodus oder Highscore-Boards

---

## Projektstruktur

```plaintext
stein-schere-papier/
├── assets/             # Bilder, Sounds, Icons
├── src/                # Quellcode
│   ├── ui/             # Benutzeroberfläche
│   ├── logic/          # Spiellogik
│   └── controller/     # Eventsteuerung
├── tests/              # Testfälle
├── docs/               # Projektdokumentation
└── README.md
