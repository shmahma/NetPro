

# NetPro

Projet Réseau
Méthode utilisé:Peer to peer
Protocole utilisé:UDP

Systeme:
1er choix:different clan(les differents membres partages la meme map),il peuvent s attaquait entre eux.
2 eme choix:chaque jouer a une map(pas de clans)
3eme choix:tous les joueurs partage la m map

Régles:
systeme de niveau(points) :
tu passes un niveau ou tu gagnes une attaque -> tu gagnes de l'argent->t'achetes des ressources.

```diff
- Pas encore réalisé
! En cours de réalisation
# Effectué

- Test VirtualMachine
# Effectué: Régler le problème des walkers (){Asad & Souhail}
! Régler les problèmes de priorité (Arrivée de plusiseurs paquets au meme temps) {Souhail}
# Effectué: Gérer des username
# Effectué: Créer un Room avec des réglages (nombre limite de joueurs, privé/public, stockage des joueurs ...){Corentin}
# Effectué: class Player(ipJoueur, username, ...){Hadil & Ines}
! Création d'espace chat dans le jeu(Partie Graphique) {Hiba}
! Sécuriser le Broadcast dans le réseau (Send uniquement aux jouers connectés)
! Lister les Rooms qui sont disponibles
- Lorsqu'un nouveau joueur se connecte dans une partie, une sauvegarde de l'état actuel du jeu est envoyé
- Mettre en place les différents modes de Jeu
-             Possibilité de créer une partie multijoueur avec un mode
-             1er mode de Jeu : Possibilité d'attaquer/défendre un village
-             2eme mode de Jeu : Avec un chrono, construire le meilleur village avec un budget donné
-             3eme mode de Jeu : Open World (gérer la propriété des bâtiments)
-             4eme mode de Jeu : ...
                          
