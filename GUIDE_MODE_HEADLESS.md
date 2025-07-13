# 🖥️ Guide - Contrôle du Mode d'Affichage Chrome

## 🎯 Problème Résolu

✅ **Vous pouvez maintenant désactiver l'ouverture de Chrome lors du parsing !**

Par défaut, Chrome s'exécute en **mode headless** (fenêtre cachée) pour ne pas déranger votre travail.

## 🚀 Utilisation Rapide

### Mode Headless (Recommandé) - Fenêtre Cachée
```bash
# Activer le mode headless (par défaut)
python config_scraper.py --headless

# Extraction sans fenêtre visible
python main.py
```

### Mode Visible - Fenêtre Affichée
```bash
# Activer le mode visible
python config_scraper.py --visible

# Extraction avec fenêtre Chrome visible
python main.py
```

## ⚙️ Configuration Détaillée

### 📋 Vérifier la Configuration Actuelle
```bash
python config_scraper.py --status
```

**Sortie :**
```
📋 CONFIGURATION ACTUELLE:
========================================
  Mode d'affichage: 🚫 Fenêtre cachée
  Timeout: 30s
  Mode debug: ❌ Désactivé
  Screenshots: ❌ Désactivé
```

### 🔧 Configuration Interactive
```bash
python config_scraper.py
```

**Menu interactif :**
```
⚙️ CONFIGURATION DU SCRAPER SCPI
==================================================
1. Basculer le mode d'affichage (headless/visible)
2. Modifier le timeout
3. Activer/désactiver le mode debug
4. Activer/désactiver les screenshots
5. Afficher la configuration
0. Quitter
```

## 🎯 Modes Disponibles

### 🚫 Mode Headless (Par Défaut)
- ✅ **Avantages** : Pas de fenêtre visible, plus rapide, moins de ressources
- ✅ **Usage** : Production, extraction automatique, scripts
- ✅ **Commande** : `python config_scraper.py --headless`

### 👁️ Mode Visible
- ✅ **Avantages** : Voir ce qui se passe, debug visuel, démonstration
- ✅ **Usage** : Développement, debug, présentation
- ✅ **Commande** : `python config_scraper.py --visible`

## 📊 Comparaison des Performances

| Mode | Vitesse | Ressources | Usage Recommandé |
|------|---------|------------|------------------|
| 🚫 **Headless** | ⚡ Plus rapide | 💾 Moins de RAM | 🏭 Production |
| 👁️ **Visible** | 🐌 Plus lent | 💾 Plus de RAM | 🔧 Développement |

## 🔧 Utilisation Avancée

### Script avec Mode Forcé
```python
from scpi_scraper_configurable import scrape_scpi_data_configurable

# Force le mode headless
data = scrape_scpi_data_configurable(39, headless=True)

# Force le mode visible
data = scrape_scpi_data_configurable(39, headless=False)

# Utilise la configuration globale
data = scrape_scpi_data_configurable(39)  # headless=None
```

### Configuration Programmatique
```python
from config_scraper import scraper_config

# Vérifier le mode actuel
if scraper_config.is_headless():
    print("Mode headless activé")

# Changer le mode
scraper_config.set_headless(False)  # Mode visible
scraper_config.set_headless(True)   # Mode headless

# Basculer le mode
scraper_config.toggle_headless()
```

## 📁 Fichiers de Configuration

### Configuration Automatique
- **Fichier** : `scraper_config.json`
- **Création** : Automatique au premier lancement
- **Localisation** : Répertoire du projet

### Exemple de Configuration
```json
{
  "headless_mode": true,
  "timeout": 30,
  "debug_mode": false,
  "save_screenshots": false,
  "chrome_path": "./chrome-win64/chrome.exe",
  "chromedriver_path": "./chromedriver-win64/chromedriver.exe"
}
```

## 🎯 Cas d'Usage Pratiques

### 🏭 Production / Automatisation
```bash
# Configuration pour production
python config_scraper.py --headless

# Extraction automatique
python main.py 39  # EPARGNE FONCIERE
python main.py 51  # GENEPIERRE
```

### 🔧 Développement / Debug
```bash
# Configuration pour développement
python config_scraper.py --visible

# Extraction avec visualisation
python main.py 39
```

### 📊 Monitoring Quotidien
```bash
#!/bin/bash
# Script de monitoring quotidien

# S'assurer du mode headless
python config_scraper.py --headless

# Extraire les SCPI principales
python main.py 39  # EPARGNE FONCIERE
python main.py 51  # GENEPIERRE
python main.py 84  # PFO
```

### 🎥 Démonstration / Présentation
```bash
# Configuration pour démonstration
python config_scraper.py --visible

# Démonstration complète
python demo_final.py
```

## 🚨 Dépannage

### Problème : Chrome ne se lance pas
```bash
# Vérifier la configuration
python config_scraper.py --status

# Tester en mode visible pour voir les erreurs
python config_scraper.py --visible
python main.py
```

### Problème : Timeout fréquents
```bash
# Augmenter le timeout
python config_scraper.py
# Choisir option 2 et définir 60 secondes
```

### Problème : Performances lentes
```bash
# Passer en mode headless
python config_scraper.py --headless
```

## 💡 Conseils d'Optimisation

### 🚀 Pour la Vitesse
1. **Mode headless** : `python config_scraper.py --headless`
2. **Timeout optimisé** : 30 secondes (par défaut)
3. **Pas de screenshots** : Désactivé par défaut

### 🔍 Pour le Debug
1. **Mode visible** : `python config_scraper.py --visible`
2. **Mode debug** : Activé via le menu interactif
3. **Screenshots** : Activés pour capturer les erreurs

### ⚖️ Équilibre
- **Développement** : Mode visible + debug activé
- **Tests** : Mode headless + timeout court
- **Production** : Mode headless + configuration optimisée

## 🎉 Résumé

✅ **Chrome peut maintenant être complètement caché** pendant l'extraction

✅ **Configuration flexible** : Headless par défaut, visible sur demande

✅ **Contrôle total** : Configuration interactive ou par ligne de commande

✅ **Performance optimisée** : Mode headless pour la production

✅ **Debug facilité** : Mode visible pour le développement

---

**🎯 Commandes Essentielles :**
- `python config_scraper.py --headless` - Mode caché
- `python config_scraper.py --visible` - Mode visible  
- `python config_scraper.py --status` - Vérifier la config
- `python main.py` - Extraction avec config actuelle
