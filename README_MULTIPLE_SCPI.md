# SCPI Scraper - Mode Multiple

## 🚀 Nouvelle Fonctionnalité : Extraction Multiple

Le scraper SCPI a été amélioré pour supporter l'extraction de données de plusieurs SCPI en une seule exécution.

## 📋 SCPI Configurées

Le script traite automatiquement les SCPI suivantes :

| Nom SCPI | ID | Description |
|----------|----|-----------| 
| PFO2 | 85 | SCPI par défaut |
| EPARGNE FONCIERE | 39 | SCPI populaire |
| AESTIAM PIERRE RENDEMENT | 10 | SCPI de rendement |
| LF OPPORTUNITE IMMO | 66 | SCPI d'opportunité |

## 🖥️ Modes d'Utilisation

### Mode Multiple (Nouveau)
```bash
# Extraction de toutes les SCPI configurées
python main.py --multiple
# ou
python main.py --multi
```

### Mode Unique (Existant)
```bash
# SCPI par défaut (PFO2, ID: 85)
python main.py

# SCPI spécifique par ID
python main.py 39  # EPARGNE FONCIERE
python main.py 10  # AESTIAM PIERRE RENDEMENT
```

### Mode Rapide (Existant)
```bash
# Extraction rapide d'EPARGNE FONCIERE uniquement
python main.py --quick
```

### Aide
```bash
# Afficher l'aide et les options disponibles
python main.py --help
```

## 📊 Fonctionnalités du Mode Multiple

### ✅ Avantages
- **Extraction automatisée** : Traite toutes les SCPI configurées en une seule commande
- **Gestion d'erreurs robuste** : Si une SCPI échoue, les autres continuent
- **Affichage organisé** : Résultats clairement séparés par SCPI
- **Résumé comparatif** : Tableau de comparaison des prix et rendements
- **Statistiques d'exécution** : Nombre de succès/échecs et temps total

### 🔧 Caractéristiques Techniques
- **Mode headless par défaut** : Fenêtre Chrome cachée pour plus de discrétion
- **Pause entre extractions** : 2 secondes entre chaque SCPI pour éviter la surcharge
- **Gestion des exceptions** : Chaque SCPI est traitée indépendamment
- **Affichage détaillé** : Toutes les informations (prix, actualités, événements)

## 📈 Exemple de Sortie (Mode Multiple)

```
🚀 EXTRACTION DES DONNÉES SCPI - MODE MULTIPLE
================================================================================
🖥️ 🚫 Mode headless (fenêtre cachée)
   💡 Pour changer: python config_scraper.py --visible ou --headless

📋 4 SCPI à traiter:
   • PFO2 (ID: 85)
   • EPARGNE FONCIERE (ID: 39)
   • AESTIAM PIERRE RENDEMENT (ID: 10)
   • LF OPPORTUNITE IMMO (ID: 66)

================================================================================
📊 SCPI 1/4: PFO2 (ID: 85)
================================================================================
🔍 Extraction en cours...

💰 INFORMATIONS FINANCIÈRES:
   Prix d'achat: 1000€
   Prix de vente: 950€
   Distribution brute: 4.5% (45€/part)
   [...]

✅ Extraction réussie pour PFO2

⏳ Pause de 2 secondes avant la prochaine extraction...

[... autres SCPI ...]

================================================================================
📈 RÉSUMÉ DE L'EXTRACTION MULTIPLE
================================================================================
✅ Extractions réussies: 4/4
❌ Extractions échouées: 0/4
⏱️  Temps total d'exécution: 45.67 secondes

💼 COMPARAISON RAPIDE:
--------------------------------------------------------------------------------
SCPI                      Prix Achat   Prix Vente   Distrib. Brute 
--------------------------------------------------------------------------------
PFO2                      1000€        950€         4.5%           
EPARGNE FONCIERE          200€         190€         5.2%           
AESTIAM PIERRE RENDEMENT  100€         95€          4.8%           
LF OPPORTUNITE IMMO       1000€        980€         4.1%           
```

## 🧪 Tests et Validation

### Script de Test
```bash
# Tests de configuration
python test_multiple_scpi.py

# Simulation complète (sans scraping réel)
python test_multiple_scpi.py --dry-run
```

### Validation
- ✅ Configuration des SCPI validée
- ✅ Affichage des en-têtes testé
- ✅ Simulation d'extraction multiple réussie
- ✅ Gestion d'erreurs implémentée

## ⚙️ Configuration

### Modifier la Liste des SCPI
Pour ajouter/modifier les SCPI à traiter, éditez la variable `SCPI_LIST` dans `main.py` :

```python
SCPI_LIST = [
    {"nom": "NOUVELLE_SCPI", "id": 123},
    {"nom": "PFO2", "id": 85},
    # ... autres SCPI
]
```

### Mode d'Affichage
```bash
# Passer en mode visible (fenêtre Chrome affichée)
python config_scraper.py --visible

# Revenir en mode headless (fenêtre cachée)
python config_scraper.py --headless
```

## 🔄 Mise à Jour de la Memory Bank

- ✅ Fonctionnalité d'extraction multiple implémentée
- ✅ Support de 4 SCPI configurées (PFO2, EPARGNE FONCIERE, AESTIAM PIERRE RENDEMENT, LF OPPORTUNITE IMMO)
- ✅ Gestion d'erreurs robuste avec continuation sur échec individuel
- ✅ Affichage organisé avec résumé comparatif
- ✅ Mode headless conservé par défaut
- ✅ Tests et validation ajoutés
