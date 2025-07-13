#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script principal pour l'extraction des données SCPI
Utilise les scrapers améliorés avec sélecteurs dynamiques
"""

from scpi_scraper import scrape_scpi_data
from config_scraper import scraper_config
import sys

def main():
    """Fonction principale d'extraction"""

    print("🚀 EXTRACTION DES DONNÉES SCPI")
    print("=" * 50)

    # Affichage du mode d'affichage
    mode_display = "🚫 Mode headless (fenêtre cachée)" if scraper_config.is_headless() else "👁️ Mode visible (fenêtre affichée)"
    print(f"🖥️ {mode_display}")
    print("   💡 Pour changer: python config_scraper.py --visible ou --headless")

    # ID de la SCPI à extraire (par défaut EPARGNE FONCIERE)
    scpi_id = 39

    # Vérifier si un ID est passé en argument
    if len(sys.argv) > 1:
        try:
            scpi_id = int(sys.argv[1])
            print(f"📋 SCPI ID spécifié: {scpi_id}")
        except ValueError:
            print("⚠️ ID invalide, utilisation de l'ID par défaut (39)")

    try:
        print(f"\n🔍 Extraction des données pour la SCPI ID {scpi_id}...")

        # Utiliser le scraper optimisé
        data = scrape_scpi_data(scpi_id)

        # Afficher les résultats
        print("\n" + "=" * 50)
        print("📊 RÉSULTATS DE L'EXTRACTION")
        print("=" * 50)

        data.print_summary()

        # Afficher les informations clés
        print("\n💰 INFORMATIONS FINANCIÈRES:")
        print(f"   Prix de part: {data.chiffres_cles.prix_part_actuel}€")
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

        print("\n✅ Extraction terminée avec succès!")

        return data

    except Exception as e:
        print("\n❌ ERREUR lors de l'extraction:")
        print(f"   {str(e)}")
        return None

def extraction_rapide():
    """Extraction rapide avec affichage minimal"""
    try:
        data = scrape_scpi_data(39)
        print(f"EPARGNE FONCIERE - Prix: {data.chiffres_cles.prix_part_actuel}€ - Distribution: {data.chiffres_cles.taux_distribution_brut}%")
        return data
    except Exception as e:
        print(f"Erreur: {e}")
        return None

if __name__ == "__main__":
    # Vérifier si l'argument --quick est passé
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        extraction_rapide()
    else:
        main()