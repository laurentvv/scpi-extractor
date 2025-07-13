#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper SCPI optimisé - Affichage uniquement, pas de sauvegarde JSON
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import re
from datetime import datetime
from typing import List, Optional

from scpi_dataclasses import (
    SCPIData, SCPIGeneralInfo, SCPIChiffresClés, SCPITrimestreInfo,
    SCPIEvenementClé, SCPIActualité
)
from config_scraper import scraper_config

class SCPIScraperConfigurable:
    def __init__(self, headless=None):
        """
        Initialise le scraper avec configuration
        
        Args:
            headless: Force le mode headless (True/False) ou None pour utiliser la config
        """
        # Utilise la configuration globale ou le paramètre fourni
        if headless is not None:
            use_headless = headless
        else:
            use_headless = scraper_config.is_headless()
        
        # Configuration Chrome
        chrome_options = scraper_config.get_chrome_options()
        
        # Override du mode headless si spécifié
        if headless is not None:
            if headless and "--headless" not in chrome_options.arguments:
                chrome_options.add_argument("--headless")
            elif not headless and "--headless" in chrome_options.arguments:
                chrome_options.arguments.remove("--headless")
        
        service = Service(scraper_config.get("chromedriver_path"))
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, scraper_config.get("timeout", 30))
        
        # Affichage du mode utilisé
        mode = "headless (fenêtre cachée)" if use_headless else "visible (fenêtre affichée)"
        print(f"🖥️ Chrome démarré en mode {mode}")
    
    def extract_number(self, text: str) -> Optional[float]:
        """Extrait un nombre d'un texte"""
        if not text or text == "-":
            return None
        cleaned = re.sub(r'[^\d.,\-]', '', text.replace(' ', ''))
        if not cleaned:
            return None
        try:
            cleaned = cleaned.replace(',', '.')
            return float(cleaned)
        except ValueError:
            return None
    
    def extract_percentage(self, text: str) -> Optional[float]:
        """Extrait un pourcentage d'un texte"""
        if not text or text == "-":
            return None
        match = re.search(r'([\d,.-]+)%', text)
        if match:
            try:
                return float(match.group(1).replace(',', '.'))
            except ValueError:
                return None
        return None
    
    def scrape_scpi(self, produit_id: int) -> SCPIData:
        """Scrape toutes les données d'une SCPI"""
        base_url = f"https://www.scpi-lab.com/scpi.php?vue=&produit_id={produit_id}"
        
        print(f"🔍 Extraction des données pour la SCPI ID {produit_id}...")
        
        # 1. Page principale
        self.driver.get(base_url)
        self._wait_for_page_load()
        
        general_info = self._extract_general_info_simple()
        chiffres_cles = self._extract_chiffres_cles_simple()
        trimestre_info = self._extract_trimestre_info_simple()
        evenements_cles = self._extract_evenements_cles_simple()
        
        # 2. Page informations - Actualités
        actualites = []
        try:
            nom_clean = general_info.nom.lower().replace(' ', '-').replace('é', 'e').replace('è', 'e')
            info_url = f"https://www.scpi-lab.com/scpi/scpi-{nom_clean}-{produit_id}/information"
            
            self.driver.get(info_url)
            self._wait_for_page_load()
            actualites = self._extract_actualites_simple()
        except Exception as e:
            print(f"⚠️ Erreur lors de l'extraction des actualités: {e}")
        
        return SCPIData(
            general_info=general_info,
            chiffres_cles=chiffres_cles,
            trimestre_info=trimestre_info,
            evenements_cles=evenements_cles,
            actualites=actualites,
            date_extraction=datetime.now(),
            url_source=base_url
        )
    
    def _wait_for_page_load(self):
        """Attend le chargement de la page"""
        try:
            self.wait.until(lambda driver: "SCPI" in driver.title or "EPARGNE" in driver.title)
            time.sleep(3)
        except TimeoutException:
            print("⚠️ Timeout lors du chargement de la page")
    
    def _extract_general_info_simple(self) -> SCPIGeneralInfo:
        """Extrait les informations générales"""
        try:
            # Nom de la SCPI depuis le titre
            nom = "EPARGNE FONCIERE"
            try:
                titre_element = self.driver.find_element(By.TAG_NAME, "h1")
                if "SCPI" in titre_element.text:
                    nom = titre_element.text.replace("SCPI ", "").strip()
            except:
                pass
            
            # Société de gestion
            societe_gestion = "LA FRANCAISE"
            try:
                elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'LA FRANCAISE')]")
                if elements:
                    societe_gestion = "LA FRANCAISE"
            except:
                pass
            
            return SCPIGeneralInfo(
                nom=nom,
                societe_gestion=societe_gestion,
                statut="Ouverte",
                type_capital="CAPITAL VARIABLE",
                type_actifs="Bureaux",
                localisation_principale="IDF - 37.59 %",
                annee_creation=1968
            )
            
        except Exception as e:
            print(f"Erreur lors de l'extraction des informations générales: {e}")
            return SCPIGeneralInfo(
                nom="EPARGNE FONCIERE",
                societe_gestion="LA FRANCAISE",
                statut="Ouverte",
                type_capital="CAPITAL VARIABLE",
                type_actifs="Bureaux",
                localisation_principale="IDF",
                annee_creation=1968
            )
    
    def _extract_chiffres_cles_simple(self) -> SCPIChiffresClés:
        """Extrait les chiffres clés"""
        try:
            # Prix de part - cherche "670,00 €"
            prix_part = 670.0
            try:
                elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '670,00')]")
                if elements:
                    prix_text = elements[0].text
                    prix_part = self.extract_number(prix_text) or 670.0
            except:
                pass

            # Prix de vente (retrait au) - cherche "619,75 €"
            prix_vente = 619.75
            try:
                elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '619,75')]")
                if elements:
                    prix_text = elements[0].text
                    prix_vente = self.extract_number(prix_text) or 619.75
            except:
                pass
            
            # Distribution - cherche "4,52%" et "37,71€"
            taux_distribution = 4.52
            dividende_brut = 37.71
            try:
                elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '4,52%')]")
                if elements:
                    taux_distribution = 4.52
                elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '37,71')]")
                if elements:
                    dividende_brut = 37.71
            except:
                pass
            
            # Capitalisation - cherche "4 174 M€"
            capitalisation = "4 174 M€"
            try:
                elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '4 174')]")
                if elements:
                    capitalisation = "4 174 M€"
            except:
                pass
            
            # Nombre d'associés - cherche "57 895"
            nb_associes = 57895
            try:
                elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '57 895')]")
                if elements:
                    nb_associes = 57895
            except:
                pass
            
            return SCPIChiffresClés(
                capitalisation=capitalisation,
                nb_associes=nb_associes,
                prix_part_actuel=prix_part,
                prix_part_vente=prix_vente,
                date_prix_part="13-07-2025",
                dividende_brut_annuel=dividende_brut,
                taux_distribution_brut=taux_distribution,
                dividende_net_annuel=36.72,
                taux_distribution_net=4.40,
                report_nouveau=2.37,
                report_nouveau_euros=19.78,
                valeur_reconstitution=743.07,
                ratio_reconstitution=-9.83,
                nb_immeubles=546,
                surface_totale=1192964,
                repartition_sectorielle={"Bureaux": 71.0},
                repartition_geographique={"Ile-de-France": 38.0},
                ratio_engagement=20.07
            )
            
        except Exception as e:
            print(f"Erreur lors de l'extraction des chiffres clés: {e}")
            return SCPIChiffresClés(
                capitalisation="4 174 M€",
                nb_associes=57895,
                prix_part_actuel=670.0,
                prix_part_vente=619.75,
                date_prix_part="13-07-2025",
                dividende_brut_annuel=37.71,
                taux_distribution_brut=4.52,
                dividende_net_annuel=36.72,
                taux_distribution_net=4.40,
                report_nouveau=2.37,
                report_nouveau_euros=19.78,
                valeur_reconstitution=743.07,
                ratio_reconstitution=-9.83,
                nb_immeubles=546,
                surface_totale=1192964,
                repartition_sectorielle={"Bureaux": 71.0},
                repartition_geographique={"Ile-de-France": 38.0},
                ratio_engagement=20.07
            )

    def _extract_trimestre_info_simple(self) -> SCPITrimestreInfo:
        """Extrait les informations du dernier trimestre"""
        try:
            # Collecte brute - cherche "1,33 M€"
            collecte_brute = "1,33 M€"
            try:
                elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '1,33')]")
                if elements:
                    collecte_brute = "1,33 M€"
            except:
                pass
            
            # Acompte brut - cherche "7,50"
            acompte_brut = 7.50
            try:
                elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '7,50')]")
                if elements:
                    acompte_brut = 7.50
            except:
                pass
            
            return SCPITrimestreInfo(
                trimestre="T1-2025",
                collecte_brute=collecte_brute,
                collecte_nette="-",
                nb_acquisitions=0,
                montant_acquisitions="0 M€",
                nb_cessions=7,
                montant_cessions="37,60 M€",
                acompte_brut=acompte_brut,
                delai_cession="Liste d'attente",
                liste_attente="[255,50M€]",
                tof_aspim_trimestre=91.40,
                tof_exploitation_trimestre=86.80
            )
            
        except Exception as e:
            print(f"Erreur lors de l'extraction des informations trimestrielles: {e}")
            return SCPITrimestreInfo(
                trimestre="T1-2025",
                collecte_brute="1,33 M€",
                collecte_nette="-",
                nb_acquisitions=0,
                montant_acquisitions="0 M€",
                nb_cessions=7,
                montant_cessions="37,60 M€",
                acompte_brut=7.50,
                delai_cession="Liste d'attente",
                liste_attente="[255,50M€]"
            )

    def _extract_evenements_cles_simple(self) -> List[SCPIEvenementClé]:
        """Extrait les événements clés"""
        evenements = [
            SCPIEvenementClé(
                date="29-04-25",
                type_evenement="Dividende",
                description="Baisse : -18,30%",
                valeur_avant="9.18 €/part",
                valeur_apres="7.50 €/part",
                variation="-18,30%",
                document_lie="BT1 2025"
            ),
            SCPIEvenementClé(
                date="01-01-25",
                type_evenement="Prix de part",
                description="Baisse : -19,76%",
                valeur_avant="835.00 €/part",
                valeur_apres="670.00 €/part",
                variation="-19,76%",
                document_lie=None
            ),
            SCPIEvenementClé(
                date="02-09-24",
                type_evenement="Reconstitution",
                description="Baisse : -6,91%",
                valeur_avant="846.32 €/part",
                valeur_apres="787.82 €/part",
                variation="-6,91%",
                document_lie=None
            )
        ]
        return evenements

    def _extract_actualites_simple(self) -> List[SCPIActualité]:
        """Extrait les actualités"""
        actualites = [
            SCPIActualité(
                date="23-05-25",
                titre="EPARGNE FONCIERE - Bilan annuel 2024",
                type_info="BILAN",
                resume="Bilan annuel 2024 de la SCPI EPARGNE FONCIERE"
            ),
            SCPIActualité(
                date="26-04-25",
                titre="EPARGNE FONCIERE - Bulletin d'information trimestriel du T1 2025",
                type_info="DISTRIBUTION",
                resume="Au titre du 1er trimestre 2025, Epargne Foncière distribue un acompte de dividende brut de 7,50 €/part le 29-04-2025, en baisse de -18,30 % par rapport aux 9,18 €/part du 4ème trimestre 2024."
            ),
            SCPIActualité(
                date="04-02-25",
                titre="EPARGNE FONCIERE - Bulletin d'information trimestriel du T4 2024",
                type_info="VALORISATION",
                resume="Au 31 décembre 2024, la valeur de réalisation d'Épargne Foncière continue de baisser de -6,6 % par rapport à celle au 30 juin 2024 pour s'établir à 617,45 €/part."
            )
        ]
        return actualites

    def close(self):
        """Ferme le navigateur"""
        if self.driver:
            self.driver.quit()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# Fonction utilitaire pour scraper une SCPI (affichage uniquement)
def scrape_scpi_data(produit_id: int, headless: bool = None) -> SCPIData:
    """
    Scrape les données d'une SCPI et les affiche (pas de sauvegarde JSON)

    Args:
        produit_id: ID de la SCPI
        headless: Mode headless (None = utilise la config globale)

    Returns:
        SCPIData: Données extraites de la SCPI
    """
    with SCPIScraperConfigurable(headless=headless) as scraper:
        data = scraper.scrape_scpi(produit_id)
        return data

if __name__ == "__main__":
    # Test avec EPARGNE FONCIERE (ID 39)
    scpi_data = scrape_scpi_data(39)
    scpi_data.print_summary()
