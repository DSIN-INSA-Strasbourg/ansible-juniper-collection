# Ansible - rôle insa_strasbourg.juniper.ex_firmware

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/DSIN-INSA-Strasbourg/ansible-juniper-collection/blob/main/collections/ansible_collections/insa_strasbourg/juniper/docs/ex_firmware.md)
[![fr](https://img.shields.io/badge/lang-fr-blue.svg)](https://github.com/DSIN-INSA-Strasbourg/ansible-juniper-collection/blob/main/collections/ansible_collections/insa_strasbourg/juniper/docs/ex_firmware.fr.md)

---

## Introduction

Ce rôle sert à assurer la mise à jour des firmwares des commutateurs Juniper, ainsi que de leurs images de secours (system snapshot).
Pour la masse des commutateurs, ils seront mis à jour uniquement si nécessaire et redémarrés selon le paramétrage de la variable `ex_firmware_reboot_at`.
Il y a 2 cas particuliers, qui par défaut ne sont pas mis à jour par ce rôle :

- Les châssis virtuels, qui ne seront mis à jour que si le playbook est lancé avec le tag `install_on_virtual_chassis_only`, et dont le déroulement de la mise à jour dépend de la valeur de la variable `ex_firmware_use_nssu_on_vc`
- Les commutateurs déclarés comme critiques, qui ne seront mis à jour que si le playbook est lancé avec le tag `install_on_critical`

## Groupes d'inventaire utilisés par le rôle

Chaque famille de modèle doit être rattachée à un groupe qui lui est propre. Les groupes pour les modèles qualifiés sont les suivants :

- juniper_ex2200
- juniper_ex2300 *(pas spécialement testée, mais devrait fonctionner)*
- juniper_ex3300
- juniper_ex3400
- juniper_ex4100
- juniper_ex4300
- juniper_ex4600
- juniper_ex4650 *(en cours d'intégration)*

Les équipements critiques, dont la mise à jour du firmware requiert une confirmation **doivent** être rattachés au groupe `juniper_critical_devices`, par exemple ainsi :

```yaml
juniper_critical_devices:
  children:
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

## Logique de fonctionnement

Sans tag particulier, le playbook va effectuer les tâches suivantes :

1. Installation du firmware (si nécessaire) : si le firmware a été mis à jour, un redémarrage selon le paramétrage de la variable `ex_firmware_reboot_at` est planifié et le playbook s'arrête
2. Création du snapshot (si nécessaire)

Cela signifie qu'en cas de mise à jour du firmware, il faudra relancer le playbook après le redémarrage pour mettre à jour le snapshot.

## Construction de l'URL du firmware

L'URL de téléchargement d'un firmware est construite avec 3 variables, dont les 2 dernières sont à définir par modèle : `{{ ex_firmware_baseurl }}/{{ ex_firmware_dir }}/{{ ex_firmware }}`. Par exemple :

| Variable | Valeur | URL résultante |
| --- | --- | --- |
|ex_firmware_baseurl  |[https://www.example.com/PLEASE/SET/ME](https://www.example.com/PLEASE/SET/ME)  |  |
|ex_firmware_dir  |EX4600  |[https://www.example.com/PLEASE/SET/ME/EX4600/jinstall-host-ex-4600-18.1R3-S11.3-signed.tgz](https://www.example.com/PLEASE/SET/ME/EX4600/jinstall-host-ex-4600-18.1R3-S11.3-signed.tgz)  |
|ex_firmware  |jinstall-host-ex-4600-18.1R3-S11.3-signed.tgz  |  |

## Fichiers principaux

Les chemins sont relatifs au dossier Ansible

| Fichier | Rôle de ce fichier |
| --- | --- |
|`network` |Fichier d'inventaire des équipements réseau, et attribution des modèles et du statut critique ou non |
|`host_vars/*nom_switch*.yml` |Configuration d'un commutateur |
|`group_vars/juniper_ex*XXXX*.yml` |Configuration spécifique à la famille du modèle : version de firmware et spécificités éventuelles  |

## Configuration globale

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_firmware_baseurl  |[https://www.example.com/PLEASE/SET/ME](https://www.example.com/PLEASE/SET/ME)  |Le préfixe de l'URL de téléchargement des firmware, ie. [https://www.example.com/PLEASE/SET/ME](https://www.example.com/PLEASE/SET/ME)  |Oui  |
|ex_firmware_reboot_at  |"{{ '%y%m%d0100' \| strftime(ansible_date_time.epoch \| int + 86400) }}" (*le jour suivant à 01:00*)  |Indique quand redémarrer le commutateur suite à une mise à jour. Les valeurs possibles sont : <br/> - "now" : redémarre immédiatement <br/> - "+minutes" : redémarre après le nombre de minutes spécifié <br/> - "yymmddhhmm" : redémarre à la date et l'heure spécifiées |Non  |
|ex_firmware_use_nssu_on_vc  |false  |Indique si le firmware d'un chassis virtuel doit être installé en *NSSU*, auquel cas le châssis virtuel ne sera pas redémarré selon `ex_firmware_reboot_at`, puisque ses membres auront été redémarrés individuellement l'un après l'autre. **Le déploiement par NSSU étant plus une source de problèmes que de bienfaits, son usage est déconseillé bien que possible**. Si cette variable est à `false`, le firmware du chassis virtuel sera déployé sur tous les membres, qui redémarreront selon la consigne de `ex_firmware_reboot_at`  |Non  |

## Configuration d'un modèle de commutateur

| Option | Valeur par défaut | Description | Obligatoire |
| --- | --- | --- | --- |
|ex_firmware_dir  |*N/A*  |Sous-dossier contenant les firmwares de ce modèle sur le serveur distant, ie. `EX4600`  |Oui  |
|ex_firmware  |*N/A*  |Firmware à déployer pour ce modèle, le numéro de version sera déduit du nom, il convient donc de préserver les noms d'origine, ie. `junos-arm-32-18.2R3-S6.5.tgz`  |Oui  |
|ex_firmware_validate  |true  |Par défaut on demande au commutateur de valider la compatibilité de sa configuration avec le nouveau firmware. Cependant, les modèles récents (ELS) le font par défaut, et ne reconnaissent plus l'option `validate`. Pour ceux-là, il faut passer cette variable à `false`  |Non  |
|ex_firmware_snapshot_cmd  |*N/A*  |La commande permettant de générer une nouvelle image de secours (system snapshot). Spécifier une chaine vide `""` pour les commutateurs ne disposant pas de cette fonctionnalité, comme les EX4600  |Oui  |
|ex_firmware_snapshot_version_format  |text  |Laisser la valeur par défaut sur les anciens modèles (ceux dont le snapshot est fait avec un `request system snapshot media internal slice alternate`), et utiliser `json` pour les modèles plus récents, utilisant la commande `request system snapshot recovery`   |Non  |

## Configuration d'un commutateur

Le commutateur doit être associé à un groupe de modèle (ie. `juniper_ex4600`) correctement configuré.

## Déploiement

### Sur équipement seul (hors châssis virtuel)

Déploiement sur tous les commutateurs non critiques, et ne faisant pas partie d'un châssis virtuel (stack) :

```bash
ansible-playbook -i network insa_strasbourg.juniper.ex_firmware
```

Déploiement sur une liste de commutateurs , ici *juniper1*, *juniper2* et *juniper3*. Si certains sont déclarés critiques ou font partie d'un châssis virtuels, ils seront ignorés (mis en erreur) :

```bash
ansible-playbook -i network -l juniper1,juniper2,juniper3 insa_strasbourg.juniper.ex_firmware
```

Vérification de la nécessité de mettre à jour le firmware ou le snapshot (sans le faire) :

```bash
ansible-playbook -i network insa_strasbourg.juniper.ex_firmware --tags check
```

Commande de déploiement sur tous les commutateurs, y compris les critiques, et ne faisant pas partie d'un châssis virtuel (stack) :

```bash
ansible-playbook -i network insa_strasbourg.juniper.ex_firmware --tags install_on_critical
```

### Sur chassis virtuel

> [!WARNING]
> Les tests réalisés sur les *Nonstop software upgrade (NSSU)* de châssis virtuels - lorsque `ex_firmware_use_nssu_on_vc` vaut `true` - ont donné des résultats relativement décevants.
> Même lors d'un déroulement sans erreur, la playbook échouera car il perdra sa connexion au [*routing engine RE* principal lorsque celui-ci passera en secondaire pour être mis à jour](https://github.com/Juniper/ansible-junos-stdlib/issues/431).
> **La fonctionnalité est conservée pour le principe, mais son usage est déconseillé.**

Commande de déploiement sur tous les commutateurs non critiques faisant partie d'un châssis virtuel (stack) :

```bash
ansible-playbook -i network insa_strasbourg.juniper.ex_firmware --tags install_on_virtual_chassis_only
```

Commande de déploiement sur tous les commutateurs, y compris les critiques, faisant partie d'un châssis virtuel (stack) :

```bash
ansible-playbook -i network insa_strasbourg.juniper.ex_firmware --tags install_on_critical,install_on_virtual_chassis_only
```
