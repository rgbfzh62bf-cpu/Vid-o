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
  basse sur noir pur (contour lissé, restes de mur supprimés) + netteté (unsharp + CAS).
  Les plans plein écran (ex. la fin) sont détectés automatiquement et détourés par IA
  (RobustVideoMatting, `/home/user/models/rvm.onnx`, à télécharger depuis
  github.com/PeterL1n/RobustVideoMatting/releases v1.0.0 `rvm_mobilenetv3_fp32.onnx`),
  en gardant sous-titres et graphismes par-dessus. Sortie ~17 Mbit/s pour rester < 100 Mo.

## Rangement
- Les vidéos terminées vont dans le dossier `vidéos finales/` du dépôt.
- Dossier Drive de destination « VIDÉOS FINALES » (id `1K-LeQe14q5eoioX9NVCneYNbeWSxmW2g`) :
  https://drive.google.com/drive/folders/1K-LeQe14q5eoioX9NVCneYNbeWSxmW2g
  Limites constatées : le connecteur Google Drive refuse les fichiers > 10 Mo, et le
  dossier a renvoyé `canAddChildren: false` pour le compte connecté.

## Préférences
- Livraison : envoyer chaque vidéo finie dans la conversation (SendUserFile) ; l'utilisateur
  la télécharge et la met lui-même dans le Drive « VIDÉOS FINALES ». Ne pas l'envoyer sur Drive.
- Réponses en français.
- Format vertical 9:16 (réels/TikTok).
