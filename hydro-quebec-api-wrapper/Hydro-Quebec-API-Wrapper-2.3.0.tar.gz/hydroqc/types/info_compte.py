"""Info compte json output formats."""
# pylint: disable=invalid-name
from enum import Enum, IntEnum
from typing import Any, TypedDict


# https://cl-services.idp.hydroquebec.com/cl/prive/api/v1_0/relations
class ComptesTyping(TypedDict, total=True):
    """Comptes json output format."""

    noPartenaireDemandeur: str
    nom1Demandeur: str
    nom2Demandeur: str
    noPartenaireTitulaire: str
    nom1Titulaire: str
    nom2Titulaire: str
    typeRelation: str
    indEcActif: bool
    indFavori: bool
    nickname: str
    actif: bool | None  # Could be not present
    dateDebutRelation: str | None  # Could be not present
    dateFinRelation: str | None  # Could be not present


# .../cl/prive/api/v3_0/partenaires/infoCompte
class listeComptesContratsTyping(TypedDict, total=True):
    """Info compte json sub output format."""

    titulaire: str
    nomTitulaire: str
    prenomTitulaire: str
    raisonSocialeTitulaire1: str
    raisonSocialeTitulaire2: str
    nomGroupeTitulaire1: str
    nomGroupeTitulaire2: str
    categorieTitulaire: str
    adresse: str
    modeEncaissement: str
    payeurDivergent: str
    dateEmission: str
    montantEchu: float
    typeMVE: str
    indContrats: bool
    indFinEventuelleCC: bool
    typeRelation: str
    indDonneesErreur: bool
    factureIXOSID: str
    documentArchivelinkID: str
    dateFin: str | None
    dateDebug: str | None
    indicateurPA: bool
    compteBancaire: str | None
    adresseFacturation: str
    regroupement: str
    listePaiements: list[str]
    noCompteContrat: str
    dateEcheance: str
    montant: float
    solde: float
    soldeEnSouffrance: float
    dernierMontantPaye: float
    contientPaiementsPostDates: bool
    coche: bool
    listeNoContrat: list[str]
    dateProchaineFacture: str
    typeDateProchaineFacture: str
    segmentation: str
    sousConsommationMVE: bool
    surConsommationMVE: bool
    revisionAnnuelleMVE: bool
    infoEligibiliteConfirmationPaiement: str | None
    noPartenaireMandataire: str | None
    infoEligibiliteEntentePaiement: str | None
    infoEligibiliteConfirmPaiementOuEntente: str | None
    indProjection: bool
    typeEntenteSansProjection: str
    gereDansEspaceClient: bool
    idBanque: str
    institution: str
    succursale: str
    folio: str
    libelle: str
    indBloquerPI: bool


class infoCockpitPourPartenaireModelTyping(TypedDict, total=True):
    """Info compte json output formats."""

    noPartenaire: str
    nom: str
    idTechnique: str
    prenom: str
    courriel: str
    segmentation: str
    categorie: str
    raisonSociale1: str
    raisonSociale2: str
    langueCorrespondance: str
    indPagePersonnelleActive: bool
    indFactureInternet: bool
    indPaiementInternet: bool
    indAucunCompteContrat: bool
    indDonneesConsommation: bool
    dateDerniereVisite: str
    etatFacturePapier: str
    listeComptesContrats: list[listeComptesContratsTyping]


class listeContratModelTyping(TypedDict, total=True):
    """Info compte json output formats."""

    codeResponsabilite: str | None
    noContrat: str
    adresseConsommation: str
    idLieuConsommation: str
    noCompteContrat: str
    noInstallation: str
    noCompteur: str
    indicateurPortrait: bool
    indicateurDiagnostique: bool
    indicateurDiagnostiqueDR: bool
    documentArchivelinkID: str
    codeDiagnostique: str
    codeDiagnostiqueDR: str
    indicateurAutoReleve: bool
    indicateurMVE: bool
    adhesionMVEEncours: bool
    retraitMVEEnCours: bool
    desinscritMVE: bool
    sousConsommationMVE: bool
    surConsommationMVE: bool
    mntEcart: float
    revisionAnnuelleMVE: bool
    indicateurEligibiliteMVE: bool
    codePortrait: str
    codeAutoReleve: str
    noCivique: str
    rue: str
    appartement: str
    ville: str
    codePostal: str
    dateDebutContrat: str
    dateFinContrat: str | None
    contratAvecArriveePrevue: bool
    contratAvecArriveePrevueDansLePasse: bool
    contratAvecDepartPrevu: bool
    contratAvecDepartPrevuDansLePasse: bool
    departPrevuSansAvis: bool
    numeroTelephone: str
    posteTelephone: str
    indPuissance: bool
    codeAdhesionCPC: str
    codeEligibiliteCPC: str | None
    codeEligibiliteCLT: str | None
    tarifActuel: str
    optionTarifActuel: str
    codeEligibiliteDRCV: str
    dateDebutEligibiliteDRCV: str | None
    indEligibiliteDRCV: bool


class InfoCompteTyping(TypedDict, total=True):
    """Info compte json output format."""

    indEligibilite: bool
    infoCockpitPourPartenaireModel: infoCockpitPourPartenaireModelTyping
    listeContratModel: list[listeContratModelTyping]
    listeInfoEligibiliteConfirmPaiementOuEntenteModel: list[Any]


class AccountContratTyping(TypedDict, total=True):
    """AccountContrat subelement of ContractSummaryTyping format."""

    noCompteContrat: str
    listeNoContrat: list[str]
    titulaire: str


class ContractSummaryTyping(TypedDict, total=True):
    """Contract Summary json output format."""

    nbContrats: int
    nbComptesContrats: int
    listeComptesContrats: dict[str, list[str]]
    comptesContrats: list[AccountContratTyping]


class ListContractsTyping(TypedDict, total=True):
    """Contract list json output format."""

    listeContrats: list[listeContratModelTyping]


# Outages

# Outage example
# [{"idLieuConso":"0500314629","etat":"N","date":"2023-01-04T03:25:40.000+00:00",
#   "interruptions":[{
#       "idInterruption":{"site":"ORL","typeObjet":"I","noInterruption":37224,"noSection":1},
#       "dateDebut":"2023-01-04T03:25:40.000+00:00",
#       "etat":"C",
#       "dateFinEstimeeMax":"2023-01-04T04:30:00.000+00:00",
#       "codeIntervention":"L","niveauUrgence":"P","nbClient":3,"codeCause":"51",
#       "codeMunicipal":"5557",
#       "datePublication":"2023-01-04T03:25:54.932+00:00","codeRemarque":"","dureePrevu":0,
#       "probabilite":0.0,"interruptionPlanifiee":false}]}]

# Planned outage example
# {'idLieuConso': '0502451550', 'etat': 'A', 'date': '2022-06-28T09:14:00.000+00:00',
#  'interruptions': [{
#       'idInterruption': {'site': 'LAV', 'typeObjet': 'A',
#                          'noInterruption': 117915, 'noSection': 1},
#       'dateDebut': '2022-12-21T13:30:00.000+00:00',
#       'dateFin': '2022-12-21T20:30:00.000+00:00',
#       'dateDebutReport': '2023-01-12T13:30:00.000+00:00',
#       'dateFinReport': '2023-01-12T20:30:00.000+00:00',
#       'etat': 'R', 'nbClient': 18, 'codeCause': '62', 'codeMunicipal': '9160',
#       'datePublication': '2022-12-20T16:02:52.920+00:00',
#       'codeRemarque': '91', 'dureePrevu': 420, 'probabilite': 0.0, 'interruptionPlanifiee': True
# }]}

# No outage example
# [{'idLieuConso': '0501706180', 'etat': 'A',
# 'date': '2022-10-20T19:50:13.000+00:00', 'interruptions': []}]


class OutageCause(IntEnum):
    """Outage cause enum."""

    # Unkonwn (not official HQ code)
    inconnu = 0
    # Not planned
    defaillance = 11
    surcharge = 12
    montage = 13
    protection = 14
    non_qualite = 15
    foudre = 21
    precipitation = 22
    sinistre_naturel = 24
    vent = 25
    temperature_extreme = 26
    subtance_sel = 31
    pollution_industriel = 32
    vetuste = 33
    indencie_fuite_de_gaz = 34
    erreur_de_manoeuvre = 41
    contact_accidentel = 42
    essai = 43
    man_sec_non_plan = 44
    vegetation = 51
    oiseau = 52
    animal = 53
    vehicule = 54
    objet = 55
    vandalisme = 56
    equipement_client = 57
    indetermine = 58
    non_fournie = 59
    # Planned
    entretien = 61
    modification_reseau = 62
    travaux_securitaire = 63
    manoeuvre_securitaire = 64
    manoeuvre = 65
    securite_public = 66
    interruption_demande_client = 76
    reforcement_de_reseau = 68
    programme_special = 69


# TODO use strEnum on python 3.11
class OutageStatus(Enum):
    """Outage status enum."""

    # Unkonwn (not official HQ code)
    inconnu = "_"
    travaux_assignes = "A"
    equipe_au_travail = "L"
    equipe_en_route = "R"


class OutageIdTyping(TypedDict, total=True):
    """Outage id json output format."""

    site: str
    typeObjet: str
    noInterruption: int
    noSection: int


class OutageTyping(TypedDict, total=True):
    """Outage json output format."""

    idInterruption: OutageIdTyping
    dateDebut: str
    dateFin: str
    dateDebutReport: str
    dateFinReport: str
    dateFinEstimeeMax: str
    etat: str
    nbClient: int
    codeCause: OutageCause
    codeIntervention: OutageStatus | None
    codeMunicipal: str
    datePublication: str
    codeRemarque: str
    dureePrevu: int  # minutes
    probabilite: float  # 0.0
    interruptionPlanifiee: bool
    niveauUrgence: str | None


class OutageListTyping(TypedDict, total=True):
    """Outage list json output format."""

    idLieuConso: str
    etat: str
    date: str
    interruptions: list[OutageTyping]
