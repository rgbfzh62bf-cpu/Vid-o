# Vid-o — montage vidéo

## Source des vidéos
Dossier Google Drive de l'utilisateur (à utiliser pour toutes les prochaines vidéos) :
https://drive.google.com/drive/folders/1I8DcpoQFZ1X8O-xlSVBVariQqq_rnVWP

Lister le dossier :
```
python3 -c "import gdown; [print(f.id, f.path) for f in gdown.download_folder('https://drive.google.com/drive/folders/1I8DcpoQFZ1X8O-xlSVBVariQqq_rnVWP', skip_download=True, quiet=True)]"
```
Télécharger un fichier (gdown passe par des serveurs googleusercontent non autorisés ; utiliser plutôt) :
```
curl -sSL -o FICHIER "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"
```
Hôtes réseau déjà autorisés dans l'environnement : drive.google.com, drive.usercontent.google.com,
huggingface.co, us.aws.cdn.hf.co (modèles Whisper ; mettre `HF_HUB_DISABLE_XET=1`).

## Outils
- `pip install gdown faster-whisper opencv-contrib-python-headless`
- ffmpeg est installé (libass disponible pour les sous-titres ASS, police « Inter » installée).

## Scripts (dossier `montage/`)
- `build.py` + `captions.json` : sous-titres animés mot par mot + motion design.
- `build_drole.py` : montage mème (arrêts sur image, zooms, boom).
- `detourage.py` : format « visuels en haut / personne en bas » — re-détoure la moitié
  basse sur noir pur (contour lissé, restes de mur supprimés) + débruitage et netteté.

## Rangement
- Les vidéos terminées vont dans le dossier `vidéos finales/` du dépôt.

## Préférences
- Réponses en français.
- Format vertical 9:16 (réels/TikTok).
