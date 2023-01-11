# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://textgrid.info/namespaces/metadata/agent/2010"


class AgentRoleType(Enum):
    """
    The role a person or institution has for the object.

    Attributes
        ACTOR: Same as: http://id.loc.gov/vocabulary/relators/act
        ADAPTER: Same as: http://id.loc.gov/vocabulary/relators/adp
        ANALYST: Same as: http://id.loc.gov/vocabulary/relators/anl
        ANIMATOR: Same as: http://id.loc.gov/vocabulary/relators/anm
        ANNOTATOR: Same as: http://id.loc.gov/vocabulary/relators/ann
        APPLICANT: Same as: http://id.loc.gov/vocabulary/relators/app
        ARCHITECT: Same as: http://id.loc.gov/vocabulary/relators/arc
        ARRANGER: Same as: http://id.loc.gov/vocabulary/relators/arr
        ART_COPYIST: Same as: http://id.loc.gov/vocabulary/relators/acp
        ARTIST: Same as: http://id.loc.gov/vocabulary/relators/art
        ARTISTIC_DIRECTOR: Same as:
            http://id.loc.gov/vocabulary/relators/ard
        ASSIGNEE: Same as: http://id.loc.gov/vocabulary/relators/asg
        ASSOCIATED_NAME: Same as:
            http://id.loc.gov/vocabulary/relators/asn
        ATTRIBUTED_NAME: Same as:
            http://id.loc.gov/vocabulary/relators/att
        AUCTIONEER: Same as: http://id.loc.gov/vocabulary/relators/auc
        AUTHOR: Same as: http://id.loc.gov/vocabulary/relators/aut
        AUTHOR_IN_QUOTATIONS: Same as:
            http://id.loc.gov/vocabulary/relators/aqt
        AUTHOR_OF_AFTERWORD: Same as:
            http://id.loc.gov/vocabulary/relators/aft
        AUTHOR_OF_DIALOG: Same as:
            http://id.loc.gov/vocabulary/relators/aud
        AUTHOR_OF_INTRODUCTION: Same as:
            http://id.loc.gov/vocabulary/relators/aui
        AUTHOR_OF_SCREENPLAY: Same as:
            http://id.loc.gov/vocabulary/relators/aus
        BIBLIOGRAPHIC_ANTECEDENT: Same as:
            http://id.loc.gov/vocabulary/relators/ant
        BINDER: Same as: http://id.loc.gov/vocabulary/relators/bnd
        BINDING_DESIGNER: Same as:
            http://id.loc.gov/vocabulary/relators/bdd
        BLURB_WRITER: Same as: http://id.loc.gov/vocabulary/relators/blw
        BOOK_DESIGNER: Same as:
            http://id.loc.gov/vocabulary/relators/bkd
        BOOK_PRODUCER: Same as:
            http://id.loc.gov/vocabulary/relators/bkp
        BOOK_JACKET_DESIGNER: Same as:
            http://id.loc.gov/vocabulary/relators/bjd
        BOOKPLATE_DESIGNER: Same as:
            http://id.loc.gov/vocabulary/relators/bpd
        BOOKSELLER: Same as: http://id.loc.gov/vocabulary/relators/bsl
        CALLIGRAPHER: Same as: http://id.loc.gov/vocabulary/relators/cll
        CARTOGRAPHER: Same as: http://id.loc.gov/vocabulary/relators/ctg
        CENSOR: Same as: http://id.loc.gov/vocabulary/relators/cns
        CINEMATOGRAPHER: Same as:
            http://id.loc.gov/vocabulary/relators/cng
        CLIENT: Same as: http://id.loc.gov/vocabulary/relators/cli
        COLLABORATOR: Same as: http://id.loc.gov/vocabulary/relators/clb
        COLLECTOR: Same as: http://id.loc.gov/vocabulary/relators/col
        COLLOTYPER: Same as: http://id.loc.gov/vocabulary/relators/clt
        COLORIST: Same as: http://id.loc.gov/vocabulary/relators/clr
        COMMENTATOR: Same as: http://id.loc.gov/vocabulary/relators/cmm
        COMMENTATOR_FOR_WRITTEN_TEXT: Same as:
            http://id.loc.gov/vocabulary/relators/cwt
        COMPILER: Same as: http://id.loc.gov/vocabulary/relators/com
        COMPLAINANT: Same as: http://id.loc.gov/vocabulary/relators/cpl
        COMPLAINANT_APPELLANT: Same as:
            http://id.loc.gov/vocabulary/relators/cpt
        COMPLAINANT_APPELLEE: Same as:
            http://id.loc.gov/vocabulary/relators/cpe
        COMPOSER: Same as: http://id.loc.gov/vocabulary/relators/cmp
        COMPOSITOR: Same as: http://id.loc.gov/vocabulary/relators/cmt
        CONCEPTOR: Same as: http://id.loc.gov/vocabulary/relators/ccp
        CONDUCTOR: Same as: http://id.loc.gov/vocabulary/relators/cnd
        CONSERVATOR: Same as: http://id.loc.gov/vocabulary/relators/con
        CONSULTANT: Same as: http://id.loc.gov/vocabulary/relators/csl
        CONSULTANT_TO_PROJECT: Same as:
            http://id.loc.gov/vocabulary/relators/csp
        CONTESTANT: Same as: http://id.loc.gov/vocabulary/relators/cos
        CONTESTANT_APPELLANT: Same as:
            http://id.loc.gov/vocabulary/relators/cot
        CONTESTANT_APPELLEE: Same as:
            http://id.loc.gov/vocabulary/relators/coe
        CONTESTEE: Same as: http://id.loc.gov/vocabulary/relators/cts
        CONTESTEE_APPELLANT: Same as:
            http://id.loc.gov/vocabulary/relators/ctt
        CONTESTEE_APPELLEE: Same as:
            http://id.loc.gov/vocabulary/relators/cte
        CONTRACTOR: Same as: http://id.loc.gov/vocabulary/relators/ctr
        CONTRIBUTOR: Same as: http://id.loc.gov/vocabulary/relators/ctb
        COPYRIGHT_CLAIMANT: Same as:
            http://id.loc.gov/vocabulary/relators/cpc
        COPYRIGHT_HOLDER: Same as:
            http://id.loc.gov/vocabulary/relators/cph
        CORRECTOR: Same as: http://id.loc.gov/vocabulary/relators/crr
        CORRESPONDENT: Same as:
            http://id.loc.gov/vocabulary/relators/crp
        COSTUME_DESIGNER: Same as:
            http://id.loc.gov/vocabulary/relators/cst
        COVER_DESIGNER: Same as:
            http://id.loc.gov/vocabulary/relators/cov
        CREATOR: Same as: http://id.loc.gov/vocabulary/relators/cre
        CURATOR_OF_AN_EXHIBITION: Same as:
            http://id.loc.gov/vocabulary/relators/cur
        DANCER: Same as: http://id.loc.gov/vocabulary/relators/dnc
        DATA_CONTRIBUTOR: Same as:
            http://id.loc.gov/vocabulary/relators/dtc
        DATA_MANAGER: Same as: http://id.loc.gov/vocabulary/relators/dtm
        DEDICATEE: Same as: http://id.loc.gov/vocabulary/relators/dte
        DEDICATOR: Same as: http://id.loc.gov/vocabulary/relators/dto
        DEFENDANT: Same as: http://id.loc.gov/vocabulary/relators/dfd
        DEFENDANT_APPELLANT: Same as:
            http://id.loc.gov/vocabulary/relators/dft
        DEFENDANT_APPELLEE: Same as:
            http://id.loc.gov/vocabulary/relators/dfe
        DEGREE_GRANTOR: Same as:
            http://id.loc.gov/vocabulary/relators/dgg
        DELINEATOR: Same as: http://id.loc.gov/vocabulary/relators/dln
        DEPICTED: Same as: http://id.loc.gov/vocabulary/relators/dpc
        DEPOSITOR: Same as: http://id.loc.gov/vocabulary/relators/dpt
        DESIGNER: Same as: http://id.loc.gov/vocabulary/relators/dsr
        DIRECTOR: Same as: http://id.loc.gov/vocabulary/relators/drt
        DISSERTANT: Same as: http://id.loc.gov/vocabulary/relators/dis
        DISTRIBUTION_PLACE: Same as:
            http://id.loc.gov/vocabulary/relators/dbp
        DISTRIBUTOR: Same as: http://id.loc.gov/vocabulary/relators/dst
        DONOR: Same as: http://id.loc.gov/vocabulary/relators/dnr
        DRAFTSMAN: Same as: http://id.loc.gov/vocabulary/relators/drm
        DUBIOUS_AUTHOR: Same as:
            http://id.loc.gov/vocabulary/relators/dub
        EDITOR: Same as: http://id.loc.gov/vocabulary/relators/edt
        ELECTRICIAN: Same as: http://id.loc.gov/vocabulary/relators/elg
        ELECTROTYPER: Same as: http://id.loc.gov/vocabulary/relators/elt
        ENGINEER: Same as: http://id.loc.gov/vocabulary/relators/eng
        ENGRAVER: Same as: http://id.loc.gov/vocabulary/relators/egr
        ETCHER: Same as: http://id.loc.gov/vocabulary/relators/etr
        EVENT_PLACE: Same as: http://id.loc.gov/vocabulary/relators/evp
        EXPERT: Same as: http://id.loc.gov/vocabulary/relators/exp
        FACSIMILIST: Same as: http://id.loc.gov/vocabulary/relators/fac
        FIELD_DIRECTOR: Same as:
            http://id.loc.gov/vocabulary/relators/fld
        FILM_EDITOR: Same as: http://id.loc.gov/vocabulary/relators/flm
        FIRST_PARTY: Same as: http://id.loc.gov/vocabulary/relators/fpy
        FORGER: Same as: http://id.loc.gov/vocabulary/relators/frg
        FORMER_OWNER: Same as: http://id.loc.gov/vocabulary/relators/fmo
        FUNDER: Same as: http://id.loc.gov/vocabulary/relators/fnd
        GEOGRAPHIC_INFORMATION_SPECIALIST: Same as:
            http://id.loc.gov/vocabulary/relators/gis
        HONOREE: Same as: http://id.loc.gov/vocabulary/relators/hnr
        HOST: Same as: http://id.loc.gov/vocabulary/relators/hst
        ILLUMINATOR: Same as: http://id.loc.gov/vocabulary/relators/ilu
        ILLUSTRATOR: Same as: http://id.loc.gov/vocabulary/relators/ill
        INSCRIBER: Same as: http://id.loc.gov/vocabulary/relators/ins
        INSTRUMENTALIST: Same as:
            http://id.loc.gov/vocabulary/relators/itr
        INTERVIEWEE: Same as: http://id.loc.gov/vocabulary/relators/ive
        INTERVIEWER: Same as: http://id.loc.gov/vocabulary/relators/ivr
        INVENTOR: Same as: http://id.loc.gov/vocabulary/relators/inv
        LABORATORY: Same as: http://id.loc.gov/vocabulary/relators/lbr
        LABORATORY_DIRECTOR: Same as:
            http://id.loc.gov/vocabulary/relators/ldr
        LEAD: Same as: http://id.loc.gov/vocabulary/relators/led
        LANDSCAPE_ARCHITECT: Same as:
            http://id.loc.gov/vocabulary/relators/lsa
        LENDER: Same as: http://id.loc.gov/vocabulary/relators/len
        LIBELANT: Same as: http://id.loc.gov/vocabulary/relators/lil
        LIBELANT_APPELLANT: Same as:
            http://id.loc.gov/vocabulary/relators/lit
        LIBELANT_APPELLEE: Same as:
            http://id.loc.gov/vocabulary/relators/lie
        LIBELEE: Same as: http://id.loc.gov/vocabulary/relators/lel
        LIBELEE_APPELLANT: Same as:
            http://id.loc.gov/vocabulary/relators/let
        LIBELEE_APPELLEE: Same as:
            http://id.loc.gov/vocabulary/relators/lee
        LIBRETTIST: Same as: http://id.loc.gov/vocabulary/relators/lbt
        LICENSEE: Same as: http://id.loc.gov/vocabulary/relators/lse
        LICENSOR: Same as: http://id.loc.gov/vocabulary/relators/lso
        LIGHTING_DESIGNER: Same as:
            http://id.loc.gov/vocabulary/relators/lgd
        LITHOGRAPHER: Same as: http://id.loc.gov/vocabulary/relators/ltg
        LYRICIST: Same as: http://id.loc.gov/vocabulary/relators/lyr
        MANUFACTURER: Same as: http://id.loc.gov/vocabulary/relators/mfr
        MARBLER: Same as: http://id.loc.gov/vocabulary/relators/mrb
        MARKUP_EDITOR: Same as:
            http://id.loc.gov/vocabulary/relators/mrk
        METADATA_CONTACT: Same as:
            http://id.loc.gov/vocabulary/relators/mdc
        METALENGRAVER: Same as:
            http://id.loc.gov/vocabulary/relators/mte
        MODERATOR: Same as: http://id.loc.gov/vocabulary/relators/mod
        MONITOR: Same as: http://id.loc.gov/vocabulary/relators/mon
        MUSIC_COPYIST: Same as:
            http://id.loc.gov/vocabulary/relators/mcp
        MUSICAL_DIRECTOR: Same as:
            http://id.loc.gov/vocabulary/relators/msd
        MUSICIAN: Same as: http://id.loc.gov/vocabulary/relators/mus
        NARRATOR: Same as: http://id.loc.gov/vocabulary/relators/nrt
        OPPONENT: Same as: http://id.loc.gov/vocabulary/relators/opn
        ORGANIZER_OF_MEETING: Same as:
            http://id.loc.gov/vocabulary/relators/orm
        ORIGINATOR: Same as: http://id.loc.gov/vocabulary/relators/org
        OTHER: Same as: http://id.loc.gov/vocabulary/relators/oth
        OWNER: Same as: http://id.loc.gov/vocabulary/relators/own
        PAPERMAKER: Same as: http://id.loc.gov/vocabulary/relators/ppm
        PATENT_APPLICANT: Same as:
            http://id.loc.gov/vocabulary/relators/pta
        PATENT_HOLDER: Same as:
            http://id.loc.gov/vocabulary/relators/pth
        PATRON: Same as: http://id.loc.gov/vocabulary/relators/pat
        PERFORMER: Same as: http://id.loc.gov/vocabulary/relators/prf
        PERMITTING_AGENCY: Same as:
            http://id.loc.gov/vocabulary/relators/pma
        PHOTOGRAPHER: Same as: http://id.loc.gov/vocabulary/relators/pht
        PLAINTIFF: Same as: http://id.loc.gov/vocabulary/relators/ptf
        PLAINTIFF_APPELLANT: Same as:
            http://id.loc.gov/vocabulary/relators/ptt
        PLAINTIFF_APPELLEE: Same as:
            http://id.loc.gov/vocabulary/relators/pte
        PLATEMAKER: Same as: http://id.loc.gov/vocabulary/relators/plt
        PRINTER: Same as: http://id.loc.gov/vocabulary/relators/prt
        PRINTER_OF_PLATES: Same as:
            http://id.loc.gov/vocabulary/relators/pop
        PRINTMAKER: Same as: http://id.loc.gov/vocabulary/relators/prm
        PROCESS_CONTACT: Same as:
            http://id.loc.gov/vocabulary/relators/prc
        PRODUCER: Same as: http://id.loc.gov/vocabulary/relators/pro
        PRODUCTION_MANAGER: Same as:
            http://id.loc.gov/vocabulary/relators/pmm
        PRODUCTION_PERSONNEL: Same as:
            http://id.loc.gov/vocabulary/relators/prd
        PROGRAMMER: Same as: http://id.loc.gov/vocabulary/relators/prg
        PROJECT_DIRECTOR: Same as:
            http://id.loc.gov/vocabulary/relators/pdr
        PROOFREADER: Same as: http://id.loc.gov/vocabulary/relators/pfr
        PUBLICATION_PLACE: Same as:
            http://id.loc.gov/vocabulary/relators/pup
        PUBLISHER: Same as: http://id.loc.gov/vocabulary/relators/pbl
        PUBLISHING_DIRECTOR: Same as:
            http://id.loc.gov/vocabulary/relators/pbd
        PUPPETEER: Same as: http://id.loc.gov/vocabulary/relators/ppt
        RECIPIENT: Same as: http://id.loc.gov/vocabulary/relators/rcp
        RECORDING_ENGINEER: Same as:
            http://id.loc.gov/vocabulary/relators/rce
        REDACTOR: Same as: http://id.loc.gov/vocabulary/relators/red
        RENDERER: Same as: http://id.loc.gov/vocabulary/relators/ren
        REPORTER: Same as: http://id.loc.gov/vocabulary/relators/rpt
        REPOSITORY: Same as: http://id.loc.gov/vocabulary/relators/rps
        RESEARCH_TEAM_HEAD: Same as:
            http://id.loc.gov/vocabulary/relators/rth
        RESEARCH_TEAM_MEMBER: Same as:
            http://id.loc.gov/vocabulary/relators/rtm
        RESEARCHER: Same as: http://id.loc.gov/vocabulary/relators/res
        RESPONDENT: Same as: http://id.loc.gov/vocabulary/relators/rsp
        RESPONDENT_APPELLANT: Same as:
            http://id.loc.gov/vocabulary/relators/rst
        RESPONDENT_APPELLEE: Same as:
            http://id.loc.gov/vocabulary/relators/rse
        RESPONSIBLE_PARTY: Same as:
            http://id.loc.gov/vocabulary/relators/rpy
        RESTAGER: Same as: http://id.loc.gov/vocabulary/relators/rsg
        REVIEWER: Same as: http://id.loc.gov/vocabulary/relators/rev
        RUBRICATOR: Same as: http://id.loc.gov/vocabulary/relators/rbr
        SCENARIST: Same as: http://id.loc.gov/vocabulary/relators/sce
        SCIENTIFIC_ADVISOR: Same as:
            http://id.loc.gov/vocabulary/relators/sad
        SCRIBE: Same as: http://id.loc.gov/vocabulary/relators/scr
        SCULPTOR: Same as: http://id.loc.gov/vocabulary/relators/scl
        SECOND_PARTY: Same as: http://id.loc.gov/vocabulary/relators/spy
        SECRETARY: Same as: http://id.loc.gov/vocabulary/relators/sec
        SETDESIGNER: Same as: http://id.loc.gov/vocabulary/relators/std
        SIGNER: Same as: http://id.loc.gov/vocabulary/relators/sgn
        SINGER: Same as: http://id.loc.gov/vocabulary/relators/sng
        SOUND_DESIGNER: Same as:
            http://id.loc.gov/vocabulary/relators/sds
        SPEAKER: Same as: http://id.loc.gov/vocabulary/relators/spk
        SPONSOR: Same as: http://id.loc.gov/vocabulary/relators/spn
        STAGE_MANAGER: Same as:
            http://id.loc.gov/vocabulary/relators/stm
        STANDARDS_BODY: Same as:
            http://id.loc.gov/vocabulary/relators/stn
        STEREOTYPER: Same as: http://id.loc.gov/vocabulary/relators/str
        STORYTELLER: Same as: http://id.loc.gov/vocabulary/relators/stl
        SUPPORTING_HOST: Same as:
            http://id.loc.gov/vocabulary/relators/sht
        SURVEYOR: Same as: http://id.loc.gov/vocabulary/relators/srv
        TEACHER: Same as: http://id.loc.gov/vocabulary/relators/tch
        TECHNICAL_DIRECTOR: Same as:
            http://id.loc.gov/vocabulary/relators/tcd
        THESIS_ADVISOR: Same as:
            http://id.loc.gov/vocabulary/relators/ths
        TRANSCRIBER: Same as: http://id.loc.gov/vocabulary/relators/trc
        TRANSLATOR: Same as: http://id.loc.gov/vocabulary/relators/trl
        TYPE_DESIGNER: Same as:
            http://id.loc.gov/vocabulary/relators/tyd
        TYPOGRAPHER: Same as: http://id.loc.gov/vocabulary/relators/tyg
        UNIVERSITY_PLACE: Same as:
            http://id.loc.gov/vocabulary/relators/uvp
        VIDEOGRAPHER: Same as: http://id.loc.gov/vocabulary/relators/vdg
        VOCALIST: Same as: http://id.loc.gov/vocabulary/relators/voc
        WITNESS: Same as: http://id.loc.gov/vocabulary/relators/wit
        WOOD_ENGRAVER: Same as:
            http://id.loc.gov/vocabulary/relators/wde
        WOODCUTTER: Same as: http://id.loc.gov/vocabulary/relators/wdc
        WRITER_OF_ACCOMPANYING_MATERIAL: Same as:
            http://id.loc.gov/vocabulary/relators/wam
    """
    ACTOR = "actor"
    ADAPTER = "adapter"
    ANALYST = "analyst"
    ANIMATOR = "animator"
    ANNOTATOR = "annotator"
    APPLICANT = "applicant"
    ARCHITECT = "architect"
    ARRANGER = "arranger"
    ART_COPYIST = "artCopyist"
    ARTIST = "artist"
    ARTISTIC_DIRECTOR = "artisticDirector"
    ASSIGNEE = "assignee"
    ASSOCIATED_NAME = "associatedName"
    ATTRIBUTED_NAME = "attributedName"
    AUCTIONEER = "auctioneer"
    AUTHOR = "author"
    AUTHOR_IN_QUOTATIONS = "authorInQuotations"
    AUTHOR_OF_AFTERWORD = "authorOfAfterword"
    AUTHOR_OF_DIALOG = "authorOfDialog"
    AUTHOR_OF_INTRODUCTION = "authorOfIntroduction"
    AUTHOR_OF_SCREENPLAY = "authorOfScreenplay"
    BIBLIOGRAPHIC_ANTECEDENT = "bibliographicAntecedent"
    BINDER = "binder"
    BINDING_DESIGNER = "bindingDesigner"
    BLURB_WRITER = "blurbWriter"
    BOOK_DESIGNER = "bookDesigner"
    BOOK_PRODUCER = "bookProducer"
    BOOK_JACKET_DESIGNER = "bookJacketDesigner"
    BOOKPLATE_DESIGNER = "bookplateDesigner"
    BOOKSELLER = "bookseller"
    CALLIGRAPHER = "calligrapher"
    CARTOGRAPHER = "cartographer"
    CENSOR = "censor"
    CINEMATOGRAPHER = "cinematographer"
    CLIENT = "client"
    COLLABORATOR = "collaborator"
    COLLECTOR = "collector"
    COLLOTYPER = "collotyper"
    COLORIST = "colorist"
    COMMENTATOR = "commentator"
    COMMENTATOR_FOR_WRITTEN_TEXT = "commentatorForWrittenText"
    COMPILER = "compiler"
    COMPLAINANT = "complainant"
    COMPLAINANT_APPELLANT = "complainantAppellant"
    COMPLAINANT_APPELLEE = "complainantAppellee"
    COMPOSER = "composer"
    COMPOSITOR = "compositor"
    CONCEPTOR = "conceptor"
    CONDUCTOR = "conductor"
    CONSERVATOR = "conservator"
    CONSULTANT = "consultant"
    CONSULTANT_TO_PROJECT = "consultantToProject"
    CONTESTANT = "contestant"
    CONTESTANT_APPELLANT = "contestantAppellant"
    CONTESTANT_APPELLEE = "contestantAppellee"
    CONTESTEE = "contestee"
    CONTESTEE_APPELLANT = "contesteeAppellant"
    CONTESTEE_APPELLEE = "contesteeAppellee"
    CONTRACTOR = "contractor"
    CONTRIBUTOR = "contributor"
    COPYRIGHT_CLAIMANT = "copyrightClaimant"
    COPYRIGHT_HOLDER = "copyrightHolder"
    CORRECTOR = "corrector"
    CORRESPONDENT = "correspondent"
    COSTUME_DESIGNER = "costumeDesigner"
    COVER_DESIGNER = "coverDesigner"
    CREATOR = "creator"
    CURATOR_OF_AN_EXHIBITION = "curatorOfAnExhibition"
    DANCER = "dancer"
    DATA_CONTRIBUTOR = "dataContributor"
    DATA_MANAGER = "dataManager"
    DEDICATEE = "dedicatee"
    DEDICATOR = "dedicator"
    DEFENDANT = "defendant"
    DEFENDANT_APPELLANT = "defendantAppellant"
    DEFENDANT_APPELLEE = "defendantAppellee"
    DEGREE_GRANTOR = "degreeGrantor"
    DELINEATOR = "delineator"
    DEPICTED = "depicted"
    DEPOSITOR = "depositor"
    DESIGNER = "designer"
    DIRECTOR = "director"
    DISSERTANT = "dissertant"
    DISTRIBUTION_PLACE = "distributionPlace"
    DISTRIBUTOR = "distributor"
    DONOR = "donor"
    DRAFTSMAN = "draftsman"
    DUBIOUS_AUTHOR = "dubiousAuthor"
    EDITOR = "editor"
    ELECTRICIAN = "electrician"
    ELECTROTYPER = "electrotyper"
    ENGINEER = "engineer"
    ENGRAVER = "engraver"
    ETCHER = "etcher"
    EVENT_PLACE = "eventPlace"
    EXPERT = "expert"
    FACSIMILIST = "facsimilist"
    FIELD_DIRECTOR = "fieldDirector"
    FILM_EDITOR = "filmEditor"
    FIRST_PARTY = "firstParty"
    FORGER = "forger"
    FORMER_OWNER = "formerOwner"
    FUNDER = "funder"
    GEOGRAPHIC_INFORMATION_SPECIALIST = "geographicInformationSpecialist"
    HONOREE = "honoree"
    HOST = "host"
    ILLUMINATOR = "illuminator"
    ILLUSTRATOR = "illustrator"
    INSCRIBER = "inscriber"
    INSTRUMENTALIST = "instrumentalist"
    INTERVIEWEE = "interviewee"
    INTERVIEWER = "interviewer"
    INVENTOR = "inventor"
    LABORATORY = "laboratory"
    LABORATORY_DIRECTOR = "laboratoryDirector"
    LEAD = "lead"
    LANDSCAPE_ARCHITECT = "landscapeArchitect"
    LENDER = "lender"
    LIBELANT = "libelant"
    LIBELANT_APPELLANT = "libelantAppellant"
    LIBELANT_APPELLEE = "libelantAppellee"
    LIBELEE = "libelee"
    LIBELEE_APPELLANT = "libeleeAppellant"
    LIBELEE_APPELLEE = "libeleeAppellee"
    LIBRETTIST = "librettist"
    LICENSEE = "licensee"
    LICENSOR = "licensor"
    LIGHTING_DESIGNER = "lightingDesigner"
    LITHOGRAPHER = "lithographer"
    LYRICIST = "lyricist"
    MANUFACTURER = "manufacturer"
    MARBLER = "marbler"
    MARKUP_EDITOR = "markupEditor"
    METADATA_CONTACT = "metadataContact"
    METALENGRAVER = "metalengraver"
    MODERATOR = "moderator"
    MONITOR = "monitor"
    MUSIC_COPYIST = "musicCopyist"
    MUSICAL_DIRECTOR = "musicalDirector"
    MUSICIAN = "musician"
    NARRATOR = "narrator"
    OPPONENT = "opponent"
    ORGANIZER_OF_MEETING = "organizerOfMeeting"
    ORIGINATOR = "originator"
    OTHER = "other"
    OWNER = "owner"
    PAPERMAKER = "papermaker"
    PATENT_APPLICANT = "patentApplicant"
    PATENT_HOLDER = "patentHolder"
    PATRON = "patron"
    PERFORMER = "performer"
    PERMITTING_AGENCY = "permittingAgency"
    PHOTOGRAPHER = "photographer"
    PLAINTIFF = "plaintiff"
    PLAINTIFF_APPELLANT = "plaintiffAppellant"
    PLAINTIFF_APPELLEE = "plaintiffAppellee"
    PLATEMAKER = "platemaker"
    PRINTER = "printer"
    PRINTER_OF_PLATES = "printerOfPlates"
    PRINTMAKER = "printmaker"
    PROCESS_CONTACT = "processContact"
    PRODUCER = "producer"
    PRODUCTION_MANAGER = "productionManager"
    PRODUCTION_PERSONNEL = "productionPersonnel"
    PROGRAMMER = "programmer"
    PROJECT_DIRECTOR = "projectDirector"
    PROOFREADER = "proofreader"
    PUBLICATION_PLACE = "publicationPlace"
    PUBLISHER = "publisher"
    PUBLISHING_DIRECTOR = "publishingDirector"
    PUPPETEER = "puppeteer"
    RECIPIENT = "recipient"
    RECORDING_ENGINEER = "recordingEngineer"
    REDACTOR = "redactor"
    RENDERER = "renderer"
    REPORTER = "reporter"
    REPOSITORY = "repository"
    RESEARCH_TEAM_HEAD = "researchTeamHead"
    RESEARCH_TEAM_MEMBER = "researchTeamMember"
    RESEARCHER = "researcher"
    RESPONDENT = "respondent"
    RESPONDENT_APPELLANT = "respondentAppellant"
    RESPONDENT_APPELLEE = "respondentAppellee"
    RESPONSIBLE_PARTY = "responsibleParty"
    RESTAGER = "restager"
    REVIEWER = "reviewer"
    RUBRICATOR = "rubricator"
    SCENARIST = "scenarist"
    SCIENTIFIC_ADVISOR = "scientificAdvisor"
    SCRIBE = "scribe"
    SCULPTOR = "sculptor"
    SECOND_PARTY = "secondParty"
    SECRETARY = "secretary"
    SETDESIGNER = "setdesigner"
    SIGNER = "signer"
    SINGER = "singer"
    SOUND_DESIGNER = "soundDesigner"
    SPEAKER = "speaker"
    SPONSOR = "sponsor"
    STAGE_MANAGER = "stageManager"
    STANDARDS_BODY = "standardsBody"
    STEREOTYPER = "stereotyper"
    STORYTELLER = "storyteller"
    SUPPORTING_HOST = "supportingHost"
    SURVEYOR = "surveyor"
    TEACHER = "teacher"
    TECHNICAL_DIRECTOR = "technicalDirector"
    THESIS_ADVISOR = "thesisAdvisor"
    TRANSCRIBER = "transcriber"
    TRANSLATOR = "translator"
    TYPE_DESIGNER = "typeDesigner"
    TYPOGRAPHER = "typographer"
    UNIVERSITY_PLACE = "universityPlace"
    VIDEOGRAPHER = "videographer"
    VOCALIST = "vocalist"
    WITNESS = "Witness"
    WOOD_ENGRAVER = "woodEngraver"
    WOODCUTTER = "woodcutter"
    WRITER_OF_ACCOMPANYING_MATERIAL = "writerOfAccompanyingMaterial"


@dataclass
class PersonType:
    class Meta:
        name = "personType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    is_corporate_body: bool = field(
        default=False,
        metadata={
            "name": "isCorporateBody",
            "type": "Attribute",
        }
    )


@dataclass
class AgentType:
    class Meta:
        name = "agentType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    role: Optional[AgentRoleType] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
