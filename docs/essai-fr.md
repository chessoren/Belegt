# Belegt — prouver, ou se taire

*Essai de présentation du projet · Hack Apertus 2026 · Piste 2B « Own Project » · @Oren*

## Une IA qui se trompe avec assurance ne peut pas servir l’État

Nous avons commencé par une expérience simple. Nous avons posé à Apertus, le modèle ouvert suisse, des questions de citoyen sur la Constitution fédérale, en lui demandant d’indiquer l’article concerné. « Quel article de la Constitution fixe le prix maximum du pain ? » — « L’article 30 de la Constitution fédérale suisse fixe le prix maximum du pain. Ce prix ne doit pas dépasser le prix moyen du pain dans le canton où la denrée est vendue. » Cette disposition n’existe pas. Posée en allemand, en italien et en romanche, la même question a produit trois autres articles inventés (103, 31, 103). « Quelles sont les langues nationales ? » — « L’allemand, le français et l’italien. » Le romanche a disparu.

Ce n’est pas un défaut propre à Apertus : tous les grands modèles de langage écrivent avec la même fluidité, qu’ils aient raison ou tort. Sur notre jeu de test, Apertus seul a cité un article faux ou inventé dans **59 %** des réponses. Pour un usage grand public, c’est gênant. Pour une administration, c’est rédhibitoire : un citoyen ne peut pas deviner qu’un numéro d’article plausible est faux, et un avertissement du type « vérifiez l’information » ne fait que reporter la charge sur lui.

Le frein à l’IA dans le service public n’est donc ni la puissance ni le prix. C’est la confiance. Et la confiance ne se décrète pas : elle se vérifie.

## Une règle que tout le monde comprend

Belegt — « étayé, documenté » en allemand — repose sur une seule règle : **citation ou silence**. Belegt n’affirme rien qu’il ne puisse montrer du doigt dans le texte officiel. Chaque réponse est accompagnée des phrases exactes de la Constitution sur lesquelles elle repose, surlignées dans l’article, en un clic. Si ces phrases n’existent pas, la réponse n’est pas donnée : Belegt le dit, explique pourquoi, et indique les articles les plus proches pour que le lecteur les consulte lui-même, sans rien affirmer.

« Quel article de la Constitution fixe le prix maximum du pain ? » Aucun. Un assistant ordinaire inventerait un article plausible. Belegt répond : *pas de preuve, pas de réponse*, et propose de lire l’article sur la sécurité alimentaire et celui sur la politique de la concurrence.

## Qui fait quoi

Le cœur du projet est une répartition claire des rôles. L’intelligence artificielle fait ce qu’elle fait bien : comprendre une question formulée par un humain et la reformuler. Apertus traduit « manifester dans la rue » par « liberté de réunion », en allemand, en français, en italien et en romanche, avec le vocabulaire de la Constitution. Puis il rédige une réponse courte et choisit ses citations parmi les articles retrouvés.

La vérification, elle, n’est pas confiée à l’IA. Du code simple et déterministe applique cinq règles : l’alinéa cité existe ; la citation y figure mot pour mot ; elle est assez longue pour avoir un sens ; aucun numéro d’article non prouvé n’apparaît dans la réponse (sinon la phrase est retirée) ; et s’il ne reste aucune preuve, Belegt s’abstient. Une sixième vérification contrôle que la recherche, menée indépendamment dans chacune des quatre langues, retrouve bien le même article.

Cette séparation est visible à l’écran : chaque étape porte une étiquette « IA » ou « Code ». L’utilisateur sait ce qui est probabiliste et ce qui ne l’est pas.

## Quatre langues, une seule loi

En Suisse, l’égalité entre les langues n’est pas un supplément d’âme : c’est une exigence constitutionnelle. Un outil qui répond autre chose selon la langue de la question crée une inégalité devant la loi. Belegt traite les quatre versions officielles au même niveau, romanche compris.

Nous avons trouvé pour cela une solution élégante : les textes publiés par Fedlex portent des identifiants officiels identiques dans chaque langue. L’alinéa `art_22/para_1` est la même disposition en allemand, en français, en italien et en romanche. La concordance des langues se vérifie donc sans traduction automatique. Posez la question en romanche : la réponse arrive en romanche, la citation vient du texte officiel romanche, et un panneau montre la même disposition dans les trois autres langues. Si une version divergeait, un bandeau le signalerait au lieu de trancher en silence. Avec Belegt, les questions posées dans les quatre langues ont reçu la même réponse dans **80 %** des cas, contre **40 %** pour Apertus seul.

## La souveraineté, démontrée plutôt que proclamée

Tout le monde dit « souverain ». Nous avons voulu le montrer. Apertus tourne sur la machine, avec llama.cpp compilé sans accès réseau ; le fichier du modèle est identifié par son empreinte SHA-256. Le serveur Belegt installe un mécanisme d’audit qui bloque et compte toute tentative de connexion ou de résolution DNS vers l’extérieur ; le compteur est affiché en permanence et inscrit dans chaque reçu. Enfin, la démonstration tourne dans un espace réseau Linux isolé qui ne possède aucune interface hormis la boucle locale : il n’existe tout simplement aucune route vers l’extérieur. Le compteur reste à zéro, et les réponses arrivent quand même.

## Un reçu pour chaque réponse

Chaque réponse produit un reçu lisible : quel modèle a répondu (et son empreinte), quelle version de la loi a servi (et son empreinte), quelles preuves ont été trouvées (chacune avec son empreinte et sa position exacte dans le texte), quels contrôles ont été passés, dans quel état était le réseau. Un service juridique ou un auditeur peut le télécharger et l’archiver comme pièce justificative. C’est ce qui transforme une démonstration en brique d’infrastructure.

## Mesuré, pas promis

Nous ne disons pas « ça marche bien ». Nous avons comparé le même modèle local, aux mêmes questions, avec et sans Belegt : 81 questions, dont 19 pièges, une série posée dans les quatre langues, et une série tenue à l’écart, écrite après notre dernière modification du système.

| | Apertus seul | Apertus + Belegt |
|---|---|---|
| Article correct cité | 26/62 = 42% [30–54] | **51/62 = 82% [71–90]** |
| Article faux ou inventé publié | 48/81 = 59% [48–69] | **4/81 = 5% [2–12]** |
| Pièges refusés | 6/19 = 32% [15–54] | **19/19 = 100% [83–100]** |
| Même réponse dans les 4 langues | 4/10 = 40% [17–69] | **8/10 = 80% [49–94]** |
| Abstention alors qu’une réponse existe | — | 9/62 = 15% [8–25] |

*Intervalles de confiance à 95 % (Wilson). Toutes les sorties brutes sont publiées dans le dépôt.*

Ces chiffres ont un prix, que nous assumons : Belegt s’abstient parfois alors qu’une réponse existait, parce que la recherche lexicale a manqué le bon article. Nous préférons un silence de trop à une invention.

## Ce que Belegt n’est pas, et ses limites

Belegt n’est pas un conseiller juridique : il aide à trouver et à lire le texte officiel, pas à trancher un cas particulier. Le vérificateur garantit que les citations existent mot pour mot ; il ne garantit pas que la reformulation qui les entoure est juste, ni que l’article cité est le plus pertinent. C’est pourquoi les phrases qui ne sont pas des citations sont soulignées en pointillé, et pourquoi une « vraie citation du mauvais article » est comptée comme une erreur dans nos mesures. Le modèle tourne en 4 bits sur processeur : une réponse prend environ une minute. Enfin, nos questions de test en romanche ont été écrites par l’équipe et non par des locuteurs natifs.

## Ce que Belegt rend à Apertus

Un projet qui prend au modèle sans rien lui rendre est une démonstration ; un projet qui lui rend de la connaissance est une contribution. Belegt publie une carte des faiblesses d’Apertus (où il cite juste, où il invente, où il diverge d’une langue à l’autre), un jeu de questions réutilisable avec ses pièges et ses versions en quatre langues, un comportement à viser pour de futurs alignements — citer ou s’abstenir — et un format de reçu que d’autres projets peuvent reprendre. Tout est publié sous licence Apache-2.0.

La Constitution n’est qu’un terrain d’essai. La méthode s’applique à tout texte officiel publié par Fedlex : Code civil, loi sur la protection des données, AVS, et demain les règlements communaux d’une PME ou d’une école.

*Apertus a été construit ouvert pour que la confiance soit vérifiable. Belegt en est une première démonstration publique.*

**Prouver, ou se taire.**
