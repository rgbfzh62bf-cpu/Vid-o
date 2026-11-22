cd /home/user/IC-Light
RM=$(ls -d /root/.cache/huggingface/hub/models--briaai--RMBG-1.4/snapshots/*)
for i in 1 2 3 4 5 6 7 8 9 10; do
  E=PS=45; [ $i = 9 ] && E="PS=45 LOWFLAT=1"
  env $E /home/user/iclenv/bin/python composite2.py $i $RM 2>&1 | grep -E "^ok|Error|Traceback"
  cp /home/user/Vid-o/work/out/o$i.mp4 /home/user/Vid-o/video-lumiere/assets/o$i.mp4
done
cd /home/user/Vid-o/video-lumiere
node /home/user/Vid-o/.claude/skills/hyperframes/scripts/plugin-cli.mjs render -o renders/video-lumiere-v3.mp4 > /home/user/render7.log 2>&1
echo CHAIN_DONE
