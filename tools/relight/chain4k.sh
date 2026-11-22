set -e
cd /home/user/Vid-o
for i in 1 2 3 4 5 6 7 8 9 10; do SEG=seg4k OUT=out4k /home/user/iclenv/bin/python tools/relight/grade.py $i soft & [ $((i%2)) = 0 ] && wait; done; wait
for i in 1 2 3 4 5 6 7 8 9 10; do cp work/out4k/o$i.mp4 video-lumiere/assets/o$i.mp4; done
cd video-lumiere
node /home/user/Vid-o/.claude/skills/hyperframes/scripts/plugin-cli.mjs render --resolution portrait-4k --quality delivery -o renders/master-4k.mp4 > /home/user/render4k.log 2>&1
ffmpeg -v error -y -i renders/master-4k.mp4 -c:v libx264 -profile:v high -level 5.1 -preset slow -b:v 40M -maxrate 45M -bufsize 80M -pix_fmt yuv420p -r 30 -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 48000 -movflags +faststart renders/reel-calories-cachees-4k.mp4
echo CHAIN_DONE
