---
title: Creazione sito con gh-pages
date: 2025-01-26
tags:
  - coding
  - hugo
  - tutorial
---
# Creazione di un sito basato su Hugo con Github Pages tramite Github Actions
Questo post fornisce una guida passo passo su come creare questo sito basato su Hugo, configurando le Github Actions. (NB: Questo sopprattutto per me al fine di ricordarmi come e cosa ho fatto :) ).
## Creazione sito
Andare nella directory scelta (nel mio caso `sites/`) ed eseguire il seguente comando:
```
hugo new site nome_sito -f yml
```
Ecco come ho fatto:
```
~$ cd Documents/sites/
~/Documents/sites$ hugo new site prova -f yml
Congratulations! Your new Hugo site was created in ~Documents/sites/prova.

Just a few more steps...

1. Change the current directory to ~Documents/sites/prova.
2. Create or install a theme:
   - Create a new theme with the command "hugo new theme <THEMENAME>"
   - Or, install a theme from https://themes.gohugo.io/
3. Edit hugo.toml, setting the "theme" property to the theme name.
4. Create new content with the command "hugo new content <SECTIONNAME>/<FILENAME>.<FORMAT>".
5. Start the embedded web server with the command "hugo server --buildDrafts".

See documentation at https://gohugo.io/.
```
Di seguito la struttura che verrà creata:
```
~/Documents/sites/prova$ tree
.
├── archetypes
│   └── default.md
├── assets
├── content
├── data
├── hugo.toml
├── i18n
├── layouts
├── static
└── themes

9 directories, 2 files
```
## Cambiare file di configurazione
Per questo sito serve il file `config.yml` quindi cambiare il nome e modificare l'attuale file `hugo.toml`. 
Ecco il contenuto dell'attuale file `hugo.toml`:
```
baseURL = 'https://example.org/'
languageCode = 'en-us'
title = 'My New Hugo Site'
```
Cambiare nome e estensione del file:
```
~/Documents/sites/prova$ mv hugo.toml config.yml
```
Modificare il contenuto del file in:
```
baseURL:
languageCode: en-us
title: titoloDelSito
```
Lasciamo il `baseurl` vuoto per ora.
## Creare il file .md
Il sito è basato su un file.md, per crearlo eseguire:
```
hugo new docs/prova.md
```
Ecco lo svolgimento:
```
~/Documents/sites/prova$ hugo new docs/prova.md
Content "~/Documents/sites/prova/content/docs/prova.md" created
~/Documents/sites/prova$ tree content/
content/
└── docs
    └── prova.md
    
2 directories, 1 file
```
Ci sono 2 opzioni:
1 -Modificare il file normalmente
2 - Sincronizzarlo con un file.md presente sul computer con il con il comando:
```
rsync -av --delete "percorso/del/file/da/copiare" "/percorso/prova/content/docs/"
```
## Installare e applicare il tema
Copiare e incollare questi comandi:
```
git init
git clone https://github.com/adityatelange/hugo-PaperMod themes/PaperMod --depth=1
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```
Ecco lo svolgimento e la verifica dell'installazione del tema:
```
~/Documents/sites/prova$ git init
hint: Using 'master' as the name for the initial branch. This default branch name
hint: is subject to change. To configure the initial branch name to use in all
hint: of your new repositories, which will suppress this warning, call:
hint: 
hint: 	git config --global init.defaultBranch <name>
hint: 
hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
hint: 'development'. The just-created branch can be renamed via this command:
hint: 
hint: 	git branch -m <name>
Initialized empty Git repository in ~Documents/sites/prova/.git/
~/Documents/sites/prova$ git clone https://github.com/adityatelange/hugo-PaperMod themes/PaperMod --depth=1
Cloning into 'themes/PaperMod'...
remote: Enumerating objects: 139, done.
remote: Counting objects: 100% (139/139), done.
remote: Compressing objects: 100% (98/98), done.
remote: Total 139 (delta 36), reused 120 (delta 36), pack-reused 0 (from 0)
Receiving objects: 100% (139/139), 249.17 KiB | 2.49 MiB/s, done.
Resolving deltas: 100% (36/36), done.
~/Documents/sites/prova$ git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
Adding existing repo at 'themes/PaperMod' to the index
~/Documents/sites/prova$ ls themes/
PaperMod
```
Modificare il file `config.yml`:
`config.yml` modificato:
```
baseURL:
languageCode: en-us
title: titoloDelSito
theme: PaperMod
```
## Github
Creare un repository di github e eseguire questi comandi nel terminale nella cartella principale del progetto (`prova/`):
```
echo "# README" >> README.md
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin <path_to_your_git_repo>
git push -u origin main
```
Aggiungere manualmente il branch `gh-pages`.
Andare nelle impostazioni e abilitare "Read and write permission".
### deploy.yml
Creare le cartelle `.github/workflows/` e il file `deploy.yml` all'interno di esse.
Contenuto:
```
name: Publish to GH Pages
on:
  push:
    branches:
      - main
  pull_request:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout source
        uses: actions/checkout@v3
        with:
          submodules: true

      - name: Checkout destination
        uses: actions/checkout@v3
        if: github.ref == 'refs/heads/main'
        with:
          ref: gh-pages
          path: built-site

      - name: Setup Hugo
        run: |
          curl -L -o /tmp/hugo.tar.gz 'https://github.com/gohugoio/hugo/releases/download/v0.142.0/hugo_extended_0.142.0_linux-amd64.tar.gz'
          tar -C ${RUNNER_TEMP} -zxvf /tmp/hugo.tar.gz hugo

      - name: Check Hugo version
        run: ${RUNNER_TEMP}/hugo version

      - name: Build
        run: ${RUNNER_TEMP}/hugo

      - name: Deploy
        if: github.ref == 'refs/heads/main'
        run: |
          cp -R public/* ${GITHUB_WORKSPACE}/built-site/
          cd ${GITHUB_WORKSPACE}/built-site
          git add .
          git config user.name 'username'
          git config user.email 'mail@gmail.com'
          git commit -m 'Updated site'
          git push
```
