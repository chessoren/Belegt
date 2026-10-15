/* Belegt UI strings — FR (master), DE, IT, RM, EN.
   Answers are always produced in the language of the question,
   whatever the interface language. */
window.I18N = {
fr: {
  netNow: "État actuel de cette machine",
  netTitle: "Réseau et souveraineté", netBlocked: "connexions sortantes bloquées", netRoute: "Route par défaut", netNone: "aucune", netYes: "présente", netLoop: "Appels locaux (127.0.0.1)", netExplain: "Observé passivement : table de routage du noyau et journal d’audit du processus Belegt. Aucun paquet n’est envoyé pour le vérifier.",
  skip: "Aller au contenu", banner: "Prototype indépendant pour Hack Apertus — pas un site officiel de la Confédération",
  uiLang: "Langue de l’interface", menu: "Menu", describe: "Votre question", send: "Envoyer",
  lede: "Une question sur la Constitution fédérale ? Belegt répond avec le texte officiel, ou il se tait.",
  tryQ: "Essayez « {q} »", askAnything: "Posez votre question, dans la langue nationale de votre choix…",
  foundVerbatim: "Trouvé mot pour mot",
  f1t: "Prouvé.<br>Mot pour mot.", f1p: "Chaque réponse s’appuie sur des phrases exactes de la Constitution, surlignées dans le texte officiel. Vous n’avez pas à nous croire : vous vérifiez en dix secondes.", f1l: "Voir comment ça marche",
  f2t: "Souverain.<br>Câble débranché.", f2p: "Apertus tourne sur cette machine. Aucun service étranger, aucune donnée qui sort : toute connexion sortante serait bloquée et comptée. Le compteur est à zéro.", f2l: "En savoir plus sur la confidentialité",
  f3t: "Quatre langues.<br>Une seule loi.", f3p: "Allemand, français, italien, romanche. Belegt vérifie que la même question mène aux mêmes articles dans chaque version officielle, et le signale sinon.", f3l: "Poser une question en romanche",
  f4t: "Mesuré.<br>Pas promis.", f4p: "Apertus seul contre Apertus avec Belegt, sur le même modèle local et les mêmes questions, pièges compris. Les chiffres sont publiés avec leurs marges d’erreur et leurs échecs.", f4l: "Voir les chiffres",
  comingT: "Une méthode, pas seulement un outil.", comingP: "La Constitution est un terrain d’essai. La règle « citation ou silence » s’applique à tout texte officiel : Code civil, protection des données, AVS, règlements communaux.", comingB: "Lire la méthode",
  howT: "Comment ça marche", privacyT: "Confidentialité", numbersT: "Méthode et chiffres", limitsT: "Limites connues", aboutT: "À propos",
  poweredBy: "Propulsé par Apertus · EPFL, ETH Zurich, CSCS", motto: "Citation ou silence", builtFor: "Conçu pour Hack Apertus 2026 · Piste 2B",
  fine: "Belegt aide à trouver le texte officiel. Ce n’est pas un conseil juridique.",
  netOffline: "Hors ligne", netOnline: "En ligne", netCount: "{n} connexion sortante", netCountP: "{n} connexions sortantes", netUnknown: "Réseau…",
  stUnderstand: "Apertus lit la question et la reformule dans les 4 langues", stRetrieve: "Recherche dans les 4 versions officielles",
  stDraft: "Apertus rédige une réponse et choisit ses citations", stVerify: "Vérification mot pour mot et concordance des langues", stQueue: "En attente : une question à la fois sur ce processeur",
  whoAI: "IA", whoCode: "Code", candidates: "Candidats", details: "Détails",
  verifiedBadge: "{n} citation vérifiée mot pour mot", verifiedBadgeP: "{n} citations vérifiées mot pour mot",
  inferenceTip: "Reformulation : cette phrase n’est pas une citation mot pour mot.",
  langsHead: "Quatre langues, une seule loi", langsAgree: "{a}/4 versions concordent", langsDiverge: "Divergence signalée : la recherche en {langs} n’a pas retrouvé cet article",
  showParallel: "Voir les 4 versions", hideParallel: "Masquer les versions",
  receipt: "Reçu", openArticle: "Ouvrir l’article", copy: "Copier", copied: "Copié",
  verRejected: "Le vérificateur a écarté {n} citation(s) introuvable(s) mot pour mot.", verRemoved: "{n} phrase(s) retirée(s) : elle(s) citait(ent) un article non prouvé.",
  refusalT: "Pas de preuve, pas de réponse.", refusalP: "Je n’ai trouvé aucune disposition de la Constitution fédérale qui réponde directement à cette question. Plutôt que de deviner, je préfère me taire.",
  nearestT: "Articles les plus proches, à lire vous-même (rien n’est affirmé)", cannotClaim: "Ce que je ne peux pas affirmer : qu’un tel article existe.",
  errorT: "Le modèle local ne répond pas. Vérifiez que le serveur Apertus est lancé.",
  officialText: "Texte officiel · Fedlex · état au 3 mars 2024", seconds: "s",
  rcTitle: "Reçu de réponse", rcAnswered: "Réponse publiée", rcAbstained: "Abstention", rcQuestion: "Question", rcModel: "Modèle", rcModelHash: "Empreinte modèle",
  rcLaw: "Texte de loi", rcVersion: "Version", rcTextHash: "Empreinte texte", rcEvidence: "Preuves", rcChecks: "Contrôles", rcNetwork: "Réseau", rcDuration: "Durée",
  rcDownload: "Télécharger le reçu (.json)", rcPrint: "Imprimer", rcNone: "aucune", rcOffline: "hors ligne (aucune route par défaut)", rcOnline: "en ligne", rcOutbound: "connexion(s) sortante(s) depuis Belegt",
  ckVerbatim: "Citations mot pour mot", ckNoUnproven: "Aucun article non prouvé", ckSilence: "Citation ou silence", ckLangs: "Concordance des 4 langues",
  lang: { de: "allemand", fr: "français", it: "italien", rm: "romanche", en: "anglais" },
  greetNote: "",
  home: "Accueil", close: "Fermer", menuNote: "Prototype indépendant · Hack Apertus 2026 · Code ouvert sous licence Apache-2.0",
  chartUs: "Apertus + Belegt", chartBase: "Apertus seul", chartTrap: "Pièges refusés", chartWrong: "Articles faux ou inventés publiés", chartLang: "Mêmes articles dans les 4 langues",
},
de: {
  netNow: "Aktueller Zustand dieses Rechners",
  netTitle: "Netz und Souveränität", netBlocked: "ausgehende Verbindungen blockiert", netRoute: "Standardroute", netNone: "keine", netYes: "vorhanden", netLoop: "Lokale Aufrufe (127.0.0.1)", netExplain: "Passiv ermittelt: Routingtabelle des Kernels und Audit-Protokoll des Belegt-Prozesses. Dafür wird kein Paket gesendet.",
  skip: "Zum Inhalt", banner: "Unabhängiger Prototyp für Hack Apertus — keine offizielle Website des Bundes",
  uiLang: "Sprache der Oberfläche", menu: "Menü", describe: "Ihre Frage", send: "Senden",
  lede: "Eine Frage zur Bundesverfassung? Belegt antwortet mit dem amtlichen Text – oder schweigt.",
  tryQ: "Versuchen Sie «{q}»", askAnything: "Stellen Sie Ihre Frage, in der Landessprache Ihrer Wahl…",
  foundVerbatim: "Wörtlich gefunden",
  f1t: "Belegt.<br>Wort für Wort.", f1p: "Jede Antwort stützt sich auf genaue Sätze der Verfassung, im amtlichen Text markiert. Sie müssen uns nicht glauben: Sie prüfen in zehn Sekunden.", f1l: "So funktioniert es",
  f2t: "Souverän.<br>Kabel gezogen.", f2p: "Apertus läuft auf diesem Rechner. Kein ausländischer Dienst, keine Daten, die hinausgehen: Jede ausgehende Verbindung würde blockiert und gezählt. Der Zähler steht auf null.", f2l: "Mehr zum Datenschutz",
  f3t: "Vier Sprachen.<br>Ein Gesetz.", f3p: "Deutsch, Französisch, Italienisch, Rätoromanisch. Belegt prüft, ob dieselbe Frage in jeder amtlichen Fassung zu denselben Artikeln führt – und meldet es, wenn nicht.", f3l: "Eine Frage auf Rumantsch stellen",
  f4t: "Gemessen.<br>Nicht versprochen.", f4p: "Apertus allein gegen Apertus mit Belegt, gleiches lokales Modell, gleiche Fragen, Fallen inklusive. Die Zahlen werden mit Fehlermargen und Fehlschlägen veröffentlicht.", f4l: "Zu den Zahlen",
  comingT: "Eine Methode, nicht nur ein Werkzeug.", comingP: "Die Verfassung ist das Testgelände. Die Regel «Zitat oder Schweigen» gilt für jeden amtlichen Text: ZGB, Datenschutz, AHV, Gemeindereglemente.", comingB: "Die Methode lesen",
  howT: "So funktioniert es", privacyT: "Datenschutz", numbersT: "Methode und Zahlen", limitsT: "Bekannte Grenzen", aboutT: "Über Belegt",
  poweredBy: "Mit Apertus · EPFL, ETH Zürich, CSCS", motto: "Zitat oder Schweigen", builtFor: "Entwickelt für Hack Apertus 2026 · Track 2B",
  fine: "Belegt hilft, den amtlichen Text zu finden. Es ist keine Rechtsberatung.",
  netOffline: "Offline", netOnline: "Online", netCount: "{n} ausgehende Verbindung", netCountP: "{n} ausgehende Verbindungen", netUnknown: "Netz…",
  stUnderstand: "Apertus liest die Frage und formuliert sie in den 4 Sprachen", stRetrieve: "Suche in den 4 amtlichen Fassungen",
  stDraft: "Apertus entwirft eine Antwort und wählt Zitate", stVerify: "Wortgenaue Prüfung und Abgleich der Sprachen", stQueue: "Warten: eine Frage nach der anderen auf diesem Prozessor",
  whoAI: "KI", whoCode: "Code", candidates: "Kandidaten", details: "Details",
  verifiedBadge: "{n} Zitat wörtlich geprüft", verifiedBadgeP: "{n} Zitate wörtlich geprüft",
  inferenceTip: "Umformulierung: Dieser Satz ist kein wörtliches Zitat.",
  langsHead: "Vier Sprachen, ein Gesetz", langsAgree: "{a}/4 Fassungen stimmen überein", langsDiverge: "Abweichung gemeldet: Die Suche auf {langs} hat diesen Artikel nicht gefunden",
  showParallel: "Alle 4 Fassungen zeigen", hideParallel: "Fassungen ausblenden",
  receipt: "Beleg", openArticle: "Artikel öffnen", copy: "Kopieren", copied: "Kopiert",
  verRejected: "Die Prüfung hat {n} Zitat(e) verworfen: nicht wörtlich auffindbar.", verRemoved: "{n} Satz/Sätze entfernt: nennt einen nicht belegten Artikel.",
  refusalT: "Kein Beleg, keine Antwort.", refusalP: "Ich habe keine Bestimmung der Bundesverfassung gefunden, die diese Frage direkt beantwortet. Statt zu raten, schweige ich lieber.",
  nearestT: "Nächstliegende Artikel zum Selberlesen (nichts wird behauptet)", cannotClaim: "Was ich nicht behaupten kann: dass es einen solchen Artikel gibt.",
  errorT: "Das lokale Modell antwortet nicht. Prüfen Sie, ob der Apertus-Server läuft.",
  officialText: "Amtlicher Text · Fedlex · Stand 3. März 2024", seconds: "s",
  rcTitle: "Antwortbeleg", rcAnswered: "Antwort veröffentlicht", rcAbstained: "Enthaltung", rcQuestion: "Frage", rcModel: "Modell", rcModelHash: "Modell-Hash",
  rcLaw: "Erlass", rcVersion: "Fassung", rcTextHash: "Text-Hash", rcEvidence: "Belege", rcChecks: "Prüfungen", rcNetwork: "Netz", rcDuration: "Dauer",
  rcDownload: "Beleg herunterladen (.json)", rcPrint: "Drucken", rcNone: "keine", rcOffline: "offline (keine Standardroute)", rcOnline: "online", rcOutbound: "ausgehende Verbindung(en) von Belegt",
  ckVerbatim: "Wörtliche Zitate", ckNoUnproven: "Kein unbelegter Artikel", ckSilence: "Zitat oder Schweigen", ckLangs: "Abgleich der 4 Sprachen",
  lang: { de: "Deutsch", fr: "Französisch", it: "Italienisch", rm: "Rätoromanisch", en: "Englisch" },
  home: "Start", close: "Schliessen", menuNote: "Unabhängiger Prototyp · Hack Apertus 2026 · Offener Code, Apache-2.0",
  chartUs: "Apertus + Belegt", chartBase: "Apertus allein", chartTrap: "Fallen abgelehnt", chartWrong: "Falsche oder erfundene Artikel veröffentlicht", chartLang: "Gleiche Artikel in allen 4 Sprachen",
},
it: {
  netNow: "Stato attuale di questa macchina",
  netTitle: "Rete e sovranità", netBlocked: "connessioni in uscita bloccate", netRoute: "Route predefinita", netNone: "nessuna", netYes: "presente", netLoop: "Chiamate locali (127.0.0.1)", netExplain: "Osservato passivamente: tabella di routing del kernel e registro di audit del processo Belegt. Nessun pacchetto viene inviato per verificarlo.",
  skip: "Vai al contenuto", banner: "Prototipo indipendente per Hack Apertus — non è un sito ufficiale della Confederazione",
  uiLang: "Lingua dell’interfaccia", menu: "Menu", describe: "La sua domanda", send: "Invia",
  lede: "Una domanda sulla Costituzione federale? Belegt risponde con il testo ufficiale, oppure tace.",
  tryQ: "Provi «{q}»", askAnything: "Ponga la sua domanda, nella lingua nazionale che preferisce…",
  foundVerbatim: "Trovato parola per parola",
  f1t: "Provato.<br>Parola per parola.", f1p: "Ogni risposta si basa su frasi esatte della Costituzione, evidenziate nel testo ufficiale. Non deve crederci: verifica in dieci secondi.", f1l: "Come funziona",
  f2t: "Sovrano.<br>Cavo staccato.", f2p: "Apertus gira su questa macchina. Nessun servizio estero, nessun dato in uscita: ogni connessione verso l’esterno sarebbe bloccata e contata. Il contatore è a zero.", f2l: "Di più sulla protezione dei dati",
  f3t: "Quattro lingue.<br>Una sola legge.", f3p: "Tedesco, francese, italiano, romancio. Belegt verifica che la stessa domanda porti agli stessi articoli in ogni versione ufficiale, e lo segnala altrimenti.", f3l: "Fare una domanda in romancio",
  f4t: "Misurato.<br>Non promesso.", f4p: "Apertus da solo contro Apertus con Belegt, stesso modello locale e stesse domande, trappole comprese. Le cifre sono pubblicate con margini d’errore e fallimenti.", f4l: "Vedere le cifre",
  comingT: "Un metodo, non solo uno strumento.", comingP: "La Costituzione è un banco di prova. La regola «citazione o silenzio» vale per ogni testo ufficiale: Codice civile, protezione dei dati, AVS, regolamenti comunali.", comingB: "Leggere il metodo",
  howT: "Come funziona", privacyT: "Protezione dei dati", numbersT: "Metodo e cifre", limitsT: "Limiti noti", aboutT: "Informazioni",
  poweredBy: "Con Apertus · EPFL, ETH Zurigo, CSCS", motto: "Citazione o silenzio", builtFor: "Ideato per Hack Apertus 2026 · Percorso 2B",
  fine: "Belegt aiuta a trovare il testo ufficiale. Non è una consulenza giuridica.",
  netOffline: "Offline", netOnline: "Online", netCount: "{n} connessione in uscita", netCountP: "{n} connessioni in uscita", netUnknown: "Rete…",
  stUnderstand: "Apertus legge la domanda e la riformula nelle 4 lingue", stRetrieve: "Ricerca nelle 4 versioni ufficiali",
  stDraft: "Apertus redige una risposta e sceglie le citazioni", stVerify: "Verifica parola per parola e concordanza delle lingue", stQueue: "In attesa: una domanda alla volta su questo processore",
  whoAI: "IA", whoCode: "Codice", candidates: "Candidati", details: "Dettagli",
  verifiedBadge: "{n} citazione verificata parola per parola", verifiedBadgeP: "{n} citazioni verificate parola per parola",
  inferenceTip: "Riformulazione: questa frase non è una citazione letterale.",
  langsHead: "Quattro lingue, una sola legge", langsAgree: "{a}/4 versioni concordano", langsDiverge: "Divergenza segnalata: la ricerca in {langs} non ha ritrovato questo articolo",
  showParallel: "Vedere le 4 versioni", hideParallel: "Nascondere le versioni",
  receipt: "Ricevuta", openArticle: "Aprire l’articolo", copy: "Copiare", copied: "Copiato",
  verRejected: "Il verificatore ha scartato {n} citazione/i non trovata/e alla lettera.", verRemoved: "{n} frase/i rimossa/e: citava un articolo non provato.",
  refusalT: "Nessuna prova, nessuna risposta.", refusalP: "Non ho trovato alcuna disposizione della Costituzione federale che risponda direttamente a questa domanda. Piuttosto che indovinare, preferisco tacere.",
  nearestT: "Articoli più vicini, da leggere di persona (nulla è affermato)", cannotClaim: "Ciò che non posso affermare: che un tale articolo esista.",
  errorT: "Il modello locale non risponde. Verifichi che il server Apertus sia avviato.",
  officialText: "Testo ufficiale · Fedlex · stato 3 marzo 2024", seconds: "s",
  rcTitle: "Ricevuta della risposta", rcAnswered: "Risposta pubblicata", rcAbstained: "Astensione", rcQuestion: "Domanda", rcModel: "Modello", rcModelHash: "Impronta modello",
  rcLaw: "Atto", rcVersion: "Versione", rcTextHash: "Impronta testo", rcEvidence: "Prove", rcChecks: "Controlli", rcNetwork: "Rete", rcDuration: "Durata",
  rcDownload: "Scaricare la ricevuta (.json)", rcPrint: "Stampare", rcNone: "nessuna", rcOffline: "offline (nessuna route predefinita)", rcOnline: "online", rcOutbound: "connessione/i in uscita da Belegt",
  ckVerbatim: "Citazioni letterali", ckNoUnproven: "Nessun articolo non provato", ckSilence: "Citazione o silenzio", ckLangs: "Concordanza delle 4 lingue",
  lang: { de: "tedesco", fr: "francese", it: "italiano", rm: "romancio", en: "inglese" },
  home: "Home", close: "Chiudere", menuNote: "Prototipo indipendente · Hack Apertus 2026 · Codice aperto, Apache-2.0",
  chartUs: "Apertus + Belegt", chartBase: "Apertus da solo", chartTrap: "Trappole rifiutate", chartWrong: "Articoli errati o inventati pubblicati", chartLang: "Stessi articoli nelle 4 lingue",
},
rm: {
  netNow: "Stadi actual da questa maschina",
  netTitle: "Rait e suveranitad", netBlocked: "colliaziuns vers l’exteriur bloccadas", netRoute: "Ruta da standard", netNone: "nagina", netYes: "avant maun", netLoop: "Clomadas localas (127.0.0.1)", netExplain: "Observà passivamain: tabella da rutas dal kernel e protocol d’audit dal process Belegt. Nagin pachet na vegn tramess per quai.",
  skip: "Ir al cuntegn", banner: "Prototip independent per Hack Apertus — betg ina pagina uffiziala da la Confederaziun",
  uiLang: "Lingua da l’interfatscha", menu: "Menu", describe: "Vossa dumonda", send: "Trametter",
  lede: "Ina dumonda davart la Constituziun federala? Belegt respunda cun il text uffizial, u el tascha.",
  tryQ: "Empruvai «{q}»", askAnything: "Faschai Vossa dumonda, en la lingua naziunala che Vus vulais…",
  foundVerbatim: "Chattà pled per pled",
  f1t: "Cumprovà.<br>Pled per pled.", f1p: "Mintga resposta sa basa sin frasas exactas da la Constituziun, marcadas en il text uffizial. Vus na stuais betg crair nus: Vus controllais en diesch secundas.", f1l: "Co che quai funcziuna",
  f2t: "Suveran.<br>Cabel distaccà.", f2p: "Apertus funcziuna sin questa maschina. Nagin servetsch ester, naginas datas che sortan: mintga colliaziun vers l’exteriur vegniss bloccada e dumbrada. Il dumbrader è a nulla.", f2l: "Dapli davart la protecziun da datas",
  f3t: "Quatter linguas.<br>Ina suletta lescha.", f3p: "Tudestg, franzos, talian, rumantsch. Belegt controllescha che la medema dumonda maina tar ils medems artitgels en mintga versiun uffiziala, ed el signalisescha il cuntrari.", f3l: "Far ina dumonda en rumantsch",
  f4t: "Mesirà.<br>Betg empermess.", f4p: "Apertus sulet cunter Apertus cun Belegt, cun il medem model local e las medemas dumondas, inclus las trappas. Las cifras vegnan publitgadas cun lur margins d’errur e lur sbagls.", f4l: "Mussar las cifras",
  comingT: "Ina metoda, betg mo in instrument.", comingP: "La Constituziun è in terren d’emprova. La regla «citat u silenzi» vala per mintga text uffizial: Cudesch civil, protecziun da datas, AVS, reglaments communals.", comingB: "Leger la metoda",
  howT: "Co che quai funcziuna", privacyT: "Protecziun da datas", numbersT: "Metoda e cifras", limitsT: "Limits enconuschents", aboutT: "Davart Belegt",
  poweredBy: "Cun Apertus · EPFL, ETH Turitg, CSCS", motto: "Citat u silenzi", builtFor: "Concepì per Hack Apertus 2026 · Traject 2B",
  fine: "Belegt gida a chattar il text uffizial. Quai n’è betg in cussegl giuridic.",
  netOffline: "Offline", netOnline: "Online", netCount: "{n} colliaziun vers l’exteriur", netCountP: "{n} colliaziuns vers l’exteriur", netUnknown: "Rait…",
  stUnderstand: "Apertus legia la dumonda e la formulescha en las 4 linguas", stRetrieve: "Tschertga en las 4 versiuns uffizialas",
  stDraft: "Apertus scriva ina resposta e tscherna ses citats", stVerify: "Verificaziun pled per pled e concordanza da las linguas", stQueue: "Spetgar: ina dumonda suenter l’autra sin quest processur",
  whoAI: "IA", whoCode: "Code", candidates: "Candidats", details: "Detagls",
  verifiedBadge: "{n} citat verifitgà pled per pled", verifiedBadgeP: "{n} citats verifitgads pled per pled",
  inferenceTip: "Reformulaziun: questa frasa n’è betg in citat pled per pled.",
  langsHead: "Quatter linguas, ina suletta lescha", langsAgree: "{a}/4 versiuns concordan", langsDiverge: "Divergenza: la tschertga en {langs} n’ha betg chattà quest artitgel",
  showParallel: "Mussar las 4 versiuns", hideParallel: "Zuppentar las versiuns",
  receipt: "Quittanza", openArticle: "Avrir l’artitgel", copy: "Copiar", copied: "Copià",
  verRejected: "Il verificatur ha refusà {n} citat(s) betg chattà(s) pled per pled.", verRemoved: "{n} frasa(s) allontanada(s): numna in artitgel betg cumprovà.",
  refusalT: "Nagina cumprova, nagina resposta.", refusalP: "Jau n’hai chattà nagina disposiziun da la Constituziun federala che respunda directamain a questa dumonda. Empè dad induvinar, tasch jau pli gugent.",
  nearestT: "Ils artitgels ils pli damanaivel, per leger sez (nagut na vegn affirmà)", cannotClaim: "Quai che jau na poss betg affirmar: ch’in tal artitgel exista.",
  errorT: "Il model local na respunda betg. Controllai sch’il server dad Apertus è avià.",
  officialText: "Text uffizial · Fedlex · stadi dals 3 da mars 2024", seconds: "s",
  rcTitle: "Quittanza da la resposta", rcAnswered: "Resposta publitgada", rcAbstained: "Abstenziun", rcQuestion: "Dumonda", rcModel: "Model", rcModelHash: "Impronta dal model",
  rcLaw: "Text legal", rcVersion: "Versiun", rcTextHash: "Impronta dal text", rcEvidence: "Cumprovas", rcChecks: "Controllas", rcNetwork: "Rait", rcDuration: "Durada",
  rcDownload: "Telechargiar la quittanza (.json)", rcPrint: "Stampar", rcNone: "nagina", rcOffline: "offline (nagina ruta da standard)", rcOnline: "online", rcOutbound: "colliaziun(s) vers l’exteriur da Belegt",
  ckVerbatim: "Citats pled per pled", ckNoUnproven: "Nagin artitgel betg cumprovà", ckSilence: "Citat u silenzi", ckLangs: "Concordanza da las 4 linguas",
  lang: { de: "tudestg", fr: "franzos", it: "talian", rm: "rumantsch", en: "englais" },
  home: "Pagina principala", close: "Serrar", menuNote: "Prototip independent · Hack Apertus 2026 · Code avert, Apache-2.0",
  chartUs: "Apertus + Belegt", chartBase: "Apertus sulet", chartTrap: "Trappas refusadas", chartWrong: "Artitgels fauss u inventads publitgads", chartLang: "Ils medems artitgels en las 4 linguas",
},
en: {
  netNow: "Current state of this machine",
  netTitle: "Network & sovereignty", netBlocked: "outbound connections blocked", netRoute: "Default route", netNone: "none", netYes: "present", netLoop: "Local calls (127.0.0.1)", netExplain: "Observed passively: the kernel routing table and the audit log of the Belegt process. No packet is sent to check it.",
  skip: "Skip to content", banner: "Independent prototype for Hack Apertus — not an official website of the Swiss Confederation",
  uiLang: "Interface language", menu: "Menu", describe: "Your question", send: "Send",
  lede: "A question about the Swiss Federal Constitution? Belegt answers with the official text, or stays silent.",
  tryQ: "Try “{q}”", askAnything: "Ask in German, French, Italian, Romansh or English…",
  foundVerbatim: "Found word for word",
  f1t: "Proven.<br>Word for word.", f1p: "Every answer rests on exact sentences of the Constitution, highlighted in the official text. You don’t have to trust us: you can check in ten seconds.", f1l: "See how it works",
  f2t: "Sovereign.<br>Cable unplugged.", f2p: "Apertus runs on this machine. No foreign service, no data leaving: any outbound connection would be blocked and counted. The counter reads zero.", f2l: "Learn about privacy",
  f3t: "Four languages.<br>One law.", f3p: "German, French, Italian, Romansh. Belegt checks that the same question leads to the same articles in every official version, and says so when it doesn’t.", f3l: "Ask a question in Romansh",
  f4t: "Measured.<br>Not promised.", f4p: "Apertus alone versus Apertus with Belegt: same local model, same questions, traps included. Numbers are published with error margins and failures.", f4l: "See the numbers",
  comingT: "A method, not just a tool.", comingP: "The Constitution is the test bed. The “cite or stay silent” rule applies to any official text: Civil Code, data protection, pensions, municipal regulations.", comingB: "Read the method",
  howT: "How it works", privacyT: "Privacy", numbersT: "Method & numbers", limitsT: "Known limits", aboutT: "About",
  poweredBy: "Powered by Apertus · EPFL, ETH Zurich, CSCS", motto: "Cite or stay silent", builtFor: "Built for Hack Apertus 2026 · Track 2B",
  fine: "Belegt helps you find the official text. It is not legal advice.",
  netOffline: "Offline", netOnline: "Online", netCount: "{n} outbound connection", netCountP: "{n} outbound connections", netUnknown: "Network…",
  stUnderstand: "Apertus reads the question and rephrases it in the 4 languages", stRetrieve: "Searching the 4 official versions",
  stDraft: "Apertus drafts an answer and picks its quotes", stVerify: "Word-for-word check and cross-language agreement", stQueue: "Waiting: one question at a time on this CPU",
  whoAI: "AI", whoCode: "Code", candidates: "Candidates", details: "Details",
  verifiedBadge: "{n} quote verified word for word", verifiedBadgeP: "{n} quotes verified word for word",
  inferenceTip: "Rephrasing: this sentence is not a word-for-word quote.",
  langsHead: "Four languages, one law", langsAgree: "{a}/4 versions agree", langsDiverge: "Divergence flagged: search in {langs} did not find this article",
  showParallel: "Show all 4 versions", hideParallel: "Hide versions",
  receipt: "Receipt", openArticle: "Open article", copy: "Copy", copied: "Copied",
  verRejected: "The verifier discarded {n} quote(s) not found word for word.", verRemoved: "{n} sentence(s) removed: cited an unproven article.",
  refusalT: "No proof, no answer.", refusalP: "I found no provision of the Federal Constitution that directly answers this question. Rather than guess, I prefer to stay silent.",
  nearestT: "Closest articles, for you to read (nothing is claimed)", cannotClaim: "What I cannot claim: that such an article exists.",
  errorT: "The local model is not responding. Check that the Apertus server is running.",
  officialText: "Official text · Fedlex · as of 3 March 2024", seconds: "s",
  rcTitle: "Answer receipt", rcAnswered: "Answer published", rcAbstained: "Abstained", rcQuestion: "Question", rcModel: "Model", rcModelHash: "Model hash",
  rcLaw: "Law", rcVersion: "Version", rcTextHash: "Text hash", rcEvidence: "Evidence", rcChecks: "Checks", rcNetwork: "Network", rcDuration: "Duration",
  rcDownload: "Download receipt (.json)", rcPrint: "Print", rcNone: "none", rcOffline: "offline (no default route)", rcOnline: "online", rcOutbound: "outbound connection(s) from Belegt",
  ckVerbatim: "Word-for-word quotes", ckNoUnproven: "No unproven article", ckSilence: "Cite or stay silent", ckLangs: "4-language agreement",
  lang: { de: "German", fr: "French", it: "Italian", rm: "Romansh", en: "English" },
  home: "Home", close: "Close", menuNote: "Independent prototype · Hack Apertus 2026 · Open source, Apache-2.0",
  chartUs: "Apertus + Belegt", chartBase: "Apertus alone", chartTrap: "Traps refused", chartWrong: "Wrong or invented articles published", chartLang: "Same articles in all 4 languages",
},
};

/* Long-form pages. RM falls back to DE (with a note), IT to FR when missing. */
window.PAGES = {
fr: {
  how: `<div class="prose">
    <p>Belegt applique une règle simple : <b>il n’affirme rien qu’il ne puisse montrer du doigt dans le texte officiel.</b></p>
    <h4>1 · Comprendre — IA</h4><p>Apertus lit la question et la reformule dans les quatre langues officielles, avec le vocabulaire de la Constitution (« manifester » devient « liberté de réunion »).</p>
    <h4>2 · Chercher — code</h4><p>Une recherche lexicale (BM25 mots + trigrammes de caractères) parcourt les 657 alinéas de chaque version. Les classements des quatre langues sont fusionnés.</p>
    <h4>3 · Rédiger — IA</h4><p>Apertus rédige une réponse courte et choisit des citations parmi six alinéas candidats. Il peut aussi répondre « rien ne répond ».</p>
    <h4>4 · Vérifier — code, sans IA</h4><p>R1 l’alinéa existe · R2 la citation figure mot pour mot · R3 elle est assez longue · R4 aucun numéro d’article non prouvé dans la réponse · R5 s’il ne reste aucune preuve, Belegt s’abstient. Enfin, la concordance des quatre langues est contrôlée grâce aux identifiants Fedlex, identiques dans chaque version.</p>
    <h4>5 · Reçu</h4><p>Chaque réponse produit un reçu : modèle et son empreinte SHA-256, version du texte de loi et son empreinte, preuves, contrôles, état du réseau. Il peut être archivé comme pièce justificative.</p></div>`,
  privacy: `<div class="prose"><p><b>Rien ne sort de la machine.</b> Le modèle Apertus est exécuté localement par llama.cpp, compilé sans accès réseau. Le serveur Belegt installe un « audit hook » Python qui bloque et compte toute connexion ou résolution DNS vers l’extérieur ; le compteur est affiché en permanence et inscrit dans chaque reçu.</p>
    <p>L’état hors ligne est observé passivement (interfaces et table de routage) : aucune requête n’est envoyée pour le vérifier.</p>
    <p>Aucune question n’est enregistrée côté serveur. Le reçu vit dans votre navigateur ; vous décidez de le télécharger.</p>
    <p>Polices et scripts sont servis par Belegt lui-même : aucun CDN, aucun traceur.</p></div>`,
  limits: `<div class="prose"><ul>
    <li>Belegt n’est pas un conseiller juridique. Il aide à trouver et lire le texte officiel.</li>
    <li>La vérification garantit que les citations existent mot pour mot, pas que la reformulation est juste. Les phrases qui ne sont pas des citations sont soulignées en pointillé.</li>
    <li>Un refus peut être un faux refus : la recherche lexicale manque parfois le bon article. Le taux est mesuré et publié.</li>
    <li>Corpus : Constitution fédérale (RS 101), état au 3 mars 2024. Les dispositions transitoires longues sont incluses mais moins bien couvertes.</li>
    <li>Le modèle tourne en 4 bits sur processeur : une réponse prend environ une minute.</li>
    <li>Les questions de test en romanche ont été rédigées par l’équipe, non par des locuteurs natifs. L’interface romanche peut contenir des maladresses.</li></ul></div>`,
  about: `<div class="prose"><p><b>Belegt</b> (« étayé, documenté ») est un prototype pour <b>Hack Apertus 2026</b>, piste 2B « Own Project ». Il n’est affilié ni à la Confédération ni aux auteurs d’Apertus.</p>
    <p>Modèle : Apertus 1.5 8B (swiss-ai, EPFL · ETH Zurich · CSCS), quantifié en GGUF Q4_K_M. Texte : Fedlex, XML Akoma Ntoso officiel en DE, FR, IT, RM.</p>
    <p>Design : structure et système de composants inspirés d’America.gov, recolorés au rouge suisse (Pantone 485 C). Polices libres Newsreader et Inter, servies localement.</p>
    <p>Code, questions de test, résultats et reçus : licence Apache-2.0.</p></div>`,
},
de: {
  how: `<div class="prose"><p>Belegt folgt einer einfachen Regel: <b>Es behauptet nichts, was es nicht im amtlichen Text zeigen kann.</b></p>
    <h4>1 · Verstehen — KI</h4><p>Apertus liest die Frage und formuliert sie in den vier Amtssprachen mit dem Vokabular der Verfassung um («demonstrieren» wird zu «Versammlungsfreiheit»).</p>
    <h4>2 · Suchen — Code</h4><p>Eine lexikalische Suche (BM25 auf Wörtern und Zeichen-N-Grammen) durchsucht die 657 Absätze jeder Fassung. Die Ranglisten der vier Sprachen werden zusammengeführt.</p>
    <h4>3 · Entwerfen — KI</h4><p>Apertus schreibt eine kurze Antwort und wählt Zitate aus sechs Kandidaten. Es darf auch «nichts beantwortet das» sagen.</p>
    <h4>4 · Prüfen — Code, ohne KI</h4><p>R1 Absatz existiert · R2 Zitat steht wörtlich da · R3 lang genug · R4 keine unbelegte Artikelnummer · R5 bleibt kein Beleg, enthält sich Belegt. Zudem wird die Übereinstimmung der vier Sprachen über die identischen Fedlex-IDs geprüft.</p>
    <h4>5 · Beleg</h4><p>Jede Antwort erzeugt einen Beleg: Modell und SHA-256, Fassung und Hash des Erlasses, Zitate, Prüfungen, Netzstatus. Archivierbar als Nachweis.</p></div>`,
  privacy: `<div class="prose"><p><b>Nichts verlässt den Rechner.</b> Apertus läuft lokal in llama.cpp, ohne Netzwerkzugriff kompiliert. Ein Python-Audit-Hook blockiert und zählt jede ausgehende Verbindung und DNS-Anfrage; der Zähler steht in jeder Antwort und jedem Beleg.</p>
    <p>Der Offline-Status wird passiv ermittelt (Schnittstellen, Routingtabelle): Es wird dafür kein Paket gesendet.</p>
    <p>Fragen werden serverseitig nicht gespeichert. Der Beleg bleibt in Ihrem Browser.</p><p>Schriften und Skripte liefert Belegt selbst aus: kein CDN, kein Tracking.</p></div>`,
  limits: `<div class="prose"><ul><li>Belegt ist keine Rechtsberatung.</li><li>Die Prüfung garantiert, dass Zitate wörtlich existieren – nicht, dass die Umformulierung richtig ist. Nicht wörtliche Sätze sind gepunktet unterstrichen.</li><li>Eine Ablehnung kann falsch sein, wenn die Suche den richtigen Artikel verfehlt. Die Quote wird gemessen und veröffentlicht.</li><li>Korpus: Bundesverfassung (SR 101), Stand 3. März 2024.</li><li>Das Modell läuft 4-bit auf CPU: eine Antwort dauert rund eine Minute.</li><li>Die rätoromanischen Testfragen stammen vom Team, nicht von Muttersprachigen.</li></ul></div>`,
  about: `<div class="prose"><p><b>Belegt</b> ist ein Prototyp für <b>Hack Apertus 2026</b>, Track 2B. Nicht mit dem Bund oder den Apertus-Autorinnen und -Autoren verbunden.</p><p>Modell: Apertus 1.5 8B (swiss-ai), GGUF Q4_K_M. Text: Fedlex, amtliches Akoma-Ntoso-XML in DE, FR, IT, RM.</p><p>Design: Struktur nach America.gov, in Schweizer Rot (Pantone 485 C). Offene Schriften Newsreader und Inter, lokal ausgeliefert.</p><p>Lizenz Apache-2.0.</p></div>`,
},
it: {
  how: `<div class="prose"><p>Belegt segue una regola semplice: <b>non afferma nulla che non possa indicare nel testo ufficiale.</b></p>
    <h4>1 · Capire — IA</h4><p>Apertus legge la domanda e la riformula nelle quattro lingue ufficiali con il vocabolario della Costituzione («manifestare» diventa «libertà di riunione»).</p>
    <h4>2 · Cercare — codice</h4><p>Una ricerca lessicale (BM25 su parole e su n-grammi di caratteri) esamina i 657 capoversi di ogni versione; le classifiche delle quattro lingue vengono fuse.</p>
    <h4>3 · Redigere — IA</h4><p>Apertus scrive una risposta breve e sceglie le citazioni tra i capoversi candidati. Può anche rispondere che nulla risponde alla domanda.</p>
    <h4>4 · Verificare — codice, senza IA</h4><p>R1 il capoverso esiste · R2 la citazione compare parola per parola · R3 è abbastanza lunga · R4 nessun numero d’articolo non provato nella risposta · R5 se non resta alcuna prova, Belegt si astiene. La concordanza delle quattro lingue è controllata grazie agli identificatori Fedlex, identici in ogni versione.</p>
    <h4>5 · Ricevuta</h4><p>Ogni risposta produce una ricevuta: modello e impronta SHA-256, versione e impronta del testo di legge, prove, controlli, stato della rete.</p></div>`,
  privacy: `<div class="prose"><p><b>Nulla esce dalla macchina.</b> Apertus gira localmente in llama.cpp, compilato senza accesso alla rete. Un «audit hook» Python blocca e conta ogni connessione o richiesta DNS verso l’esterno; il contatore è sempre visibile e figura in ogni ricevuta.</p><p>Lo stato offline è osservato passivamente (interfacce e tabella di routing): nessun pacchetto viene inviato per verificarlo.</p><p>Nessuna domanda è memorizzata sul server. La ricevuta resta nel suo browser.</p><p>Caratteri e script sono serviti da Belegt stesso: nessun CDN, nessun tracciamento.</p></div>`,
  limits: `<div class="prose"><ul><li>Belegt non è una consulenza giuridica.</li><li>La verifica garantisce che le citazioni esistano alla lettera, non che la riformulazione sia corretta. Le frasi non citate sono sottolineate a puntini.</li><li>Un rifiuto può essere sbagliato se la ricerca manca l’articolo giusto. Il tasso è misurato e pubblicato.</li><li>Corpus: Costituzione federale (RS 101), stato 3 marzo 2024.</li><li>Il modello gira a 4 bit su CPU: una risposta richiede circa un minuto.</li><li>Le domande di test in romancio sono state scritte dal team, non da madrelingua.</li></ul></div>`,
  about: `<div class="prose"><p><b>Belegt</b> («comprovato, documentato» in tedesco) è un prototipo per <b>Hack Apertus 2026</b>, percorso 2B. Non è affiliato alla Confederazione né agli autori di Apertus.</p><p>Modello: Apertus 1.5 8B (swiss-ai), GGUF Q4_K_M. Testo: Fedlex, XML Akoma Ntoso ufficiale in DE, FR, IT, RM.</p><p>Design: struttura e sistema di componenti ispirati ad America.gov, ricolorati in rosso svizzero (Pantone 485 C). Caratteri liberi Newsreader e Inter, serviti localmente.</p><p>Licenza Apache-2.0.</p></div>`,
},
en: {
  how: `<div class="prose"><p>Belegt follows one rule: <b>it asserts nothing it cannot point to in the official text.</b></p>
    <h4>1 · Understand — AI</h4><p>Apertus reads the question and rewrites it in the four official languages using the Constitution’s own vocabulary (“demonstrate” becomes “freedom of assembly”).</p>
    <h4>2 · Search — code</h4><p>Lexical search (BM25 on words and character n-grams) scans the 657 paragraphs of each version; the four rankings are fused.</p>
    <h4>3 · Draft — AI</h4><p>Apertus writes a short answer and picks quotes from six candidate paragraphs. It may also say nothing answers the question.</p>
    <h4>4 · Verify — code, no AI</h4><p>R1 the paragraph exists · R2 the quote appears word for word · R3 it is long enough · R4 no unproven article number in the answer · R5 if no evidence survives, Belegt abstains. Cross-language agreement is checked through Fedlex IDs, identical in every version.</p>
    <h4>5 · Receipt</h4><p>Every answer produces a receipt: model and SHA-256, law version and hash, evidence, checks, network state. It can be archived as an audit record.</p></div>`,
  privacy: `<div class="prose"><p><b>Nothing leaves the machine.</b> Apertus runs locally in llama.cpp, built without network support. A Python audit hook blocks and counts every outbound connection and DNS lookup; the counter is always visible and written into every receipt.</p><p>Offline state is observed passively (interfaces and routing table): no packet is sent to check it.</p><p>No question is stored server-side. The receipt lives in your browser.</p><p>Fonts and scripts are served by Belegt itself: no CDN, no tracker.</p></div>`,
  limits: `<div class="prose"><ul><li>Belegt is not legal advice.</li><li>Verification guarantees quotes exist word for word, not that the rephrasing is right. Non-quoted sentences are dotted-underlined.</li><li>A refusal can be a false refusal when search misses the right article. The rate is measured and published.</li><li>Corpus: Federal Constitution (SR 101), as of 3 March 2024.</li><li>The model runs 4-bit on CPU: one answer takes about a minute.</li><li>Romansh test questions were written by the team, not native speakers; the Romansh UI may contain awkward phrasing.</li></ul></div>`,
  about: `<div class="prose"><p><b>Belegt</b> (German for “substantiated, documented”) is a prototype for <b>Hack Apertus 2026</b>, Track 2B “Own Project”. Not affiliated with the Swiss Confederation or the Apertus authors.</p><p>Model: Apertus 1.5 8B (swiss-ai: EPFL · ETH Zurich · CSCS), GGUF Q4_K_M. Text: Fedlex official Akoma Ntoso XML in DE, FR, IT, RM.</p><p>Design: structure and component system modelled on America.gov, recoloured in Swiss red (Pantone 485 C). Open fonts Newsreader and Inter, served locally.</p><p>Code, test questions, results and receipts: Apache-2.0.</p></div>`,
},
};
window.PAGES.rm = window.PAGES.de;
