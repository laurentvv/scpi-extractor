#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de démonstration des différents modes du SCPI Scraper
"""

import subprocess
import sys
import time

def run_command_demo(command, description, wait_time=3):
    """Lance une commande en mode démonstration"""
    print(f"\n🚀 {description}")
    print("=" * 60)
    print(f"💻 Commande: {command}")
    print("⏳ Lancement en cours...")
    
    try:
        # Lancer la commande
        process = subprocess.Popen(
            command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="."
        )
        
        # Attendre un peu pour voir le début de l'exécution
        time.sleep(wait_time)
        
        # Terminer le processus
        process.terminate()
        
        # Lire la sortie
        stdout, stderr = process.communicate(timeout=5)
        
        if stdout:
            print("📄 Sortie (début):")
            lines = stdout.split('\n')[:10]  # Premières lignes seulement
            for line in lines:
                if line.strip():
                    print(f"   {line}")
            if len(stdout.split('\n')) > 10:
                print("   [... sortie tronquée pour la démo ...]")
        
        print("✅ Démonstration terminée (processus arrêté)")
        
    except subprocess.TimeoutExpired:
        process.kill()
        print("⏰ Timeout - processus arrêté")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def demo_all_modes():
    """Démonstration de tous les modes"""
    print("🎯 DÉMONSTRATION DES MODES SCPI SCRAPER")
    print("=" * 80)
    print("⚠️  ATTENTION: Cette démonstration lance les commandes brièvement")
    print("   puis les arrête pour éviter une extraction complète.")
    print("   Pour une extraction complète, utilisez les commandes manuellement.")
    
    # Mode aide
    print(f"\n📚 MODE AIDE")
    print("=" * 60)
    print("💻 Commande: python main.py --help")
    try:
        result = subprocess.run(
            ["python", "main.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        print("📄 Sortie:")
        for line in result.stdout.split('\n'):
            if line.strip():
                print(f"   {line}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Tests de configuration
    print(f"\n🧪 TESTS DE CONFIGURATION")
    print("=" * 60)
    print("💻 Commande: python test_multiple_scpi.py")
    try:
        result = subprocess.run(
            ["python", "test_multiple_scpi.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        print("📄 Sortie:")
        for line in result.stdout.split('\n')[:15]:  # Premières lignes
            if line.strip():
                print(f"   {line}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Démonstration des modes de scraping (arrêtés rapidement)
    modes = [
        ("python main.py --multiple", "MODE MULTIPLE - Toutes les SCPI", 5),
        ("python main.py 39", "MODE UNIQUE - EPARGNE FONCIERE (ID: 39)", 3),
        ("python main.py --quick", "MODE RAPIDE - Extraction rapide", 3)
    ]
    
    for command, description, wait_time in modes:
        run_command_demo(command, description, wait_time)
    
    print(f"\n🎉 DÉMONSTRATION TERMINÉE")
    print("=" * 80)
    print("💡 Pour lancer une extraction complète:")
    print("   python main.py --multiple    # Toutes les SCPI")
    print("   python main.py 39           # SCPI spécifique")
    print("   python main.py --quick      # Extraction rapide")

def demo_quick_test():
    """Démonstration rapide avec tests uniquement"""
    print("⚡ DÉMONSTRATION RAPIDE - TESTS UNIQUEMENT")
    print("=" * 60)
    
    # Tests de configuration
    try:
        result = subprocess.run(
            ["python", "test_multiple_scpi.py"],
            capture_output=True,
            text=True,
            timeout=15
        )
        print("✅ Tests de configuration:")
        for line in result.stdout.split('\n'):
            if line.strip():
                print(f"   {line}")
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    # Simulation
    try:
        result = subprocess.run(
            ["python", "test_multiple_scpi.py", "--dry-run"],
            capture_output=True,
            text=True,
            timeout=15
        )
        print("\n✅ Simulation d'extraction multiple:")
        lines = result.stdout.split('\n')
        for line in lines[-10:]:  # Dernières lignes (résumé)
            if line.strip():
                print(f"   {line}")
    except Exception as e:
        print(f"❌ Erreur lors de la simulation: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        demo_quick_test()
    else:
        demo_all_modes()
