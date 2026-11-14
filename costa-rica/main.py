import json, os, re

f = 'test-input.json' if os.path.exists('test-input.json') else 'train-input.json'
docs = json.load(open(f))['documents']

acc = {'a': 'aáàä', 'e': 'eéèë', 'i': 'iíìï', 'o': 'oóòö', 'u': 'uúùü', 'n': 'nñ'}
plain = str.maketrans('áàäéèëíìïóòöúùüñÁÉÍÓÚÑ', 'aaaeeeiiiooouuunAEIOUN')


def fuzzy(w):
    return ''.join('[' + acc[c] + ']' if c in acc else re.escape(c) for c in w.lower().translate(plain))


mon = 'January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|octubre|noviembre|diciembre'
cap = r"[A-ZÁÉÍÓÚÑÜ][a-záéíóúñü'-]+"
full = cap + r'(?:\s+(?:de\s+(?:la\s+)?)?' + cap + r'){0,3}'
rel = 'son|daughter|wife|husband|brother|sister|mother|father|mom|dad|partner|friend|colleague|cousin|aunt|uncle|niece|nephew|grandson|granddaughter|grandmother|grandfather|boyfriend|girlfriend|fiancée?|fiance|companion|child|kid|spouse|travel companion|hijo|hija|esposa|esposo'
bye = r'Regards|Kind regards|Best regards|Warm regards|Best wishes|Best|Thanks|Thank you|Many thanks|Cheers|Sincerely|Yours sincerely|Yours truly|Cordially|Saludos|Atentamente|Cordialmente|Gracias|Un saludo|Pura vida'
stop = {'Pura', 'Vida', 'Voyages', 'Team', 'Hello', 'Hi', 'Dear', 'The', 'Please', 'Costa', 'Rica', 'San', 'Mr', 'Mrs', 'Ms', 'Calle', 'Avenida', 'My', 'And', 'I', 'We', 'This', 'It', 'Not', 'Writing', 'Sorry', 'Still', 'Here'}
lex = 'Carlos Isabella Diego Luis Adriana Gabriel Rocío Lucía Mauricio Valeria Tatiana Natalia Rodrigo Javier Sofía Esteban Gabriela Ignacio Fernanda Pilar Emilio María Álvaro Andrés Camila Daniela Ana Marco Paola Kevin Melissa Jorge Laura Pablo Monserrat Alejandro Alejandra Fabián Fabiola Mariana Mariela Ricardo Roberto Sergio Silvia Andrea Pedro Miguel Francisco Fernando Eduardo Adrián Josué Jonathan Steven Allan Randall Kattia Karla Karen Yorleny Marcela Priscilla Carolina Catalina Valentina Ximena Hernán Mario Óscar Julio Rafael Raquel Ruth Elena Lorena Gloria Teresa Patricia Verónica Wendy Johanna Solano Hernández Araya Quesada Hidalgo Jiménez Obando Guzmán Ureña Vargas Zúñiga Cordero Segura Fonseca Castro Núñez Chaves Brenes Mena Paniagua Rojas Mora Alvarado Villalobos Calderón Sánchez Rodríguez Madrigal Arias Salazar Ramírez González Gómez Pérez López Martínez Herrera Méndez Campos Cruz Chacón Aguilar Espinoza Montero Soto Vega Valverde Morales Cascante Badilla Barrantes Bonilla Carvajal Cerdas Céspedes Durán Elizondo Esquivel Fallas Garro Gutiérrez Leiva Marín Monge Murillo Navarro Picado Porras Quirós Ramos Retana Salas Sandí Sibaja Solís Ulate Umaña Vásquez Venegas Víquez Zamora Zeledón'.split()

pats = [
    ('EMAIL', r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+'),
    ('ACCOUNT', r'\bCR\s?\d{2}(?:[\s-]?\d){16,20}\b'),
    ('DOB', r'\b(?:' + mon + r')\.?\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}\b'),
    ('DOB', r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:de\s+)?(?:' + mon + r')\.?,?\s+(?:de\s+|of\s+)?\d{4}\b'),
    ('DOB', r'\b\d{1,2}[/.-]\d{1,2}[/.-]\d{4}\b|\b\d{4}[/.-]\d{1,2}[/.-]\d{1,2}\b'),
    ('PHONE', r'\(?\+\s?506\)?[\s.-]?\d{8}\b|\b506\d{8}\b'),
    ('ID', r'\b0?\d[\s-]\d{4}[\s-]\d{4}\b|\b0?\d{9}\b|\b\d{11,12}\b'),
    ('PHONE', r'(?:\(?\+?\s?506\)?[\s.-]?)?\b\d{4}[\s.-]?\d{4}\b'),
]
lmk = r'(?:\d+\s*(?:metros|mts?|m|varas)\s+(?:al\s+)?(?:norte|sur|este|oeste|noreste|noroeste|sureste|suroeste)(?:\s+y\s+\d+\s*(?:metros|m|varas)\s+(?:al\s+)?(?:norte|sur|este|oeste))?\s+de(?:l)?|frente\s+a(?:l)?|contiguo\s+a(?:l)?|diagonal\s+a(?:l)?|costado\s+(?:norte|sur|este|oeste)\s+de(?:l)?|detr[aá]s\s+de(?:l)?|al\s+lado\s+de(?:l)?|casa\s+(?:n[uú]mero|#|no\.?)?\s*\d+)[^,.;\n]*'
street = r'\b(?:Calle|Avenida|Avda\.?|Ave\.?|Barrio|Residencial|Urbanizaci[oó]n|Condominio|Apartamento|Apto\.?)\s+[\w#-]+(?:,\s*[^,.;\n]+?)*?(?=\s+(?:to|and|so|for|if|in case|before|after)\s|[.;\n]|$)'


def scrub(t):
    refs = re.findall(r'\bPV-?\s?[A-Za-z0-9]{5}\b', t)
    for k, r in enumerate(refs):
        t = t.replace(r, f'\x00{k}\x00', 1)
    locs = [m[:-1] for m in re.findall(r'[\w.+-]+@', t)]
    names = {x for loc in locs for x in re.split(r'[._+\-\d]+', loc) if len(x) > 2}
    for cat, p in pats:
        t = re.sub(p, '[' + cat + ']', t, flags=re.I if cat == 'DOB' else 0)
    for loc in sorted(set(locs), key=len, reverse=True):
        t = re.sub(r'(?<!\w)' + re.escape(loc) + r'(?!\w)', '[EMAIL]', t, flags=re.I)
    t = re.sub(street, '[ADDRESS]', t)
    t = re.sub(lmk, '[ADDRESS]', t, flags=re.I)
    cues = [
        r'(?:[Mm]y name is|[Nn]ame:|I am|I\'m|[Tt]his is|[Ii]t\'s|[Mm]e llamo|[Ss]oy|[Pp]assenger)\s+(' + full + ')',
        r'\b[Mm]y (?:' + rel + r')(?:,)?\s+(' + full + ')',
        r'\b(?:Mr|Mrs|Ms|Miss|Dr|Sr|Sra|Srta|Don|Doña)\.?\s+(' + full + ')',
        r'(?:' + bye + r')[,!.]?[ \t]*\n?[ \t]*(?:[-—–][ \t]*)?(' + full + r')[ \t]*$',
        r'\n[ \t]*[-—–]?[ \t]*(' + full + r')[ \t]*$',
        r'(' + full + r')\s+(?:will travel|is travell?ing|is vegetarian|and I\b)',
    ]
    for c in cues:
        for m in re.finditer(c, t):
            names.update(w for w in re.findall(cap, m.group(1)) if w not in stop)
    names = {n.lower().translate(plain) for n in names if len(n) > 2 and n.title() not in stop}
    for n in sorted(names, key=len, reverse=True):
        t = re.sub(r'(?<!\w)' + fuzzy(n) + r'(?!\w)', '[NAME]', t, flags=re.I)
    for n in lex:
        t = re.sub(r'(?<!San )(?<!\w)' + fuzzy(n) + r'(?!\w)', lambda m: '[NAME]' if m.group()[0].isupper() else m.group(), t, flags=re.I)
    t = re.sub(r'\[NAME\](?:\s+(?:de\s+(?:la\s+)?)?\[NAME\])+', '[NAME]', t)
    for k, r in enumerate(refs):
        t = t.replace(f'\x00{k}\x00', r)
    return t


res = {d['id']: scrub(d['text']) for d in docs}
json.dump({'redacted_documents': res}, open('test-output.json' if f.startswith('test') else 'my-output.json', 'w'), ensure_ascii=False, indent=1)
