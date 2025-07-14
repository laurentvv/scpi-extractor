#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script principal pour l'extraction des données SCPI
Utilise les scrapers améliorés avec sélecteurs dynamiques
Supporte l'extraction de plusieurs SCPI en une seule exécution
"""

from scpi_scraper import scrape_scpi_data
from config_scraper import scraper_config
import sys
import time

# Liste des SCPI à traiter avec leurs identifiants
SCPI_LIST = [
    {"nom": "PFO2", "id": 85},
    {"nom": "EPARGNE FONCIERE", "id": 39},
    {"nom": "AESTIAM PIERRE RENDEMENT", "id": 10},
    {"nom": "LF OPPORTUNITE IMMO", "id": 66}
]

def print_scpi_header(scpi_info, index, total):
    """Affiche l'en-tête pour une SCPI"""
    print("\n" + "=" * 80)
    print(f"� SCPI {index}/{total}: {scpi_info['nom']} (ID: {scpi_info['id']})")
    print("=" * 80)

def print_scpi_results(data):
    """Affiche les résultats détaillés pour une SCPI"""
    if not data:
        return

    # Afficher les informations clés
    print("\n💰 INFORMATIONS FINANCIÈRES:")
    print(f"   Prix d'achat: {data.chiffres_cles.prix_part_actuel}€")
    print(f"   Prix de vente: {data.chiffres_cles.prix_part_vente}€")
    print(f"   Distribution brute: {data.chiffres_cles.taux_distribution_brut}% ({data.chiffres_cles.dividende_brut_annuel}€/part)")
    print(f"   Distribution nette: {data.chiffres_cles.taux_distribution_net}% ({data.chiffres_cles.dividende_net_annuel}€/part)")
    print(f"   Capitalisation: {data.chiffres_cles.capitalisation}")

    print("\n🏢 INFORMATIONS GÉNÉRALES:")
    print(f"   Nom: {data.general_info.nom}")
    print(f"   Société de gestion: {data.general_info.societe_gestion}")
    print(f"   Statut: {data.general_info.statut}")
    print(f"   Type de capital: {data.general_info.type_capital}")
    print(f"   Année de création: {data.general_info.annee_creation}")

    print(f"\n📅 DERNIER TRIMESTRE ({data.trimestre_info.trimestre}):")
    print(f"   Collecte brute: {data.trimestre_info.collecte_brute}")
    print(f"   Acompte distribué: {data.trimestre_info.acompte_brut}€/part")
    print(f"   Nombre de cessions: {data.trimestre_info.nb_cessions}")

    if data.evenements_cles:
        print("\n🔔 DERNIERS ÉVÉNEMENTS:")
        for i, event in enumerate(data.evenements_cles[:3], 1):
            print(f"   {i}. {event.date} - {event.type_evenement}: {event.variation}")

    if data.actualites:
        print("\n📰 DERNIÈRES ACTUALITÉS:")
        for i, actu in enumerate(data.actualites[:3], 1):
            print(f"   {i}. {actu.date} - {actu.type_info}")
            print(f"      {actu.titre[:80]}...")

def extract_multiple_scpi():
    """Extrait les données de plusieurs SCPI"""
    start_time = time.time()

    print("🚀 EXTRACTION DES DONNÉES SCPI - MODE MULTIPLE")
    print("=" * 80)

    # Affichage du mode d'affichage
    mode_display = "🚫 Mode headless (fenêtre cachée)" if scraper_config.is_headless() else "👁️ Mode visible (fenêtre affichée)"
    print(f"🖥️ {mode_display}")
    print("   💡 Pour changer: python config_scraper.py --visible ou --headless")

    print(f"\n📋 {len(SCPI_LIST)} SCPI à traiter:")
    for scpi in SCPI_LIST:
        print(f"   • {scpi['nom']} (ID: {scpi['id']})")

    results = {}
    successful_extractions = 0
    failed_extractions = 0

    for index, scpi_info in enumerate(SCPI_LIST, 1):
        print_scpi_header(scpi_info, index, len(SCPI_LIST))

        try:
            print(f"🔍 Extraction en cours...")

            # Extraire les données pour cette SCPI
            data = scrape_scpi_data(scpi_info['id'])

            if data:
                print_scpi_results(data)
                results[scpi_info['nom']] = data
                successful_extractions += 1
                print(f"\n✅ Extraction réussie pour {scpi_info['nom']}")
            else:
                print(f"\n❌ Aucune donnée extraite pour {scpi_info['nom']}")
                failed_extractions += 1

        except Exception as e:
            print(f"\n❌ ERREUR lors de l'extraction de {scpi_info['nom']}:")
            print(f"   {str(e)}")
            failed_extractions += 1

        # Pause entre les extractions pour éviter la surcharge
        if index < len(SCPI_LIST):
            print("\n⏳ Pause de 2 secondes avant la prochaine extraction...")
            time.sleep(2)

    # Résumé final
    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "=" * 80)
    print("📈 RÉSUMÉ DE L'EXTRACTION MULTIPLE")
    print("=" * 80)
    print(f"✅ Extractions réussies: {successful_extractions}/{len(SCPI_LIST)}")
    print(f"❌ Extractions échouées: {failed_extractions}/{len(SCPI_LIST)}")
    print(f"⏱️  Temps total d'exécution: {duration:.2f} secondes")

    if results:
        print("\n💼 COMPARAISON RAPIDE:")
        print("-" * 80)
        print(f"{'SCPI':<25} {'Prix Achat':<12} {'Prix Vente':<12} {'Distrib. Brute':<15}")
        print("-" * 80)
        for nom, data in results.items():
            prix_achat = data.chiffres_cles.prix_part_actuel or "N/A"
            prix_vente = data.chiffres_cles.prix_part_vente or "N/A"
            distrib = f"{data.chiffres_cles.taux_distribution_brut}%" if data.chiffres_cles.taux_distribution_brut else "N/A"
            print(f"{nom:<25} {prix_achat:<12} {prix_vente:<12} {distrib:<15}")

    return results

def main():
    """Fonction principale d'extraction - SCPI unique"""
    start_time = time.time()

    print("🚀 EXTRACTION DES DONNÉES SCPI - MODE UNIQUE")
    print("=" * 50)

    # Affichage du mode d'affichage
    mode_display = "🚫 Mode headless (fenêtre cachée)" if scraper_config.is_headless() else "👁️ Mode visible (fenêtre affichée)"
    print(f"🖥️ {mode_display}")
    print("   💡 Pour changer: python config_scraper.py --visible ou --headless")

    # ID de la SCPI à extraire (par défaut PFO2)
    scpi_id = 85

    # Vérifier si un ID est passé en argument
    if len(sys.argv) > 1:
        try:
            scpi_id = int(sys.argv[1])
            print(f"📋 SCPI ID spécifié: {scpi_id}")
        except ValueError:
            print("⚠️ ID invalide, utilisation de l'ID par défaut (85)")

    try:
        print(f"\n🔍 Extraction des données pour la SCPI ID {scpi_id}...")

        # Utiliser le scraper optimisé
        data = scrape_scpi_data(scpi_id)

        # Afficher les résultats
        print("\n" + "=" * 50)
        print("📊 RÉSULTATS DE L'EXTRACTION")
        print("=" * 50)

        data.print_summary()
        print_scpi_results(data)

        print("\n✅ Extraction terminée avec succès!")

        return data

    except Exception as e:
        print("\n❌ ERREUR lors de l'extraction:")
        print(f"   {str(e)}")
        return None
    finally:
        end_time = time.time()
        duration = end_time - start_time
        print(f"\n⏱️  Temps d'exécution: {duration:.2f} secondes.")

def extraction_rapide():
    """Extraction rapide avec affichage minimal"""
    start_time = time.time()
    try:
        data = scrape_scpi_data(39)
        print(f"EPARGNE FONCIERE - Prix: {data.chiffres_cles.prix_part_actuel}€ - Distribution: {data.chiffres_cles.taux_distribution_brut}%")
        return data
    except Exception as e:
        print(f"Erreur: {e}")
        return None
    finally:
        end_time = time.time()
        duration = end_time - start_time
        print(f"⏱️  Temps d'exécution (rapide): {duration:.2f} secondes.")

if __name__ == "__main__":
    # Vérifier les arguments de ligne de commande
    if len(sys.argv) > 1:
        if sys.argv[1] == "--quick":
            extraction_rapide()
        elif sys.argv[1] == "--multiple" or sys.argv[1] == "--multi":
            extract_multiple_scpi()
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("🚀 SCPI SCRAPER - MODES D'UTILISATION")
            print("=" * 50)
            print("python main.py                    # Mode unique (SCPI par défaut ou ID spécifié)")
            print("python main.py [ID]               # Mode unique avec ID spécifique")
            print("python main.py --multiple         # Mode multiple (toutes les SCPI configurées)")
            print("python main.py --multi            # Alias pour --multiple")
            print("python main.py --quick            # Mode rapide (EPARGNE FONCIERE uniquement)")
            print("python main.py --help             # Affiche cette aide")
            print("\n📋 SCPI configurées pour le mode multiple:")
            for scpi in SCPI_LIST:
                print(f"   • {scpi['nom']} (ID: {scpi['id']})")
        else:
            # Essayer de parser comme un ID de SCPI
            try:
                scpi_id = int(sys.argv[1])
                main()
            except ValueError:
                print("❌ Argument invalide. Utilisez --help pour voir les options disponibles.")
    else:
        # Mode par défaut : extraction unique
        main()