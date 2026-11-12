# -*- coding: utf-8 -*-
"""
Extracts compressed cohort archives from C:\\Users\\PC\\Downloads\\20261112\\LG Uplus Why Not 1기
into ../extracted_sources/ with proper CP949 Korean filename decoding,
skipping lockfiles (~$*) and redundant >100MB raw videos already transcoded in ../transcoded_videos/.
"""
import os
import shutil
import zipfile

SRC_LG1 = r"C:\Users\PC\Downloads\20261112\LG Uplus Why Not 1기"
PRJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXT_ROOT = os.path.join(PRJ_ROOT, "extracted_sources")


def decode_zip_name(info: zipfile.ZipInfo) -> str:
    raw = info.filename
    if not (info.flag_bits & 0x800):
        try:
            raw = raw.encode("cp437").decode("cp949")
        except Exception:
            pass
    return raw.replace("\\", "/")


def safe_extract_zip(zip_path: str, out_dir: str, skip_exts=(".mp4", ".mov"), keep_mp4_under_mb=80.0):
    os.makedirs(out_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            rel = decode_zip_name(info).lstrip("/")
            if "__MACOSX" in rel or os.path.basename(rel).startswith("~$") or ".DS_Store" in rel:
                continue
            ext = os.path.splitext(rel)[1].lower()
            if ext in skip_exts and info.file_size > keep_mp4_under_mb * 1048576:
                continue
            dest = os.path.join(out_dir, rel.replace("/", os.sep))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with z.open(info) as src, open(dest, "wb") as dst:
                shutil.copyfileobj(src, dst)
            # Recursively unpack nested zips (like 2차_최종_2조_D오디.zip or DATA로_2차프로젝트_241030.zip)
            if ext == ".zip":
                nested_dir = os.path.join(os.path.dirname(dest), os.path.splitext(os.path.basename(dest))[0])
                safe_extract_zip(dest, nested_dir, skip_exts=skip_exts, keep_mp4_under_mb=keep_mp4_under_mb)
                os.remove(dest)


def extract_all():
    if os.path.exists(EXT_ROOT):
        shutil.rmtree(EXT_ROOT)
    os.makedirs(EXT_ROOT, exist_ok=True)

    count = 0
    for dp, _, fns in os.walk(SRC_LG1):
        for fn in sorted(fns):
            if not fn.lower().endswith(".zip"):
                continue
            # Dataset ZIPs under 1차 데이터files remain downloadable as ZIPs (not extracted into deliverable cards)
            rel_dir = os.path.relpath(dp, SRC_LG1)
            if "datafiles" in rel_dir.lower():
                continue
            zpath = os.path.join(dp, fn)
            sub_target = os.path.join(EXT_ROOT, rel_dir, os.path.splitext(fn)[0])
            safe_extract_zip(zpath, sub_target)
            count += 1
            print(f"[UNZIP] {rel_dir}\\{fn}")
    print(f"Extracted {count} deliverable ZIPs into {EXT_ROOT}")


if __name__ == "__main__":
    extract_all()

