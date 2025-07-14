#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour l'extraction multiple de SCPI
Teste la nouvelle fonctionnalité sans lancer le scraper complet
"""

from main import SCPI_LIST, extract_multiple_scpi, print_scpi_header
import sys

def test_scpi_list():
    """Teste la configuration de la liste des SCPI"""
    print("🧪 TEST DE LA CONFIGURATION DES SCPI")
    print("=" * 50)
    
    print(f"📋 Nombre de SCPI configurées: {len(SCPI_LIST)}")
    
    for i, scpi in enumerate(SCPI_LIST, 1):
        print(f"{i}. {scpi['nom']} (ID: {scpi['id']})")
        
        # Vérifications de base
        assert 'nom' in scpi, f"Clé 'nom' manquante pour la SCPI {i}"
        assert 'id' in scpi, f"Clé 'id' manquante pour la SCPI {i}"
        assert isinstance(scpi['id'], int), f"L'ID doit être un entier pour {scpi['nom']}"
        assert len(scpi['nom']) > 0, f"Le nom ne peut pas être vide pour la SCPI {i}"
    
    print("✅ Configuration des SCPI validée!")

def test_header_display():
    """Teste l'affichage des en-têtes"""
    print("\n🧪 TEST DE L'AFFICHAGE DES EN-TÊTES")
    print("=" * 50)
    
    for i, scpi in enumerate(SCPI_LIST, 1):
        print_scpi_header(scpi, i, len(SCPI_LIST))
        print("   (Simulation d'extraction...)")

def test_dry_run():
    """Simulation d'exécution sans scraping réel"""
    print("\n🧪 TEST DE SIMULATION D'EXTRACTION MULTIPLE")
    print("=" * 50)
    
    print("⚠️  SIMULATION UNIQUEMENT - Aucun scraping réel ne sera effectué")
    print("   Pour tester le scraping réel, utilisez: python main.py --multiple")
    
    for i, scpi in enumerate(SCPI_LIST, 1):
        print_scpi_header(scpi, i, len(SCPI_LIST))
        print("🔍 Extraction en cours... (SIMULATION)")
        print("✅ Extraction simulée réussie")
        
        if i < len(SCPI_LIST):
            print("⏳ Pause simulée...")
    
    print("\n📈 RÉSUMÉ DE LA SIMULATION")
    print("=" * 80)
    print(f"✅ Extractions simulées: {len(SCPI_LIST)}/{len(SCPI_LIST)}")
    print("💡 Pour lancer l'extraction réelle: python main.py --multiple")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        test_dry_run()
    else:
        test_scpi_list()
        test_header_display()
        
        print("\n🚀 COMMANDES DISPONIBLES:")
        print("=" * 50)
        print("python test_multiple_scpi.py           # Tests de configuration")
        print("python test_multiple_scpi.py --dry-run # Simulation complète")
        print("python main.py --multiple              # Extraction réelle")
        print("python main.py --help                  # Aide complète")
