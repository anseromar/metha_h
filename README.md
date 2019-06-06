# metha_h
Partie 1 et 2 :
Les fonctions qui réalisent la lecture du fichier de jeux de données se trouvent dans le fichier Source/parse_instance_solution.py
Ce fichier inclu une fonction main qui exécute le differentes fonctions pour résoudre les parties suivantes.
Vous trouverez ces fonctions commentaient il suffit d'enlever le commenter et d'éxecuter le fichier parse_instance_solution.py

Nous avons implémenté deux versions de validator (cf le rapport) une se trouve dans le dossier Source directement (Source/validator.py) et la deuxième se trouve dans le dossier Version_2_validator. les deux utilise une version séparée pour parser qui est accéssible direction dans le dossier dans laquelle elle se trouve. 
pour tester la deuxième version du validator la meme principe est appliqué. il y a un main dans le fichier checker.py

Pour ce qui est des bornes inférieurs et bornes supérieurs. chacune de ces deux fonctionnalitées est implémentée dans un fichier 
(resp lower_bound, upper_bound) vous pouvez les tester dans le fichier parse_instance_solution.py

partie 3: 
La partie 3 n'a pas été complétement traité. seul la sous partie de génération de voisins est disponible.
vous trouvez la méthode neighbour_date dans le fichier local_search.py 
