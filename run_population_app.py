#!/usr/bin/env python3

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    try:
        print("🎬📐 Uruchamianie ulepszonej animowanej aplikacji populacyjnej...")
        print("Sprawdzanie zależności...")

        try:
            import numpy
            print("✓ NumPy")
        except ImportError:
            print("❌ NumPy nie jest zainstalowane. Uruchom: pip install numpy")
            return False

        try:
            import matplotlib
            print("✓ Matplotlib")
        except ImportError:
            print("❌ Matplotlib nie jest zainstalowane. Uruchom: pip install matplotlib")
            return False

        try:
            import tkinter
            print("✓ Tkinter")
        except ImportError:
            print("❌ Tkinter nie jest zainstalowane.")
            print("Na Ubuntu/Debian: sudo apt-get install python3-tk")
            return False

        print("\nWszystkie zależności są dostępne.")
        print("🎬📐 Uruchamianie ulepszonej aplikacji...")

        from population_app import AnimatedPopulationGUI

        app = AnimatedPopulationGUI()
        print("🎬📐 Ulepszona aplikacja uruchomiona pomyślnie!")
        print("\n🆕 NOWE FUNKCJE:")
        print("📐 Wyświetlanie równań matematycznych")
        print("📊 Analiza stabilności i właściwości")
        print("💾 Eksport wykresów (PNG, PDF, SVG)")
        print("📄 Eksport danych do CSV")
        print("⚙️ Zapisywanie/wczytywanie parametrów")
        print("\n🎮 KONTROLKI ANIMACJI:")
        print("▶ Start/Wznów - rozpoczyna lub wznawia animację")
        print("⏸ Pauza - wstrzymuje animację")
        print("⏹ Stop - zatrzymuje i resetuje animację")
        print("🎚️ Suwak prędkości - kontroluje tempo animacji (0.1x - 5.0x)")
        print("\n📐 FUNKCJE MATEMATYCZNE:")
        print("📐 Pokaż równania - wyświetla równania różniczkowe i opis")
        print("📊 Analiza stabilności - oblicza punkty równowagi i stabilność")
        print("🔢 Oblicz właściwości - statystyki z symulacji")
        print("\n💾 EKSPORT:")
        print("💾 Eksportuj wykres czasowy - zapisuje dynamikę w czasie")
        print("💾 Eksportuj płaszczyznę fazową - zapisuje trajektorię fazową")
        print("💾 Eksportuj oba wykresy - kompletny zestaw wykresów")
        print("📄 Zapisz dane CSV - eksportuje dane numeryczne")
        print("\n📊 DOSTĘPNE MODELE:")
        print("- Model logistyczny (wzrost z ograniczeniem)")
        print("- Model Lotka-Volterra (drapieżnik-ofiara)")
        print("- Konkurencja międzygatunkowa (rywalizacja)")
        print("- Model SIR (epidemiologia)")
        print("- Metapopulacja (migracja między populacjami)")
        print("\nZamknij okno aplikacji aby zakończyć.")
        app.run()

        return True

    except Exception as e:
        print(f"❌ Błąd uruchamiania ulepszonej aplikacji: {str(e)}")
        print("\nSpróbuj uruchomić testy diagnostyczne:")
        print("python3 test_animation.py")
        return False


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
