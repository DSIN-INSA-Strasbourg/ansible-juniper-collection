# Ansible - rôle insa_strasbourg.juniper.ex_config

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/DSIN-INSA-Strasbourg/ansible-juniper-collection/blob/main/collections/ansible_collections/insa_strasbourg/juniper/docs/ex_config.md)
[![fr](https://img.shields.io/badge/lang-fr-blue.svg)](https://github.com/DSIN-INSA-Strasbourg/ansible-juniper-collection/blob/main/collections/ansible_collections/insa_strasbourg/juniper/docs/ex_config.fr.md)

---

## Introduction

Ce rôle sert à assurer l'exploitation courante des commutateurs Juniper, et à déployer les changements de configuration.
Chaque fichier de configuration sera généré localement dans un dossier du poste contrôleur (par défaut `$HOME/.juniper-configs/`).

## Fichiers principaux

Les chemins sont relatifs au dossier Ansible.

| Fichier | Rôle de ce fichier |
| --- | --- |
| `network` | Fichier d'inventaire des équipements réseau, et attribution des modèles et du type de configuration (ELS/non-ELS) |
| `host_vars/*nom_switch*.yml` | Configuration d'un commutateur |
| `group_vars/juniper/*.yml` | Variables par défaut : liste des VLAN, des utilisateurs |

## Groupes d'inventaire utilisés par le rôle

Chaque famille de modèle doit être rattachée à un groupe qui lui est propre. Les groupes pour les modèles qualifiés sont les suivants :

- juniper_ex2200
- juniper_ex2300 *(pas spécialement testée, mais devrait fonctionner)*
- juniper_ex3300
- juniper_ex3400
- juniper_ex4100
- juniper_ex4300
- juniper_ex4600
- juniper_ex4650

Les équipements ELS **doivent** être rattachés au groupe `juniper_els`, par exemple ainsi :

```yaml
juniper_els:
  children:
    juniper_ex2300:
    juniper_ex3400:
    juniper_ex4100:
    juniper_ex4300:
    juniper_ex4600:
    juniper_ex4650:


juniper_ex2200:
  hosts:
    my_ex2200:

juniper_ex2300:
  hosts:
    my_ex2230:

juniper_ex3400:
  hosts:
    my_ex3400:

juniper_ex4100:
  hosts:
    my_ex4100:

juniper_ex4300:
  hosts:
    my_ex4300:

juniper_ex4600:
  hosts:
    my_ex4600:

juniper_ex4650:
  hosts:
    my_ex4650:
```

## Configuration globale du rôle

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_config_save_dir  |$HOME/.juniper-configs  |Dossier local (sur le contrôleur Ansible) où seront générés les fichiers de configuration des équipements  |Non |
|ex_config_commitconfirm_delay  |5  |Délai en **minutes** durant lequel la nouvelle configuration devra être confirmée. au bout de ce délai, l'ancienne configuration sera restaurée. Doit être bien plus long que `ex_config_delay_between_commitconfirm_and_commit` afin d'éviter des rollbacks inutiles lorsque le playbook est executé sur plusieurs équipements  |Non |
|ex_config_delay_between_commitconfirm_and_commit  |15  |Délai d'attente en **secondes** entre le *commit confirm* et sa confirmation. Ce délai doit permettre de perdre la connectivité avec l'équipement en cas d'erreur de configuration  |Non |
|ex_config_ignore_commit_warnings  |`["mgd: [0-9]+g config will be applied to ports [0-9]+ to [0-9]+"]`  |Liste des avertissements à ignorer (expressions régulières). Tout avertissement non-spécifié dans cette variable qui sera levé par l'équipement lors de l'analyse de sa configuration fera échouer la tâche  |Non |

## Configuration de base d'un commutateur

### Réseau

Le rôle ne gère qu'une configuration réseau IPv4.

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_config_hostname  |*N/A*  |Nom d'hôte (court)  |Oui  |
|ex_config_location  |*N/A*  |Emplacement  |Oui  |
|ex_config_ipaddress  |*N/A*  |Adresse IP de l'interface de management |Oui  |
|ex_config_netmask  |*N/A*  |Masque de sous-réseau de l'interface de management  |Oui  |
|ex_config_mgmtvlan  |*N/A*  |Nom du VLAN de management  |Oui  |
|ex_config_toip_vlan  |*N/A*  |Nom du VLAN de ToIP  |Non  |
|ex_config_nameservers  |[]  |Liste des IP des serveurs DNS à utiliser  |Non  |
|ex_config_gateway  |  |Passerelle par défaut de l'interface de management  |Non  |
|ex_config_domainname  |  |Nom de domaine de l'équipement  |Non  |
|ex_config_domainsearch  |[]  |Liste de domaines de recherche  |Non  |

### Hachage des mots de passe

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_config_password_hashtype  |sha256  |Méthode de hachage des mots de passe à utiliser. Devrait toujours être à `sha256`, sauf sur les firmwares antérieurs à la version 15 qui ne le supportent pas où `md5` devrait être utilisée  |Non |
|ex_config_password_salt  |CHANGEME  |Chaîne de salage à utiliser lors du hash des mots de passe. Si celle-ci est trop longue pour la méthode de hachage choisie, elle sera tronquée automatiquement.  |Non |

### Classes de login

Les commutateurs Juniper fournissent par défaut les classes de login suivantes :

- operator
- read-only
- superuser ou super-user
- unauthorized

Il est possible de définir des classes de login supplémentaires en les spécifiant dans la variable `ex_config_user_classes`, qui devra être une liste comportant les attributs suivants :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|name  |*N/A*  |Nom de la classe de login (doit être unique)  |Oui  |
|permissions  |*N/A*  |Liste des [permissions](https://www.juniper.net/documentation/us/en/software/junos/user-access-evo/user-access/topics/topic-map/junos-os-login-class.html#id-junos-os-login-classes-overview__d8e136) à octroyer à la classe de login courante  |Oui  |

Exemple :

```yaml
ex_config_user_classes:
  - name: rancid
    permissions:
      - access
      - admin
      - firewall
      - flow-tap
      - interface
      - network
      - routing
      - security
      - snmp
      - storage
      - system
      - trace
      - view
      - view-configuration
```

### Comptes utilisateurs

Le compte root est défini à travers la variable `ex_config_root_user`, qui peut avoir les attributs suivants :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|password  |*N/A*  |Mot de passe  |Non  |
|ssh_pubkeys  |*N/A*  |Dictionnaire pouvant contenir une ou plusieurs des 3 clés suivantes `ssh-ecdsa`, `ssh-ed25519`, `ssh-rsa`, et en valeur la clé associée  |Non  |

Les autres comptes utilisateurs sont définis à travers la variable `ex_config_users`, qui devra être une liste dont chaque élement devra comporter les attributs suivants :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|login  |*N/A*  |Login de l'utilisateur (doit être unique)  |Oui  |
|class  |*N/A*  |Classe de login à attribuer à l'utilisateur  |Oui  |
|uid  |*N/A*  |UID de l'utilisateur (doit être unique)  |Non  |
|password  |*N/A*  |Mot de passe  |Non  |
|ssh_pubkeys  |*N/A*  |Dictionnaire pouvant contenir une ou plusieurs des 3 clés suivantes `ssh-ecdsa`, `ssh-ed25519`, `ssh-rsa`, et en valeur la clé associée  |Non  |

## Configuration des interfaces

### Configuration des VLANs

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|name |*N/A* |Nom du VLAN (doit être unique) |Oui |
|description|*N/A*   |Description du VLAN |Oui |
|vlanid|*N/A* |Nombre entier identifiant le VLAN (doit être unique), et compris entre 1 et 4094. **Ne pas affecter les valeurs 1002 à 1005 qui sont réservées par la norme** |Oui |
|dhcpsnooping|true |Indique si on souhaite activer le DHCP snooping et les fonctionnalités de sécurité de port (Dynamic ARP Inspection et IP source guard) sur ce VLAN |Non |
|jumboframes|false |Passer à True pour activer les jumbo frame (trames Ethernet dont le MTU passe de 1522 à 9216 octets) sur ce VLAN |Non |

```yaml
ex_config_vlans:
  - name: employees
    description: Employees
    vlanid: 10
    dhcpsnooping: false
  - name: students
    description: Students
    vlanid: 11
  - name: storage
    description: storage
    vlanid: 12
    jumboframes: true
    dhcpsnooping: false
```

### Sucre syntaxique pour les interfaces de confiance

Le rôle permet de déclarer des interfaces de confiance en ajoutant la variable d'interface `trusted` positionnée à true.

Le comportement des interfaces de confiance est entièrement paramétrable par une variable globale `ex_config_trusted_settings` dont le contenu (des variables d'interfaces et leurs valeurs) sera fusionné avec celui des interfaces de confiance.
Lors de la fusion, si des variables d'interfaces présentes dans `ex_config_trusted_settings` existent déjà dans l'interface, la valeur déclarée dans l'interface sera préservée (cf. exemple).

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_config_trusted_settings |{is_uplink: true, no_maxhosts: true, dhcptrusted: true, stormtrusted: true} |Variables d'interfaces qui seront ajoutées aux interfaces `trusted` si elles n'existent pas déjà  |Non |

Variables d'interfaces :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|trusted |false |Si `true`, les variables d'interfaces déclarées dans `ex_config_trusted_settings` n'existant pas déjà dans l'interface seront automatiquement ajoutées  |Non |

Exemple, en déclarant :

```yaml
ex_config_trusted_settings:
  is_uplink: true
  no_maxhosts: true
  dhcptrusted: true
  stormtrusted: true

ex_config_interfaces:
  - name: ge-0/0/0
    description: host1
    vlans:
      - employees

  - name: ge-0/0/0
    description: host2
    trusted: false
    vlans:
      - employees

  - name: xe-0/1/0
    description: switch1
    trunk: true
    trusted: true
    vlans:
      - all

  - name: xe-0/1/1
    description: switch2
    trunk: true
    trusted: true
    stormtrusted: false
    vlans:
      - all
```

On obtient en fait la configuration suivante :

```yaml
ex_config_trusted_settings:
  is_uplink: true
  no_maxhosts: true
  dhcptrusted: true
  stormtrusted: true

ex_config_interfaces:
  - name: ge-0/0/0
    description: host1
    vlans:
      - employees
    # Aucun changement, puisque trusted n'est pas spécifié, et vaut donc implicitement false

  - name: ge-0/0/0
    description: host2
    trusted: false
    vlans:
      - employees
    # Aucun changement, puisque trusted vaut false

  - name: xe-0/1/0
    description: switch1
    trunk: true
    trusted: true
    vlans:
      - all
    # Tout le contenu de ex_config_trusted_settings
    is_uplink: true
    no_maxhosts: true
    dhcptrusted: true
    stormtrusted: true

  - name: xe-0/1/1
    description: switch2
    trunk: true
    trusted: true
    stormtrusted: false
    vlans:
      - all
    # Tout le contenu de ex_config_trusted_settings sauf stormtrusted qui était déjà déclaré dans l'interface
    is_uplink: true
    no_maxhosts: true
    dhcptrusted: true
```

### Configuration d'une interface

Les variables d'interfaces s'appliquent aux éléments de `ex_config_interfaces` et `ex_config_laggs`.

Variables d'interfaces :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|name |*N/A* |Nom de l'interface |Oui |
|description| |Description de l'interface |Non |
|speed|*Selon interface et équipement* |Vitesse de l'interface ou du groupe d'interface (**EX4650 uniquement**) |Non |
|disabled|false |Indique que l'interface est désactivée |Non |
|toip |false |Si l'on veut potentiellement raccorder un téléphone sur cette interface. L'interface doit impérativement en mode *access* si cette valeur est à true |Non |
|native_vlan | |Le vlan natif sur l'interface. L'interface doit obligatoirement être en mode trunk si on définit cette option. Le vlan spécifié ici ne **doit pas** faire partie des vlans de l'interface |Non |
|trunk |false |Indique si l'interface est en mode trunk ou access port |Non |
|vlans | |La liste des vlans qui transitent par cette interface |Oui |
|used_by_lagg_or_vcport |false |Indique que l'interface doit être ignorée, car elle sert ailleurs |Non |

Chaque interface est un élément de la liste `ex_config_interfaces` ou de `ex_config_laggs`.
Par exemple :

```yaml
ex_config_interfaces:
  - name: ge-0/0/5
    description: host42
    trusted: true
    vlans:
      - employees

  - name: ge-0/0/34
    description: other_switch
    trunk: true
    trusted: true
    vlans:
      - all
```

> [!IMPORTANT]
> Attention aux ports SFP+ pouvant être à 1Gb/s, 10Gb/s, 25Gb/s, 40Gb/s et 100Gb/s : le préfixe de leur nom varie selon le débit du module enfiché `ge-` pour 1Gb/s, `xe-` pour 10Gb/s et `et-` pour 25Gb/s, 40Gb/s et 100 Gb/s

### PoE

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_config_poeenabled  |true  |Permet de désactiver le PoE globalement sur un équipement en définissant cette variable à `false`.  |Non  |

Variables d'interfaces :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|poe |false |Si l'on veut activer le PoE sur cette interface. Cette valeur est forcée à true lorsque *toip* est à true |Non |

### Configuration d'un redundant trunk group (rtg)

[Présentation Juniper des RTG](https://www.juniper.net/documentation/en_US/junos/topics/topic-map/redundant-trunk-groups.html)

Pour chaque groupe, il va falloir ajouter une configuration "principale" à une interface, et une "secondaire" à une autre. Le fait de rendre une interface membre d'un RTG désactive automatiquement le spanning tree sur cette interface.

Variables d'interfaces de l'interface principale :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|name  |*N/A* |Nom de l'interface RTG (doit commencer par *rtg* suivi d'un nombre) |Oui  |
|primary  |*N/A*  |Indique que l'interface est la principale du RTG, à mettre à `true`  |Oui  |
|wait_before_restore  |1  |Une fois un lien principal à nouveau actif, le commutateur attendra ce délai en secondes (max 600) avant de rebasculer la connectivité sur le lien principal |Non  |

Variables d'interfaces de l'interface secondaire :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|name  |*N/A* |Nom de l'interface RTG (doit commencer par *rtg* suivi d'un nombre) |Oui  |
|secondary  |*N/A*  |Indique que l'interface est la secondaire du RTG, à mettre à `true`  |Oui  |

Par exemple :

```yaml
  - name: xe-0/1/2
    description: Backup link
    trunk: true
    trusted: true
    vlans:
      - all
    rtg:
      name: rtg0
      secondary: true

  - name: xe-0/1/3
    description: Primary link
    trunk: true
    trusted: true
    vlans:
      - all
    rtg:
      name: rtg0
      primary: true
      wait_before_restore: 30
```

### Configuration d'une interface d'agrégat (lagg)

Il existe deux types de laggs configurables :

- l'agrégat standard qui a pour but de mutualiser plusieurs liens afin d'augmenter la bande passante. Cet agrégat repose sur le protocole LACP et requiert d'être paramétré sur les 2 équipements pour que le lien monte
- l'agrégat primary/backup qui a pour but de basculer vers un lien de secours lorsque le principal tombe. Cet agrégat est une alternative (en moins bien) à RTG, mais qui permet d'éviter de créer une boucle active  de trames de contrôles dans le réseau

La plupart des options d'une interface s'appliquent à un lagg (sauf celles qui n'ont pas vraiment de sens, comme `toip`, `poe`, et évidemment `member_of_lagg` et `used_by_lagg_or_vcport`.

Variables d'interfaces spécifiques à une interface lagg `ex_config_laggs`:

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|name |*N/A* |Nom de l'interface (doit **impérativement** commencer par *ae* suivi d'un nombre) |Oui |
|speed | |Débit du lien le moins rapide de l'agrégat : 1G, 10G |Oui |
|periodic |slow |Fréquence de transmission des paquets LACP (`slow\|fast`) |Non |

Variables d'interfaces spécifiques à une interface physique `ex_config_interfaces` :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|member_of_lagg |false |Indique que l'interface fait partie de l’agrégat spécifié. Si cette option est à true, seules *name* et *description* peuvent être définies. Les autres éléments de configuration seront à définir dans l'interface lagg |Non |
|lagg_link_protection |  |Si non défini (par défaut), toutes les interfaces du lagg seront actives. Sinon cette variable permet de déclarer un lagg active/backup (voir plus bas) et ne peut prendre que les valeurs `primary` ou `backup`  |Non |

Chaque interface est un élément de la liste `ex_config_laggs`.
Par exemple :

```yaml
ex_config_laggs:
  - name: ae35
    speed: 10g
    description: other_switch
    trunk: true
    trusted: true
    vlans:
      - all
```

Il faudra également associer ce lagg à ses interfaces physiques dans la configuration des interfaces :

```yaml
ex_config_interfaces:
  - name: xe-0/0/35
    description: "ae35 : other_switch"
    member_of_lagg: ae35

  - name: xe-1/0/35
    description: "ae35 : other_switch"
    member_of_lagg: ae35
```

#### Cas particulier de l'agrégat primary/backup

Cet agrégat se paramètre exactement comme l'agrégat standard, mais il doit impérativement être rattaché à exactement 2 interfaces physiques, et il faut préciser ainsi laquelle sera la principale et laquelle sera celle de secours :

```yaml
ex_config_interfaces:
  - name: xe-0/0/35
    description: "ae35 : other_switch"
    member_of_lagg: ae35
    lagg_link_protection: primary


  - name: xe-1/0/35
    description: "ae35 : other_switch"
    member_of_lagg: ae35
    lagg_link_protection: backup
```

En cas de défaillance du lien principal, le lien de secours s'activera en quelques secondes. Une fois le lien principal rétabli, il faut distinguer 2 comportements distincts selon la génération de commutateurs :

- commutateurs non-ELS (EX2200, EX3300) : il faudra procéder manuellement à la rebascule vers le lien principal, à l'aide de la commande `request interface revert ae35`
- commutateurs ELS (tous les autres) : le commutateur rebasculera automatiquement sur le lien principal

#### Suppression d'un lagg

Supprimer un lagg doit malheureusement parfois se faire en 2 étapes, sans quoi l'application des règles de QoS entraînera une erreur, car il semblerait que le commutateur essaie de les appliquer alors que son "état de compilation interne" lui indique que les interfaces sont encore associées à un lagg.

En première étape, il faut supprimer l'interface de lagg `ae*n*` désirée, et marquer les interfaces physiques associées ainsi :

```yaml
ex_config_interfaces:
  - name: xe-0/0/0
    used_by_lagg_or_vcport: true
    disabled: true

  - name: xe-1/0/0
    used_by_lagg_or_vcport: true
    disabled: true
```

Une fois cette configuration déployée, les 2 interfaces pourront être reconfigurées de la manière désirée.

### Configuration d'un anneau Ethernet Ring Protection Switching (erps)

> [!WARNING]
> Bien que le rôle soit conçu pour prendre en charge des anneaux imbriqués ou en échelle, ces cas de figures n'ont pas été testés

Ressources :

- [Understanding Ethernet Ring Protection Switching](https://www.juniper.net/documentation/us/en/software/junos/high-availability/topics/topic-map/ethernet-ring-protection-switching-understanding.html)
- [Configuring Ethernet Ring Protection Switching on Switches](https://www.juniper.net/documentation/en_US/junos/topics/task/configuration/ethernet-ring-protection-cli.html)

La configuration globale des anneaux se fait via la variable `ex_config_erps`, une liste déclarant chaque anneau, et dont chaque élément peut avoir les paramètres suivants :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ringname |*N/A* |Nom de l'anneau (doit être unique) |Oui |
|control_vlan |*N/A* |Nom du VLAN dédié au contrôle de cet anneau |Oui |
|data_vlans |*N/A* |Liste des noms des VLAN de données transitant sur l'anneau |Oui |
|guard_interval |*valeur par défaut de l'équipement* |Intervalle de garde, en millisecondes (10-2000). Empêche les nœuds de l'anneau de recevoir des messages RAPS obsolètes |Non |
|restore_interval |*valeur par défaut de l'équipement* |**Appliqué uniquement sur le nœud propriétaire de l'anneau**. Délai d'attente avant rétablissement, en minutes (5-12 ou 1-12 selon équipement). Temps pendant lequel le nœud propriétaire attend après le rétablissement de la dernière défaillance, afin de s'assurer de la stabilité de l'anneau avant de rétablir le fonctionnement de l'anneau tel que paramétré |Non |
|compatibility_version |*valeur par défaut de l'équipement* |Version de la norme UIT-T G.8032/Y.1344 à utiliser (1 ou 2). Les équipements legacy (non-ELS) sont *a priori* uniquement compatibles avec la version 1. **Directive exploitée uniquement sur les commutateurs ELS**. |Non |

Une fois les anneaux déclarés, il ne reste plus qu'à déclarer leurs interfaces (physique ou lagg) Est/Ouest, et indiquer quelle sera l'interface de fin.

Variables d'interfaces spécifiques à une interface physique `ex_config_interfaces` ou à une interface lagg `ex_config_laggs` :

| Option (clé) | Option de chaque élément de la liste | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- | --- |
|erps |  |[]  |Liste des anneaux auxquels l'interface est associée |Non |
|     |ringname  |*N/A* |  |Oui |
|     |east_interface  |False |Marque l'interface comme interface Est pour l'anneau spécifié par ringname  |Non |
|     |west_interface  |False |Marque l'interface comme interface Ouest pour l'anneau spécifié par ringname  |Non |
|     |ring_protection_link_end  |False |Marque l'interface comme bloquée par défaut en fonctionnement nominal, et déclare l'équipement comme propriétaire de l'anneau. **Il DOIT y avoir une et une seule interface avec cette valeur à True dans tout l'anneau, et le rôle ne peut pas assurer la vérification de cette contrainte**  |Non |

#### Particularités des interfaces membres d'un anneau

Une interface membre d'un anneau doit impérativement être déclarée comme trunk, puisqu'elle fera transiter au minimum un vlan de données et le vlan de contrôle de l'anneau.

ERPS étant incompatible avec les protocles spanning-tree, le rôle désactivera automatiquement le spanning-tree sur toutes les interfaces membres d'un anneau.

Le rôle va automatiquement paramétrer les VLAN de l'interface en aggrégeant :

1. Les VLANs de données `data_vlans` déclarés pour chaque anneau dont l'interface est membre
2. Les VLANs de contrôle `control_vlan` déclarés pour chaque anneau dont l'interface est membre
3. Les VLANs éventuellement déclarés dans la configuration de l'interface. C'est possible, même si dans l'usage courant il n'y a probablement aucun VLAN à déclarer au niveau de l'interface

#### Exemple

```yaml
ex_config_erps:
  - ringname: erps_ring1
    control_vlan: erps-control-ring1
    data_vlans:
      - employees
      - students
      - storage

  - ringname: erps_ring2
    control_vlan: erps-control-ring2
    data_vlans:
      - employees
      - students
```

```yaml
ex_config_interfaces:
  - name: ge-0/0/0
    trunk: true
    trusted: true
    erps:
      - ringname: erps_ring1
        east_interface: true
        ring_protection_link_end: true

  - name: ge-0/0/1
    trunk: true
    trusted: true
    erps:
      - ringname: erps_ring1
        west_interface: true
```

### Mise en place de port-mirroring

Il est parfois nécessaire de mettre en oeuvre du port-mirroring afin d'effectuer des captures réseau.

Variables d'interfaces :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|portmirroring  |  |Dictionnaire avec 2 sous-éléments (voir exemple ci-dessous) : `name`, dont la valeur sera le nom de la règle de mirroring dans la configuration de l'équipement (doit être unique) et `from`, une liste d'interfaces dont le trafic sera répliqué sur l'interface courante. Si cette option est déclarée toutes les autres variables d'interfaces seront ignorées à l'exception de *name*, *description* et *disabled*, et le port n'aura donc aucun vlan affecté, sera retiré du spanning tree, et des interfaces toip. **Si le port fait partie d'un agrégat, il en sera retiré également**  |Non  |

#### Exemple

Avec la configuration suivante, le trafic des interfaces ge-0/0/25 et ge-0/0/26 sera répliqué sur l'interface ge-0/0/5 :

```yaml
ex_config_interfaces:
  - name: ge-0/0/5
    description: Exemple portmirroring
    portmirroring:
      name: mirror-example
      from:
        - ge-0/0/25
        - ge-0/0/26
```

## Configuration des services

### Envoi des logs vers des serveurs Syslog

Afin de propager les logs vers un ou plusieurs serveurs Syslog, il est possible de déclarer la variable `ex_config_syslogservers` contenant une liste de serveurs Syslog dont chaque entrée doit comporter les attributs suivants :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ip  |*N/A*  |Adresse IP du serveur Syslog  |Oui  |
|port  |*N/A*  |Port du serveur Syslog  |Oui  |
|comment  |*N/A*  |Commentaire concernant le serveur Syslog (*e.g.* son nom de domaine)  |Oui  |

Par exemple :

```yaml
ex_config_syslogservers:
  - ip: 192.168.42.1
    port: 514
    comment: syslog1.example.com
```

### Client NTP

Afin de synchroniser l'horloge de l'équipement, il est possible de déclarer la variable `ex_config_ntpservers` contenant une liste de serveurs NTP dont chaque entrée doit comporter les attributs suivants :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ip  |*N/A*  |Adresse IP du serveur NTP  |Oui  |
|comment  |*N/A*  |Commentaire concernant le serveur NTP (*e.g.* son nom de domaine)  |Oui  |

Par exemple :

```yaml
ex_config_ntpservers:
  - ip: 192.168.42.1
    comment: ntp1.example.com
  - ip: 192.168.42.2
    comment: ntp2.example.com
```

### SNMP

Il est possible d'activer le service SNMP (v2) en lecture-seule sur les équipements sur différentes communautés.

Chaque communauté doit être un élément de la liste `ex_config_snmpcommunities` comportant les attributs suivants :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|name  |*N/A*  |Nom de la communauté (doit être unique)  |Oui  |
|clients  |[]  |Liste des clients autorisés, dont chaque entrée doit impérativement comporter les attributs `ip` (adresse IP du réseau autorisé), `netmask` (masque du réseau autorisé) et `comment` (commentaire concernant l'entrée autorisée). Si la liste est vide, l'accès à la communauté sera autorisé depuis n'importe quel client  |Non  |

Par exemple :

```yaml
ex_config_snmpcommunities:
  - name: public
    clients:
      - ip: 192.168.42.42
        netmask: 255.255.255.255
        comment: Monitoring server
      - ip: 192.168.253.0
        netmask: 255.255.255.0
        comment: IT subnet
```

Il est également possible de déclarer des groupes de cibles devant recevoir des traps SNMP émis par les équipements via la variable `ex_config_snmptrapgroups` dont chaque entrée doit comporter les attributs suivants :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|name  |*N/A*  |Nom du groupe de cibles SNMP (doit être unique)  |Oui  |
|categories  |Toutes sauf `timing-events`  |Liste des [catégories de traps](https://www.juniper.net/documentation/us/en/software/junos/cli-reference/topics/ref/statement/categories-edit-snmp.html) à transmettre aux cibles.  |Non  |
|targets  |  |Liste des cibles de ce groupe, dont chaque entrée doit impérativement comporter les attributs `ip` (adresse IP du réseau autorisé) et `comment` (commentaire concernant la cible déclarée)  |Non  |

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ip  |*N/A*  |Adresse IP de la cible des traps SNMP  |Oui  |
|targets  |*N/A*  |Commentaire concernant la cible des traps SNMP  |Oui  |

Par exemple :

```yaml
ex_config_snmptrapgroups:
  - name: monitoring
    categories:
      - authentication
      - chassis
      - link
      - remote-operations
      - routing
      - rmon-alarm
      - configuration
      - services
    targets:
      - ip: 192.168.42.42
        comment: Monitoring server
```

### Règles de filtrage rudimentaires (firewall)

Il est possible d'interdire toute communication avec l'équipement depuis une liste de réseaux déclarée dans `ex_config_firewall_denied_ips` dont chaque entrée doit comporter les attributs suivants :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ip  |*N/A*  |Adresse IP du réseau filtré  |Oui  |
|netmask  |*N/A*  |Masque du réseau filtré (*e.g.* 255.255.255.255 pour ne filtrer que l'adresse IP déclarée)  |Oui  |
|comment  |*N/A*  |Commentaire concernant l'entrée filtrée  |Oui  |

Par exemple :

```yaml
ex_config_firewall_denied_ips:
  - ip: 192.168.42.42
    netmask: 255.255.255.255
    comment: filtered_host
  - ip: 192.168.18.0
    netmask: 255.255.255.0
    comment: Students subnet
```

### Protection storm-control

Le storm control est activé par défaut sur tous les commutateurs. Il est possible de paramétrer son comportement par les variables suivantes :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_config_enable_stormcontrol  |true  |Permet de désactiver totalement le storm control en définissant la valeur à `false`  |Non  |
|ex_config_stormtrusted_default  |false  |Valeur par défaut qui sera appliquée si la variable d'interface `stormtrusted` n'est pas définie  |Non  |
|ex_config_stormcontrol_bandwidthlevel  |4000  |Seuil de bande passante en kb/s du trafic surveillé combiné au dela duquel le storm-control lèvera une alerte   |Non  |
|ex_config_stormcontrol_shutdown  |false  |Si `true`, l'alerte désactivera l'interface pour la durée définie dans `ex_config_stormcontrol_disable_timeout`   |Non  |
|ex_config_stormcontrol_disable_timeout  |60  |Durée en secondes durant laquelle une interface en alerte sera désactivée  |Non  |
|ex_config_stormcontrol_monitor_broadcast  |true  |Si `true`, le trafic broadcast sera surveillé  |Non  |
|ex_config_stormcontrol_monitor_multicast  |false  |Si `true`, le trafic multicast sera surveillé  |Non  |
|ex_config_stormcontrol_monitor_registered_multicast  |false  |Si `true`, seul le trafic multicast enregistré (adresses MAC multicast comprises entre 01-00-5E-00-00-00-00 et 01-00-5E-7F-FF) sera surveillé. **Directive exploitée uniquement sur les commutateurs ELS**.  |Non  |
|ex_config_stormcontrol_monitor_unregistered_multicast  |false  |Si `true`, le trafic multicast non-enregistré (adresses MAC multicast non-comprises entre 01-00-5E-00-00-00-00 et 01-00-5E-7F-FF) sera surveillé. **Directive exploitée uniquement sur les commutateurs ELS**.  |Non  |
|ex_config_stormcontrol_monitor_unknown_unicast  |false  |Si `true`, le trafic unicast inconnu sera surveillé  |Non  |

Voir [Comprendre Storm Control](https://www.juniper.net/documentation/fr/fr/software/junos/security-services/topics/concept/rate-limiting-storm-control-understanding.html) pour plus de détails

Variables d'interfaces :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|stormtrusted |{{ ex_config_stormtrusted_default }} |Désactive la détection de tempête sur l'interface, si mis à `true`. |Non |

### DHCP snooping, dynamic arp inspection et IP source guard

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_config_portsecurity_enable_dhcpsnooping  |false  |Active le [DHCP snooping](https://www.juniper.net/documentation/en_US/junos/topics/concept/port-security-dhcp-snooping.html)  |Non  |
|ex_config_portsecurity_enable_dynamic_arp_inspection  |false  |Active [Dynamic ARP inspection](https://www.juniper.net/documentation/en_US/junos/topics/task/configuration/understanding-and-using-dai.html#id-understanding-arp-spoofing-and-inspection). L'option *ex_config_portsecurity_enable_dhcpsnooping* doit également être à `true` pour que la fonctionnalité soit active  |Non  |
|ex_config_portsecurity_enable_ip_source_guard  |false  |Active [IP Source Guard](https://www.juniper.net/documentation/en_US/junos/topics/concept/port-security-ip-source-guard.html). L'option *ex_config_portsecurity_enable_dhcpsnooping* doit également être à `true` pour que la fonctionnalité soit active  |Non  |
|ex_config_dhcptrusted_default  |  |Définit la valeur par défaut qui sera appliquée à la variable d'interface `dhcptrusted` lorsque celle-ci n'est pas définie. Par défaut, lorsque `ex_config_dhcptrusted_default` n'est pas définie, vaudra `true` pour les interfaces en mode trunk, et `false` pour les interfaces en mode access. Si `ex_config_dhcptrusted_default` est définie, sa valeur sera appliquée quelque soit le mode de l'interface.   |Non  |

Variables d'interfaces :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|dhcptrusted |Variable selon {{ ex_config_dhcptrusted_default }}  |Valable uniquement si le commutateur a l'option `ex_config_portsecurity_enable_dhcpsnooping` activée. <br/> <br/> Indique si l'on doit faire confiance et donc ignorer les règles de dhcp snooping, Dynamic ARP Inspection et IP Source Guard sur cette interface. <br/> <br/> Par défaut (si `dhcptrusted` et `ex_config_dhcptrusted_default` ne sont pas définies), une interface en access port a cette option à `false`, et une interface en mode trunk a cette option à `true`. Si `ex_config_dhcptrusted_default` est définie, c'est sa valeur qui sera celle par défaut.  |Non |
|macstatic |  |Valable uniquement si le commutateur a l'option `ex_config_portsecurity_enable_dhcpsnooping` activée. <br/> <br/> Permet de déclarer des associations adresses IP/MAC/VLAN pour les équipements en adressage statique, ou avec un renouvellement de bail DHCP erratique. Ceci n'empêche en rien les équipements ayant obtenu un bail DHCP d'utiliser l'interface. Voir exemple de configuration ci-dessous.  |Non |

#### Exemple de configuration de `macstatic`

```yaml
ex_config_interfaces:
  - name: ge-0/0/5
    description: Exemple macstatic
    toip: true
    vlans:
      - employees
    macstatic:
      employees:
        192.168.0.1: 00:d3:ad:be:ef:01
        192.168.0.2: 00:d3:ad:be:ef:02
      toip:
        192.168.1.1: 00:d3:ad:be:ef:11
      students:
        # L'entrée ci-dessous sera ignorée puisque le vlan n'est pas affecté à l'interface
        192.168.2.1: 00:d3:ad:be:ef:21
```

### Restrictions du nombre d'équipements raccordés sur des interfaces

Il est possible de déclarer une limite du nombre d'adresses MAC actives sur une interface, par exemple pour empêcher l'utilisation non-déclarée d'un commutateur.
La fonction n'est activée que sur les interfaces dont les variables d'interfaces `is_uplink` et `no_maxhosts` ne sont pas définies ou valent `false`.

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_config_defaultmaxhosts | |Limite le nombre d'équipements (adresses mac) autorisés à se connecter, sur toutes les interfaces activées, en access port et dont la variable d'interfaces `no_maxhosts` n'est pas définie ou vaut `false`. Cette valeur est automatiquement incrémentée d'une unité si la ToIP est activée afin de comptabiliser le téléphone. Si la limite est dépassée, les paquets provenant des nouveaux équipements seront rejetés par le commutateur. Par défaut, aucune limite n'est active. Cette valeur peut être définie finement ou surchargée via le paramètre d'interface `maxhosts`|Non |

Variables d'interfaces :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|maxhosts | |Limite le nombre d'équipements (adresses mac) autorisés à se connecter via cette interface. Cette valeur est automatiquement incrémentée d'une unité si la ToIP est activée afin de comptabiliser le téléphone. Si la limite est dépassée, les paquets provenant des nouveaux équipements seront rejetés par le commutateur. Par défaut, aucune limite n'est active, sauf si le paramètre global `ex_config_defaultmaxhosts` est défini. Ce paramètre n'est pris en compte que sur les interfaces activées, en access port et dont la variable d'interfaces `no_maxhosts` n'est pas définie ou vaut `false`|Non |
|no_maxhosts |false |Désactive les restrictions sur l'interface, même lorsque les directives `maxhosts` ou `ex_config_defaultmaxhosts` sont déclarées |Non |
|is_uplink  |false  |Si `true`, indique que l'interface sert à raccorder un autre commutateur/équipement réseau. Sa valeur a une influence sur le comportement de la COS/QoS, du spanning tree, des restrictions du nombre d'équipements raccordés sur des interfaces et du 802.1X   |Non  |

### Querier multicast

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_config_igmpquerier  |{}  |Dictionnaire ayant pour clés les VLAN sur lesquels le commutateur doit faire office de *querier IGMP*, et pour valeurs (éventuelles) l'IP (v4) source que le *querier* utilisera pour émettre les messages IGMP sur ce VLAN. Cette IP (v4) source n'a pas d'autre intérêt que de servir à élire le querier par défaut lorsqu'il y en a plus d'un sur le réseau. Si la valeur n'est pas définie (`None`), l'IP (v4) définie dans `ex_config_ipaddress` sera utilisée. Un VLAN particulier `all` peut être déclaré : sa configuration s'appliquera alors à l'ensemble des VLAN non spécifiés explicitement. **Directive exploitée uniquement sur les commutateurs ELS**  |Non  |
|ex_config_mldquerier  |{}  |Dictionnaire ayant pour clés les VLAN sur lesquels le commutateur doit faire office de *querier MLD*, et pour valeurs (éventuelles) l'IP (v6) source que le *querier* utilisera pour émettre les messages MLD sur ce VLAN. Cette IP (v6) source n'a pas d'autre intérêt que de servir à élire le querier par défaut lorsqu'il y en a plus d'un sur le réseau. Un VLAN particulier `all` peut être déclaré : sa configuration s'appliquera alors à l'ensemble des VLAN non spécifiés explicitement. **Directive exploitée uniquement sur les commutateurs ELS**  |Non  |

### Provisionnement des membres d'un châssis virtuel

La configuration d'un châssis virtuel (VC) n'est pas assurée par ce rôle. Toutefois, il est possible de provisionner la liste des membres du VC dans `ex_config_virtual_chassis` dont chaque entrée doit comporter les attributs suivants :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|memberid  |*N/A*  |Identifiant du membre dans le VC (le premier commençant à 0)  |Oui  |
|serial  |*N/A*  |Numéro de série de l'équipement  |Oui  |

Par exemple :

```yaml
ex_config_virtual_chassis:
  - memberid: 0
    serial: AB123456789001
  - memberid: 1
    serial: AB123456789002
```

### Balises pour Netmagis

Le rôle permet d'ajouter automatiquement les balises requises par le module *topo* de [Netmagis](http://netmagis.org/config-topo.html).

Activation de la fonctionnalité :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_config_enable_netmagis_descriptions  |false  |Ajoute les balises spécifiques au module topo de Netmagis à la fin des descriptions d'interfaces  |Non |

Déclaration des numéros de lien sur les interfaces appropriées avec les variables d'interfaces :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|linknumber |  |Le numéro de lien pour Netmagis, à ne renseigner que si l'interface est raccordée à un autre commutateur. Le même numéro doit être déclaré sur l'interface de l'autre commutateur. Ce numéro doit être unique et déclaré dans netmagis (`Topo > Numéro de lien`). **Paramètre pris en compte uniquement si `ex_config_enable_netmagis_descriptions` vaut `true`**  |Non |

### 802.1X (incomplet)

> [!CAUTION]
> **Fonctionnalité en cours de développement**

Afin de configurer un ou plusieurs serveurs Radius, il est possible de déclarer la variable `ex_config_radiusservers` contenant une liste de serveurs Radius dont chaque entrée doit comporter les attributs suivants :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ip  |*N/A*  |Adresse IP du serveur Radius  |Oui  |
|port  |*N/A*  |Port du serveur Radius  |Oui  |
|password  |*N/A*  |Secret permettant de se connecter au serveur Radius  |Oui  |

Par exemple :

```yaml
ex_config_radiusservers:
  - ip: 192.168.42.1
    port: 1812
    password: SeCr3t_p4s5w0rD
```

Pour le 802.1X, tout se déclare sur l'interface.

Variables d'interfaces :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|dot1x | |Si définie, active le 802.1X sur l'interface. Les valeurs possible de cette option sont <br/> - `dot1x` : active uniquement le 802.1X standard sur le port <br/> - `macradius` : active uniquement l'authentification macradius sur le port <br/> - `both` : active à la fois les authentifications 802.1X **et** macradius sur le port |Non |

## Configuration du protocole spanning tree

[Comparatif Juniper des protocoles spanning tree](https://www.juniper.net/documentation/us/en/software/junos/stp-l2/topics/topic-map/spanning-tree-configuring-mstp.html#id-understanding-mstp__d6613e107)

Les protocoles spanning tree suivants sont supportés par le rôle :

- [rstp](https://www.juniper.net/documentation/en_US/junos/topics/topic-map/spanning-tree-configuring-rstp.html)
  - rapide
  - peu couteux en CPU
  - ne gère que les boucles physiques, et ne tient pas compte des vlans: il faut donc être vigilant à ce que tous les VLANs passent par tous les liens redondants, faute de quoi il y aura des risques de discontinuité de VLAN
- [mstp](https://www.juniper.net/documentation/en_US/junos/topics/topic-map/spanning-tree-configuring-mstp.html)
  - rapide
  - peu couteux en CPU
  - gère des groupes de VLANs (msti)
  - permet d'avoir de l'actif/actif en le paramétrant convenablement
  - interopérable avec RSTP

### Protection de racine

Quel que soit le protocole spanning-tree actif, le rôle permet d'y activer le mécanisme de protection de racine (*root protection*).
Si une BPDU arrive sur une interface avec ce mécanisme activé, et que cette BPDU aurait pour conséquence de modifier le commutateur racine en place, le commutateur désactivera l'interface en question pour préserver la racine et la topologie spanning-tree.

Cette fonctionnalité n'est donc activée que sur les interfaces *edge*, si la variable d'interfaces `is_uplink` n'est pas définie ou vaut `false`.

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_config_enable_rootprotection  |false  |Si `true`, active la fonctionnalité de protection de racine spanning-tree   |Non  |

Variables d'interfaces :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|is_uplink  |false  |Si `true`, indique que l'interface sert à raccorder un autre commutateur/équipement réseau. Sa valeur a une influence sur le comportement de la COS/QoS, du spanning tree, des restrictions du nombre d'équipements raccordés sur des interfaces et du 802.1X   |Non  |

- [Protection de racine (Root Protection)](https://www.juniper.net/documentation/en_US/junos/topics/topic-map/spanning-tree-root-protection.html#id-understanding-root-protection-for-spanning-tree-instance-interfaces-in-a-layer-2-switched-network).

### Filtrage des BPDU

Le rôle permet en outre d'activer le filtrage des BPDU sur des interfaces, pour éviter des problèmes d'incompatibilité et de changement de topologie de manière plus douce qu'avec la protection de racine, simplement en ignorant les BPDU.

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_config_bpdu_block_default  |false  |Permet de définir la valeur par défaut qui sera appliquée à la variable d'interfaces `bpdu_block` lorsque celle-ci n'est pas définie  |Non  |

Cette fonctionnalité ne sera pas activée si la variable d'interfaces `stp_link_cost` est définie sur l'interface.

Variables d'interfaces :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|bpdu_block  |{{ ex_config_bpdu_block_default }}  |Si `true`, active le filtrage des BPDU arrivant sur cette interface   |Non  |

- [Protection BPDU pour les protocoles Spanning-Tree](https://www.juniper.net/documentation/us/en/software/junos/stp-l2/topics/topic-map/spanning-tree-bpdu-protection.html).

### Désactivation du spanning-tree

#### Configuration globale

Pour désactiver le spanning-tree, il suffit de déclarer un protocole non-reconnu.

Exemple :

```yaml
# STP configuration
ex_config_stp:
  protocol: None
```

| Option (clé) | Sous-clés possibles | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_config_stp  |  |Configuration globale du spanning tree  |Oui  |
|  |protocol  |Le protocole STP à utiliser. `rstp` ou `mstp`. Toute autre valeur désactivera le spanning tree sur les commutateurs  |Oui  |

### RSTP

Le protocole RSTP ne gère que les boucles physiques, et ne tient pas compte des vlans: il faut donc être vigilant à ce que tous les VLANs passent par tous les liens redondants, faute de quoi il y aura des risques de discontinuité de VLAN.

#### Configuration globale

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_config_stp_default_bridge_priority  |32k  |Permet de définir la priorité spanning tree par défaut de tous les équipements lorsque `ex_config_stp_bridge_priority` n'est pas définie  |Non  |
|ex_config_stp_default_edge_link_cost  |200000000  |Permet de définir le coût spanning-tree par défaut d'une interface *edge*  |Non  |
|ex_config_stp_bridge_priority  |{{ ex_config_stp_default_bridge_priority }}  |Permet de surcharger la priorité spanning tree du commutateur : celui avec la valeur la plus faible sera élu racine (root).  |Non  |

Exemple de configuration stp :

```yaml
# STP configuration
ex_config_stp:
  protocol: rstp
```

| Option (clé) | Sous-clés possibles | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_config_stp  |  |Configuration globale du spanning tree  |Oui  |
|  |protocol  |Le protocole STP à utiliser. `rstp` ou `mstp`. Toute autre valeur désactivera le spanning tree sur les commutateurs  |Oui  |

#### Configuration d'une interface

Variables d'interfaces :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|stp_link_cost  |[Déterminé automatiquement par l'équipement selon le type d'interface](https://kb.juniper.net/InfoCenter/index?page=content&id=KB31861)  |Coût du lien pour le spanning tree. Pour le protocole MSTP, s'appliquera uniquement à la CIST. Si la valeur n'est pas définie, le commutateur choisira un coût en fonction du débit du lien   |Non  |
|disable_stp  |false  |Si `true`, désactive le spanning-tree sur cette interface  |Non  |
|is_uplink  |false  |Si `true`, indique que l'interface sert à raccorder un autre commutateur/équipement réseau. Sa valeur a une influence sur le comportement de la COS/QoS, du spanning tree, des restrictions du nombre d'équipements raccordés sur des interfaces et du 802.1X   |Non  |

Si `is_uplink` n'est pas définie ou vaut `false`, l'interface sera déclarée comme `edge`, et son coût par défaut sera `ex_config_stp_default_edge_link_cost`.

Exemple de paramétrage d'une interface :

```yaml
ex_config_laggs:
  - name: ae10
    stp_link_cost: "2000"
```

### MSTP

Le protocole MSTP découpe le réseau de sa région en plusieurs topologies spanning tree.

- Chaque MSTI définie par l'utilisateur est une topologie, qui contient les VLANs que l'utilisateur a affecté. Les MSTI sont facultatives, mais n'en créer aucune revient à utiliser le RSTP
- La CIST (forcément présente) est une topologie, qui va contenir tous les VLAN non affectés à une MSTI

En fonctionnement avec des liens redondants, il est possible d'avoir une configuration où un lien de secours pour la CIST sera un lien principal pour une MSTI et réciproquement, permettant ainsi de répartir le trafic réseau.

#### Configuration globale

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_config_stp_default_bridge_priority  |32k  |Permet de définir la priorité spanning tree par défaut de tous les équipements lorsque `ex_config_stp_bridge_priority` ou `ex_config_msti_bridge_priority` ne sont pas définies.  |Non  |
|ex_config_stp_default_edge_link_cost  |200000000  |Permet de définir le coût spanning-tree par défaut d'une interface *edge*  |Non  |
|ex_config_stp_bridge_priority  |{{ ex_config_stp_default_bridge_priority }}  |Permet de surcharger la priorité spanning tree du commutateur : celui avec la valeur la plus faible sera élu racine (root). Pour le protocole MSTP, s'appliquera uniquement à la CIST  |Non  |
|ex_config_msti_bridge_priority  |{{ ex_config_stp.msti.*mstiID*.bridge_priority }} et sinon {{ ex_config_stp_default_bridge_priority }}  | **Ne sert qu'au protocole MSTP.** Dictionnaire où la clé est le mstiID et la valeur la priorité spanning tree de cet MSTI. Permet de surcharger la priorité spanning tree de cet MSTI sur le commutateur : celui avec la valeur la plus faible sera élu racine (root)  |Non  |
|ex_config_mstp_all_vlans  |[]  | **Ne sert qu'au protocole MSTP.** Liste de tous les VLAN utilisés dans la configuration MSTP - même ceux qui ne sont pas déclarés sur l'équipement. Le format est identique à celui de la variable `ex_config_vlans`.   |Non  |

Exemple de configuration stp :

```yaml
# STP configuration
ex_config_mstp_all_vlans: "{{ ex_config_vlans }}"
ex_config_stp:
  protocol: mstp
  mstp_settings:
    configname: whatever_you_want
    revlevel: 1
    mstis:
      # storage vlan only
      - id: 1
        vlans:
          - storage
      # Some other vlans
      - id: 2
        vlans:
          - employees
          - students
      # All others vlans
      - id: 3
        vlans:
          - -REMAINING-
          - -UNDEFINED-
```

| Option (clé) | Sous-clés possibles | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_config_stp  |  |Configuration globale du spanning tree  |Oui  |
|  |protocol  |Le protocole STP à utiliser. `rstp` ou `mstp`. Toute autre valeur désactivera le spanning tree sur les commutateurs  |Oui  |
|  |mstp_settings  |Les paramètres spécifiques du protocole MSTP  |Oui, si `protocol` est à `mstp`  |

##### mstp_settings

| Option (clé) | Sous-clés possibles | Description | Obligatoire |
| --- | --- | --- | --- |
|configname  |  |Nom de la configuration MSTP  |Oui  |
|revlevel  |  |Version de la configuration MSTP  |Oui  |
|mstis  |  |Liste des MSTIS à déclarer  |Oui  |
|       |id  |L'identifiant de la MSTI (1..4094)  |Oui  |
|       |vlans  |La liste des noms de vlans à rattacher à cette MSTI. Un vlan ne peut être rattaché qu'à une MSTI. Il est également possible de spécifier le mot-clé `-REMAINING-`, qui sera remplacé par tous les VLANs déclarés sur le réseau et non affectés à une autre MSTI, et le mot-clé `-UNDEFINED-` qui sera remplacé par tous les VLANs non déclarés sur le réseau et non affectés à une autre MSTI  |Oui  |

#### Configuration d'une interface

Variables d'interfaces :

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|stp_link_cost  |[Déterminé automatiquement par l'équipement selon le type d'interface](https://kb.juniper.net/InfoCenter/index?page=content&id=KB31861)  |Coût du lien pour le spanning-tree sur la CIST  |Non  |
|msti_link_cost  |  |Dictionnaire où la clé est le mstiID et la valeur coût du lien pour cette MSTI  |Non  |
|disable_stp  |false  |Si `true`, désactive le spanning-tree sur cette interface  |Non  |
|is_uplink  |false  |Si `true`, indique que l'interface sert à raccorder un autre commutateur/équipement réseau. Sa valeur a une influence sur le comportement de la COS/QoS, du spanning tree, des restrictions du nombre d'équipements raccordés sur des interfaces et du 802.1X   |Non  |

Si `is_uplink` n'est pas définie ou vaut `false`, l'interface sera déclarée comme `edge`, et son coût par défaut sera `ex_config_stp_default_edge_link_cost`.

Exemple de paramétrage d'une interface :

```yaml
ex_config_laggs:
  - name: ae10
    stp_link_cost: "200000"
    msti_link_cost:
      1: "2000"
      2: "200000"
      3: "200000"
```

## QoS / CoS

> [!IMPORTANT]
> Le paramétrage des CoS étant variable selon le type d'équipement (oui les EX4600/EX4650, c'est à vous que je pense), et les réglages possibles étant infinis, il est impossible de garantir que cette partie du rôle pourra appliquer la politique CoS de vos rêves. En l'état actuel du rôle, la politique définie est appliquée à l'ensemble des interfaces actives.

> [!WARNING]
> Compte tenu de la complexité des règles CoS et de la quantité importante des valeurs possibles des nombreuses variables, le rôle Ansible n'effectue aucune vérification préalable. Il convient donc de valider la configuration sur les différentes familles d'équipements **avant** de la déployer en production

Il est possible de définir des niveaux de priorité très finement selon les flux réseau. Sous Juniper, c'est appelé CoS (Class of Service).
Par exemple, sur [Renater](https://services.renater.fr/services_ip/classes_de_services) la QoS se base sur le champ DSCP (Differenciated Service Code Point).

Il va falloir distinguer 2 types d'interfaces réseau et leur appliquer des règles CoS distinctes :

1. Les interfaces d'interconnexion : ces interfaces ne devraient avoir qu'à appliquer la CoS selon le champ DSCP **déjà inclus dans le paquet IP**. Dans notre rôle Ansible, on les distingue par la présence d'une variable `is_uplink` présente et de valeur *true*
2. Les autres interfaces : ces interfaces devront respecter un champ DSCP en place, mais également vérifier le type de flux réseau qui transite, afin le cas échéant d'y écrire la valeur DSCP adéquate. Cela se base sur des règles de type pare-feu (IP source, destination, protocole tcp/udp, n° de port...). Dans notre rôle Ansible, on les distingue par la variable `is_uplink` absente ou de valeur *false*

Voici la structure de base de la configuration CoS via Ansible.

```yaml
ex_config_qos:
  qos_company:
    enabled: true
    ip_prefixes:
      hosts_toip:
        - "192.168.250.0/24"
      hosts_backup:
        - "192.168.30.3/32"
        - "192.168.30.42/32"
    classes:
      - (...)
    policers:
      - (...)
```

Tout se fait par un dictionnaire `ex_config_qos`, contenant lui même un (ou plusieurs, même si ça n'est pas forcément une bonne idée) dictionnaire dont la clé est le nom de la config CoS, et la valeur un dictionnaire contenant la configuration. Cette configuration est découpée en 4 parties :

| Option (clé) | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|enabled  |false  |Indique si cette configuration sera active ou non sur l'équipement  |Non  |
|ip_prefixes  |{}  |Dictionnaire contenant en clé un nom d'alias d'adresses IP/plages réseau, et en valeur une liste de subnets en notation CIDR (192.168.42.0/24). Ces alias pourront servir dans les règles de filtrage des flux réseau  |Non  |
|classes  |N/A  |Liste de configurations de classes de service, voir ci-dessous pour les détails  |Oui  |
|policers  |[]  |Liste de règles de limitation de flux, si je devais traduire *policer* dans ce contexte, ce serait par "limiteur", voir ci-dessous pour les détails. Ces règles ne sont pas obligatoire, car le rôle du limiteur est d'empêcher un flux de dépasser des valeurs limite (en débit par exemple), mais c'est à utiliser à la marge car assez brutal lors d'un dépassement  |Non  |

### classes

Exemple de classe :

```yaml
    classes:
      - name: voice
        codepoints: "ef" # Expedited-forwarding traffic
        loss_priority: low
        queuenum: 1
        scheduler:
          buffer_size: "10%"
          priority: "strict-high"
        mf_classifier_rules:
          - name: voip
            from:
              source_prefix_list:
                - hosts_toip
              destination_prefix_list:
                - hosts_toip
            then:
              forwarding_class: true
              loss_priority: low
              policer: voip_limit
```

| Option (clé) | Sous-clés possibles | Description | Obligatoire |
| --- | --- | --- | --- |
|name  |  |Nom unique (dans l'ensemble de la configuration) de la classe  |Oui  |
|codepoints  |  |[Valeur DSCP](https://www.juniper.net/documentation/en_US/junos/topics/task/configuration/cos-classifiers-cli.html) associée à cette classe |Oui  |
|loss_priority  |  |Définit la priorité de rejet de paquet en cas de congestion. Valeurs possibles `high` et `low`  |Oui  |
|queuenum  |  |ID de la file d'attente associée à cette [classe](https://www.juniper.net/documentation/en_US/junos/topics/concept/forwarding-classes-default-cos-config-guide.html) |Oui  |
|scheduler  |  |Valeurs de réservations et limites (softs) de cette classe pour l'ordonnanceur de paquets. Les limites pourront être dépassées s'il reste de la bande passante  |Oui  |
|  |buffer_size  |Réservation d'une partie du buffer de sortie (en pourcentage), ou `remainder` indiquant de faire avec ce qui est disponible  |Non  |
|  |transmit_rate  |Réservation de bande passante (minimum garanti). La valeur peut être un entier (3200..6400000000000) en bits par seconde, ou un pourcentage (doit finir par '%') |Non  |
|  |shaping_rate  |Limite de bande passante de la classe. La valeur peut être un entier (3200..6400000000000) en bits par seconde, ou un pourcentage (doit finir par '%') |Non  |
|  |priority  |Priorité de cette classe (`low` ou `strict-high`) |Non  |
|mf_classifier_rules  |  |Règles de classification des paquets (type pare-feu). Voir ci-dessous pour les détails. Ces règles ne sont pas obligatoires : s'il n'y en a pas, les paquets seront classés en *best-effort* par défaut. De plus, le commutateur intègre déjà quelques règles de classification. Il convient donc de définir ces règles pour les flux particuliers du réseau (toip, sauvegarde, visio...)  |Non |

#### mf_classifier_rules

| Option (clé) | Sous-clés possibles | Description | Obligatoire |
| --- | --- | --- | --- |
|name  |  |Nom unique (dans l'ensemble de la configuration) de la règle de classification  |Oui  |
|if  |  |Conditions qu'un paquet doit réunir pour être classé par cette règle  |Oui  |
| |source_prefix_list  |(Liste) Le paquet doit avoir une adresse IP source correspondant à une de celles déclarées dans un des *ip_prefixes* spécifiés.  |Non  |
| |source_address  |(Liste) Le paquet doit avoir une adresse IP source correspondant à une de celles spécifiées.  |Non  |
| |source_port  |(Liste) Le paquet doit avoir un port source correspondant à un de ceux spécifiés. Il est possible de spécifier un intervalle de ports comme par exemple `10000-20000` |Non  |
| |destination_prefix_list  |(Liste) Le paquet doit avoir une adresse IP destination correspondant à une de celles déclarées dans un des *ip_prefixes* spécifiés.  |Non  |
| |destination_address  |(Liste) Le paquet doit avoir une adresse IP destination correspondant à une de celles spécifiées.  |Non  |
| |destination_port  |(Liste) Le paquet doit avoir un port destination correspondant à un de ceux spécifiés. Il est possible de spécifier un intervalle de ports comme par exemple `10000-20000`  |Non  |
| |protocol  |(Liste) Le paquet doit avoir un des protocoles IP spécifiés : tcp, udp...  |Non  |
| |vlan_id  |(Liste) Le paquet doit provenir d'un des VLAN ID spécifiés  |Non  |
|then  |  |Actions de classification  |Oui  |
| |forwarding_class  |Si à `true`, applique les règles de la classe de service courante. Devrait toujours être à `true`...  |Non  |
| |loss_priority  |Définit la priorité de rejet des paquets entrants en cas de congestion. Valeurs possibles `high` et `low`  |Non  |
| |policer  |Applique le policer (limiteur) spécifié  |Non  |

### policers

Exemple de policer :

```yaml
    policers:
      - name: voip_limit
        if_exceeding:
            bandwidth_limit: 1000000
            burst_size_limit: 15000
        then:
          discard: true
```

| Option (clé) | Sous-clés possibles | Description | Obligatoire |
| --- | --- | --- | --- |
|name  |  |Nom unique (dans l'ensemble de la configuration) du policer  |Oui  |
|if_exceeding  |  |Fixe les seuils limite  |Oui  |
|  |bandwidth_limit  |Limite de bande passante en bits par secondes. Plage de valeur admise 32000..50000000000  |Non  |
|  |burst_size_limit  |Limite de taille de rafale en octets. Plage de valeur admise 1..2147450880  |Non  |
|then  |  |Action à entreprendre lors du dépassement des seuils  |Oui  |
|  |discard  |Rejeter silencieusement les paquets si la valeur est à `true` |Non  |
|  |loss_priority  |Marquer les paquets comme devant être les premier à rejeter en cas de congestion. La seule valeur admise est `high`  |Non  |

## Déploiement

Déploiement sur tous les commutateurs :

```bash
ansible-playbook -i network insa_strasbourg.juniper.ex_config
```

Sur une liste de commutateurs , ici *juniper1*, *juniper2* et *juniper3* :

```bash
ansible-playbook -i network -l juniper1,juniper2,juniper3 insa_strasbourg.juniper.ex_config
```

### Liste des tags

Par défaut (sans tag), le playbook :

1. exécutera un nombre conséquent de vérifications qui en cas d'échec stopperont son exécution
2. générera un fichier de configuration localement
3. enverra cette configuration sur l'équipement
4. validera cette configuration avec un commit confirm devant être confirmé dans les 5 minutes
5. attendra 15 secondes afin de permettre à d'éventuels soucis de connectivité de se manifester
6. confirmera la validation de la nouvelle configuration avec un *commit*
7. enregistrera la nouvelle configuration comme configuration de secours : *request system configuration rescue save*

Avec le tag `offline`, le playbook :

1. générera un fichier de configuration localement

Avec le tag `check`, le playbook :

1. générera un fichier de configuration localement
2. enverra cette configuration sur l'équipement
3. validera cette configuration avec un commit check qui permettra de savoir si la nouvelle configuration est inchangée, différente ou invalide

Avec le tag `quick`, le playbook :

1. générera un fichier de configuration localement
2. enverra cette configuration sur l'équipement
3. validera cette configuration avec un commit confirm devant être confirmé dans les 5 minutes
4. attendra 15 secondes afin de permettre à d'éventuels soucis de connectivité de se manifester
5. confirmera la validation de la nouvelle configuration avec un *commit*
6. enregistrera la nouvelle configuration comme configuration de secours : *request system configuration rescue save*

## Références

- [Ansible for Junos OS](https://www.juniper.net/documentation/product/us/en/ansible-for-junos-os)
- [Ansible for Junos OS Developer Guide](https://www.juniper.net/documentation/us/en/software/junos-ansible/ansible/topics/concept/junos-ansible-overview.html )
