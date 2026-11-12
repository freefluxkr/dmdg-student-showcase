# -*- coding: utf-8 -*-
"""
Transcode oversized (>100 MB) and .mov videos from C:\\Users\\PC\\Downloads\\20261112
into web-optimized 720p H.264 +faststart .mp4 files in ../transcoded_videos/.
Already existing non-empty outputs are skipped (idempotent).
"""
import os
import subprocess
import sys

FFMPEG = r"C:\ffmpeg-2026-05-28-git-7b46c6a2a3-essentials_build\bin\ffmpeg.exe"
SRC_ROOT = r"C:\Users\PC\Downloads\20261112"
OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "transcoded_videos"))
os.makedirs(OUT_DIR, exist_ok=True)

JOBS = [
    # (out_filename, relative_src_path, extra_vf_fps)
    ("lg1_stage1_team1.mp4", r"LG Uplus Why Not 1기\1차 PRJ\1차 서비스 기획 발표자료\1_IPTV 채널 추천_정연진_박종현_신새봄_권정인_이중찬.mp4", None),
    ("lg1_stage1_team2.mp4", r"LG Uplus Why Not 1기\1차 PRJ\1차 서비스 기획 발표자료\2_고객상담이력_이현행_신종현_김다란솔_임기빈_박준현_정인엽.mp4", None),
    ("lg1_stage1_team3.mp4", r"LG Uplus Why Not 1기\1차 PRJ\1차 서비스 기획 발표자료\3_자율주행_한은선_김준희_박장원_김나현_김승엽_김동혁.mp4", None),
    ("lg1_stage1_team4.mp4", r"LG Uplus Why Not 1기\1차 PRJ\1차 서비스 기획 발표자료\4_TV이용행태_전서영_박시원_임세연_이지선_이상민.mp4", None),
    ("lg1_stage1_team5.mp4", r"LG Uplus Why Not 1기\1차 PRJ\1차 서비스 기획 발표자료\5_TV이용행태_곽현철_양현우_조진형_서정임_김승훈.mp4", None),
    # 2차 PRJ 발표 영상 (2024-10-30 실제 발표 순서 확인 완료: 14:59=2팀, 15:18=4팀, 15:47=3팀, 16:05=1팀, 16:16=5팀)
    ("lg1_stage2_team2_talk.mp4", r"LG Uplus Why Not 1기\2차 PRJ\4 발표 영상\20241030_145921.mp4", None),
    ("lg1_stage2_team4_talk.mp4", r"LG Uplus Why Not 1기\2차 PRJ\4 발표 영상\20241030_151857.mp4", None),
    ("lg1_stage2_team3_talk.mp4", r"LG Uplus Why Not 1기\2차 PRJ\4 발표 영상\20241030_154729.mp4", None),
    ("lg1_stage2_team1_talk.mp4", r"LG Uplus Why Not 1기\2차 PRJ\4 발표 영상\20241030_160505.mp4", None),
    ("lg1_stage2_team5_talk.mp4", r"LG Uplus Why Not 1기\2차 PRJ\4 발표 영상\20241030_161630.mp4", None),
    # 시연 동영상 샘플 (.mov -> .mp4)
    ("lg1_stage2_sample_groupware.mp4", r"LG Uplus Why Not 1기\2차 PRJ 시연 동영상 샘플\인트라넷 기반 그룹웨어 개발  시연.mov", None),
    # LG2 3조 D오디 240.65MB 60fps -> 30fps 720p 경량화
    ("lg2_team3_dodi_demo.mp4", r"LG Uplus Why Not 2기\3_자율주행_한은선_김준희_박장원_김나현_김승엽_김동혁 (1)\2차_최종본_2조_자율주행_D오디.mp4", 30),
]


def main():
    if not os.path.exists(FFMPEG):
        print(f"ERROR: ffmpeg not found at {FFMPEG}", file=sys.stderr)
        sys.exit(1)

    for out_name, rel_src, target_fps in JOBS:
        src = os.path.join(SRC_ROOT, rel_src)
        dst = os.path.join(OUT_DIR, out_name)
        tmp = dst + ".part.mp4"
        if not os.path.exists(src):
            print(f"[SKIP-MISSING] {src}")
            continue
        if os.path.exists(dst) and os.path.getsize(dst) > 100_000:
            print(f"[SKIP-EXISTS] {out_name} ({os.path.getsize(dst)/1048576:.1f} MB)")
            continue
        vf = "scale='min(1280,iw)':-2"
        cmd = [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "warning",
            "-i", src,
            "-map", "0:v:0", "-map", "0:a?",
            "-vf", vf,
        ]
        if target_fps:
            cmd += ["-r", str(target_fps)]
        cmd += [
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "28",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "96k", "-ac", "2",
            "-movflags", "+faststart",
            tmp,
        ]
        src_mb = os.path.getsize(src) / 1048576
        print(f"[TRANSCODE] {out_name} <- {os.path.basename(src)} ({src_mb:.1f} MB)...", flush=True)
        res = subprocess.run(cmd)
        if res.returncode != 0 or not os.path.exists(tmp):
            print(f"[ERROR] Failed {out_name} (code={res.returncode})", file=sys.stderr)
            sys.exit(res.returncode or 1)
        os.replace(tmp, dst)
        dst_mb = os.path.getsize(dst) / 1048576
        print(f"[DONE] {out_name}: {src_mb:.1f} MB -> {dst_mb:.1f} MB", flush=True)


if __name__ == "__main__":
    main()

