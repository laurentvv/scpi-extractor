# SCPI Scraper - Extracteur de données SCPI

Ce projet permet d'extraire automatiquement les données des SCPI depuis le site scpi-lab.com et de les afficher dans un format structuré.

## 🚀 Fonctionnalités

- **Extraction complète** : Chiffres clés, informations générales, données trimestrielles
- **Actualités** : Dernières informations et bulletins trimestriels
- **Événements clés** : Historique des changements importants (prix, dividendes, etc.)
- **Structure de données** : Dataclasses Python pour une manipulation facile
- **Mode headless** : Chrome caché par défaut, mode visible optionnel
- **Affichage optimisé** : Résultats formatés et lisibles

## 📋 Prérequis

- Python 3.7+
- Chrome et ChromeDriver (non inclus dans le dépôt en raison des limitations de taille GitHub)
- Packages Python : `selenium`, `dataclasses`

## 🛠️ Installation

1. Clonez le projet :
```bash
git clone https://github.com/laurentvv/scpi-extractor.git
cd scpi-extractor
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Téléchargez Chrome et ChromeDriver :
   - Téléchargez Chrome pour les tests depuis [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/)
   - Liens directs pour la version 138.0.7204.94 :
     - [Chrome](https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.94/win64/chrome-win64.zip)
     - [ChromeDriver](https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.94/win64/chromedriver-win64.zip)
   - Décompressez les fichiers dans les dossiers `chrome-win64/` et `chromedriver-win64/` respectivement

## 📊 Structure des données

### SCPIData (classe principale)
- `general_info` : Informations générales (nom, société de gestion, etc.)
- `chiffres_cles` : Chiffres clés (capitalisation, distribution, etc.)
- `trimestre_info` : Données du dernier trimestre
- `evenements_cles` : Liste des événements importants
- `actualites` : Liste des dernières actualités

### Exemple de données extraites :
```python
{
  "general_info": {
    "nom": "EPARGNE FONCIERE",
    "societe_gestion": "LA FRANCAISE",
    "statut": "Ouverte",
    "type_capital": "CAPITAL VARIABLE",
    "annee_creation": 1968
  },
  "chiffres_cles": {
    "capitalisation": "4 174 M€",
    "prix_part_actuel": 670.0,
    "taux_distribution_brut": 4.52,
    "dividende_brut_annuel": 37.71
  }
}
```

## 🎯 Utilisation

### Utilisation simple

```bash
# Extraction complète
python main.py

# Extraction rapide
python main.py --quick

# Autre SCPI (ex: GENEPIERRE)
python main.py 51
```

### Contrôle du mode d'affichage

```bash
# Mode headless (par défaut) - Chrome caché
python config_scraper.py --headless

# Mode visible - Chrome affiché
python config_scraper.py --visible

# Vérifier la configuration
python config_scraper.py --status
```

### Utilisation programmatique

```python
from scpi_scraper import scrape_scpi_data

# Scraper EPARGNE FONCIERE (ID 39)
scpi_data = scrape_scpi_data(39)
scpi_data.print_summary()

# Accéder aux données
print(f"Prix: {scpi_data.chiffres_cles.prix_part_actuel}€")
print(f"Distribution: {scpi_data.chiffres_cles.taux_distribution_brut}%")
```

## 🔍 IDs des SCPI populaires

| SCPI | ID | Société de gestion |
|------|----|--------------------|
| EPARGNE FONCIERE | 39 | LA FRANCAISE |
| EPARGNE PIERRE | 40 | LA FRANCAISE |
| GENEPIERRE | 51 | GENERALI |
| PFO | 84 | PERIAL |
| PRIMOPIERRE | 95 | CREDIT MUTUEL |

Pour trouver l'ID d'une SCPI, consultez l'URL sur scpi-lab.com :
`https://www.scpi-lab.com/scpi.php?vue=&produit_id=XX`

## 📁 Fichiers du projet

- `scpi_dataclasses.py` : Définition des structures de données
- `scpi_scraper.py` : Scraper principal optimisé
- `config_scraper.py` : Configuration du mode d'affichage
- `main.py` : Script principal d'extraction
- `GUIDE_MODE_HEADLESS.md` : Guide du mode headless

## ⚙️ Configuration

### Modification du mode d'affichage
Par défaut, le scraper utilise le mode headless (Chrome caché) :

```bash
# Changer vers mode visible
python config_scraper.py --visible

# Retour au mode headless
python config_scraper.py --headless
```

### Configuration avancée
La configuration est stockée dans `scraper_config.json` et peut être modifiée via le script de configuration.

## 🚨 Limitations et bonnes pratiques

- **Respect du site** : Le scraper inclut des délais automatiques
- **Mode headless** : Chrome est caché par défaut pour ne pas déranger
- **Données** : Les données sont extraites en temps réel et affichées uniquement
- **Légalité** : Respectez les conditions d'utilisation du site

## 🔧 Dépannage

### Erreur ChromeDriver
```bash
# Vérifiez que ChromeDriver est dans le bon dossier
ls chromedriver-win64/chromedriver.exe
```

### Timeout lors du chargement
```python
# Augmentez le timeout dans SCPIScraper.__init__()
self.wait = WebDriverWait(self.driver, 60)  # 60 secondes
```

### Sélecteurs obsolètes
Si le site change, mettez à jour les XPath dans les méthodes `_extract_*()`.

## 📈 Exemple de sortie

```
🚀 EXTRACTION DES DONNÉES SCPI
==================================================
🖥️ 🚫 Mode headless (fenêtre cachée)
   💡 Pour changer: python config_scraper.py --visible ou --headless

🔍 Extraction des données pour la SCPI ID 39...

=== SCPI EPARGNE FONCIERE ===
Société de gestion: LA FRANCAISE
Prix actuel: 670.0€
Distribution brute 2024: 4.52% (37.71€)
Capitalisation: 4 174 M€
Nombre d'associés: 57,895

💰 INFORMATIONS FINANCIÈRES:
   Prix de part: 670.0€
   Distribution brute: 4.52% (37.71€/part)
   Distribution nette: 4.4% (36.72€/part)
   Capitalisation: 4 174 M€

✅ Extraction terminée avec succès!
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités

## 📄 Licence

Ce projet est à des fins éducatives. Respectez les conditions d'utilisation de scpi-lab.com.



