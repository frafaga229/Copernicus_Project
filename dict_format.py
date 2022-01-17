FORMAT_COL = {
    **dict.fromkeys(['Title', 'title', 'TITLE','Titre', 'titre', 'TITRE'], 'Title'),
    **dict.fromkeys(['Training Content', 'Training content', 'TRAINING CONTENT','training content', 'Content',
                     'CONTENT', 'Contenu de la Formation', 'Contenu de la formation', 'CONTENU DE LA FORMATION',
                     'Contenu', 'CONTENU', 'Objective', 'Objectives', 'objectives'], 'Training Content'),
    **dict.fromkeys(['Way of training', 'Format', 'format'], 'Way of training'),
    **dict.fromkeys(['Disciplines', 'disciplines'], 'Disciplines'),
    **dict.fromkeys(['Admission Requirements', 'admission requirements'], 'Admission Requirements'),
    **dict.fromkeys(['Organisation', 'organisation', 'Organization', 'organization',
                     'ORG1', 'Organisme'], 'Organisation'),
    **dict.fromkeys(['Org. Country', 'org. country', 'Place', 'place','Region', 'region', 'Country',
                     'country', 'Région / à distance'], 'Org. Country'),
    **dict.fromkeys(['Language', 'language'], 'Language'),
    **dict.fromkeys(['Diploma', 'diploma', 'Level', 'level'], 'Diploma'),
    **dict.fromkeys(['Duration and terms', 'Duration and Terms', 'Duration', 'duration',
                     'DURATION'], 'Duration and terms'),
    **dict.fromkeys(['Publication Date', 'publication date'], 'Publication Date'),
    **dict.fromkeys(['Level Required', 'level required'], 'Level Required'),
    **dict.fromkeys(['Prerequisites', 'prerequisites'], 'Prerequisites'),
    **dict.fromkeys(['Public concerned', 'public concerned'], 'Public concerned'),
    **dict.fromkeys(['URL', 'url', 'Link prog', 'link prog'], 'URL'),
    **dict.fromkeys(['ID', 'id', 'Réf. Form.', ], 'ID'),
    **dict.fromkeys(['Comments', 'comments'], 'Comments')
}

DICT_LEVEL = {
    **dict.fromkeys(['Master',"Master's", 'MSc', 'Second', '2nd', 'Autonomous', 'Automation', 'Mastère', 'M2', 'Máster', 'MS', 'Masters', 'MSC', ], 'Master'),
    **dict.fromkeys(['Ingénieur', 'Ingénierie', 'Engineering', 'Ingénieur-e', ], 'Ingénieur'),
    **dict.fromkeys(['Technicien', 'Technical', ], 'Technicien'),
    **dict.fromkeys(['PhD', 'Doctorat'], 'Doctorat'),
    **dict.fromkeys(['Licence', 'Bachelor', 'Bachelors', "Bachelor's",  ], 'License'),
    **dict.fromkeys(['Copernicus', 'MOOC', 'ESA', 'Navipedia', 'COPERNICUS', 'Télédétection', 'Formation', 'Certificat', 'Big',
       'Systèmes', 'Intelligent', 'Geodesy', 'Spécialité', ], 'Spécialisation')
}

DICT_LANG = {
    **dict.fromkeys(['es-ES', 'es', 'ca', 'gl'], 'Spanish'),
    **dict.fromkeys(['en', 'en-US', 'en-GB', 'lang=', 'en-gb', 'en-us'], 'English'),
    **dict.fromkeys(['fr', 'fr-FR', 'fr-fr', 'fr_FR'], 'French'),
    **dict.fromkeys(['de-DE', 'de', 'de-de'], 'German'),
    **dict.fromkeys(['it', 'it-IT'], 'Italian'),
    **dict.fromkeys(['pl'], 'Polish'),
    **dict.fromkeys(['pt', 'pt-pt'], 'Portuguese')
}

DICT_DURA = {
    **dict.fromkeys(['es-ES', 'es', 'ca', 'gl'], 'Spanish'),
    **dict.fromkeys(['en', 'en-US', 'en-GB', 'lang=', 'en-gb', 'en-us'], 'English'),
    **dict.fromkeys(['fr', 'fr-FR', 'fr-fr', 'fr_FR'], 'French'),
    **dict.fromkeys(['de-DE', 'de', 'de-de'], 'German'),
    **dict.fromkeys(['it', 'it-IT'], 'Italian'),
    **dict.fromkeys(['pl'], 'Polish'),
    **dict.fromkeys(['pt', 'pt-pt'], 'Portuguese')
}

