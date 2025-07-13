from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class SCPIGeneralInfo:
    """Informations générales de la SCPI"""
    nom: str
    societe_gestion: str
    statut: str  # Ex: "Ouverte", "Fermée"
    type_capital: str  # Ex: "CAPITAL VARIABLE", "CAPITAL FIXE"
    type_actifs: str  # Ex: "Bureaux", "Commerces"
    localisation_principale: str  # Ex: "IDF - 37.59 %"
    annee_creation: int
    agrement_amf: Optional[str] = None
    telephone_contact: Optional[str] = None
    email_contact: Optional[str] = None

@dataclass
class SCPIChiffresClés:
    """Chiffres clés de la SCPI"""
    # Capitalisation et parts
    capitalisation: str  # Ex: "4 174 M€"
    nb_associes: int
    prix_part_actuel: float  # En euros (prix d'achat)
    prix_part_vente: float  # En euros (prix de vente/retrait)
    date_prix_part: str
    
    # Distribution
    dividende_brut_annuel: float  # En euros par part
    taux_distribution_brut: float  # En pourcentage
    dividende_net_annuel: float  # En euros par part
    taux_distribution_net: float  # En pourcentage
    
    # Valorisation
    report_nouveau: float  # En pourcentage
    report_nouveau_euros: float  # En euros par part
    valeur_reconstitution: float  # En euros
    ratio_reconstitution: float  # En pourcentage
    
    # Patrimoine
    nb_immeubles: int
    surface_totale: int  # En m²
    repartition_sectorielle: dict  # Ex: {"Bureaux": 71, "Commerces": 20}
    repartition_geographique: dict  # Ex: {"Ile-de-France": 38, "Regions": 45}
    
    # Ratios
    ratio_engagement: float  # En pourcentage
    tof_aspim: Optional[float] = None  # En pourcentage
    tof_exploitation: Optional[float] = None  # En pourcentage

@dataclass
class SCPITrimestreInfo:
    """Informations du dernier trimestre"""
    trimestre: str  # Ex: "T1-2025"
    
    # Collecte
    collecte_brute: str  # Ex: "1,33 M€"
    collecte_nette: str  # Ex: "-" ou montant
    
    # Transactions
    nb_acquisitions: int
    montant_acquisitions: str
    nb_cessions: int
    montant_cessions: str
    
    # Distribution
    acompte_brut: float  # En euros par part
    
    # Délai et liquidité
    delai_cession: str
    liste_attente: str  # Ex: "[255,50M€]"
    
    # Ratios trimestriels
    tof_aspim_trimestre: Optional[float] = None
    tof_exploitation_trimestre: Optional[float] = None

@dataclass
class SCPIEvenementClé:
    """Un événement clé de la SCPI"""
    date: str
    type_evenement: str  # Ex: "Dividende", "Prix de part", "Reconstitution"
    description: str  # Ex: "Baisse : -18,30%"
    valeur_avant: str  # Ex: "9.18 €/part"
    valeur_apres: str  # Ex: "7.50 €/part"
    variation: str  # Ex: "-18,30%"
    document_lie: Optional[str] = None  # Ex: "BT1 2025"

@dataclass
class SCPIActualité:
    """Une actualité/information de la SCPI"""
    date: str
    titre: str
    type_info: str  # Ex: "DISTRIBUTION", "VALORISATION", "SOUSCRIPTION"
    resume: str  # Résumé de l'actualité
    lien: Optional[str] = None  # Lien vers le document complet

@dataclass
class SCPIData:
    """Classe principale regroupant toutes les données d'une SCPI"""
    general_info: SCPIGeneralInfo
    chiffres_cles: SCPIChiffresClés
    trimestre_info: SCPITrimestreInfo
    evenements_cles: List[SCPIEvenementClé]
    actualites: List[SCPIActualité]
    
    # Métadonnées
    date_extraction: datetime
    url_source: str
    

    def print_summary(self):
        """Affiche un résumé des données extraites"""
        print(f"\n=== SCPI {self.general_info.nom} ===")
        print(f"Société de gestion: {self.general_info.societe_gestion}")
        print(f"Prix d'achat: {self.chiffres_cles.prix_part_actuel}€")
        print(f"Prix de vente: {self.chiffres_cles.prix_part_vente}€")
        print(f"Distribution brute 2024: {self.chiffres_cles.taux_distribution_brut}% ({self.chiffres_cles.dividende_brut_annuel}€)")
        print(f"Capitalisation: {self.chiffres_cles.capitalisation}")
        print(f"Nombre d'associés: {self.chiffres_cles.nb_associes:,}")
        print(f"\nDernier trimestre ({self.trimestre_info.trimestre}):")
        print(f"  Collecte brute: {self.trimestre_info.collecte_brute}")
        print(f"  Acompte distribué: {self.trimestre_info.acompte_brut}€/part")
        print(f"\nNombre d'événements clés: {len(self.evenements_cles)}")
        print(f"Nombre d'actualités: {len(self.actualites)}")
        print(f"\nExtraction effectuée le: {self.date_extraction.strftime('%d/%m/%Y %H:%M')}")
