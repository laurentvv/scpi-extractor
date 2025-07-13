#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration pour les scrapers SCPI
Permet de contrôler le mode d'affichage de Chrome
"""

import os
import json

class ScraperConfig:
    """Configuration globale pour les scrapers"""
    
    def __init__(self):
        self.config_file = "scraper_config.json"
        self.default_config = {
            "headless_mode": True,  # Par défaut en mode headless
            "timeout": 30,
            "debug_mode": False,
            "save_screenshots": False,
            "chrome_path": "./chrome-win64/chrome.exe",
            "chromedriver_path": "./chromedriver-win64/chromedriver.exe"
        }
        self.load_config()
    
    def load_config(self):
        """Charge la configuration depuis le fichier"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                # Ajoute les clés manquantes avec les valeurs par défaut
                for key, value in self.default_config.items():
                    if key not in self.config:
                        self.config[key] = value
            else:
                self.config = self.default_config.copy()
                self.save_config()
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration: {e}")
            self.config = self.default_config.copy()
    
    def save_config(self):
        """Sauvegarde la configuration dans le fichier"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la configuration: {e}")
    
    def get(self, key, default=None):
        """Récupère une valeur de configuration"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Définit une valeur de configuration"""
        self.config[key] = value
        self.save_config()
    
    def is_headless(self):
        """Retourne True si le mode headless est activé"""
        return self.config.get("headless_mode", True)
    
    def set_headless(self, enabled):
        """Active ou désactive le mode headless"""
        self.set("headless_mode", enabled)
        print(f"Mode headless {'activé' if enabled else 'désactivé'}")
    
    def toggle_headless(self):
        """Bascule le mode headless"""
        current = self.is_headless()
        self.set_headless(not current)
        return not current
    
    def get_chrome_options(self):
        """Retourne les options Chrome configurées"""
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.binary_location = self.get("chrome_path")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-background-networking")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Ajoute --headless si activé
        if self.is_headless():
            chrome_options.add_argument("--headless")
        
        # Mode debug
        if self.get("debug_mode", False):
            chrome_options.add_argument("--enable-logging")
            chrome_options.add_argument("--v=1")
        
        return chrome_options
    
    def print_config(self):
        """Affiche la configuration actuelle"""
        print("📋 CONFIGURATION ACTUELLE:")
        print("=" * 40)
        for key, value in self.config.items():
            if key == "headless_mode":
                status = "🚫 Fenêtre cachée" if value else "👁️ Fenêtre visible"
                print(f"  Mode d'affichage: {status}")
            elif key == "timeout":
                print(f"  Timeout: {value}s")
            elif key == "debug_mode":
                print(f"  Mode debug: {'✅ Activé' if value else '❌ Désactivé'}")
            elif key == "save_screenshots":
                print(f"  Screenshots: {'✅ Activé' if value else '❌ Désactivé'}")
            else:
                print(f"  {key}: {value}")

# Instance globale de configuration
scraper_config = ScraperConfig()

def configure_scraper():
    """Interface de configuration interactive"""
    print("⚙️ CONFIGURATION DU SCRAPER SCPI")
    print("=" * 50)
    
    scraper_config.print_config()
    
    print("\n🔧 OPTIONS DISPONIBLES:")
    print("1. Basculer le mode d'affichage (headless/visible)")
    print("2. Modifier le timeout")
    print("3. Activer/désactiver le mode debug")
    print("4. Activer/désactiver les screenshots")
    print("5. Afficher la configuration")
    print("0. Quitter")
    
    while True:
        try:
            choice = input("\n👉 Votre choix (0-5): ").strip()
            
            if choice == "0":
                print("👋 Configuration terminée")
                break
            elif choice == "1":
                current = scraper_config.is_headless()
                scraper_config.toggle_headless()
                new_status = "fenêtre cachée" if not current else "fenêtre visible"
                print(f"✅ Mode changé vers: {new_status}")
            elif choice == "2":
                timeout = input("⏱️ Nouveau timeout en secondes (actuel: {}): ".format(scraper_config.get("timeout")))
                try:
                    timeout_val = int(timeout)
                    if timeout_val > 0:
                        scraper_config.set("timeout", timeout_val)
                        print(f"✅ Timeout défini à {timeout_val}s")
                    else:
                        print("❌ Le timeout doit être positif")
                except ValueError:
                    print("❌ Valeur invalide")
            elif choice == "3":
                current = scraper_config.get("debug_mode", False)
                scraper_config.set("debug_mode", not current)
                print(f"✅ Mode debug {'activé' if not current else 'désactivé'}")
            elif choice == "4":
                current = scraper_config.get("save_screenshots", False)
                scraper_config.set("save_screenshots", not current)
                print(f"✅ Screenshots {'activés' if not current else 'désactivés'}")
            elif choice == "5":
                scraper_config.print_config()
            else:
                print("❌ Choix invalide")
                
        except KeyboardInterrupt:
            print("\n👋 Configuration interrompue")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")

def quick_config():
    """Configuration rapide via arguments"""
    import sys
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["--headless", "-h"]:
            scraper_config.set_headless(True)
            print("🚫 Mode headless activé")
        elif arg in ["--visible", "-v"]:
            scraper_config.set_headless(False)
            print("👁️ Mode visible activé")
        elif arg in ["--config", "-c"]:
            configure_scraper()
        elif arg in ["--status", "-s"]:
            scraper_config.print_config()
        else:
            print("❌ Argument non reconnu")
            print("Usage: python config_scraper.py [--headless|--visible|--config|--status]")
    else:
        configure_scraper()

if __name__ == "__main__":
    quick_config()
