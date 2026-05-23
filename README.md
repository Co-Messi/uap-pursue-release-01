<p align="center">
  <img src="cover.png" alt="THE U.S. GOVERNMENT HAS CONFIRMED THEY ARE HERE." width="480"/>
</p>

<h1 align="center">PURSUE — Complete Archive (Release 01 + 02)</h1>

<p align="center">
  <b>Both official UAP declassification releases by the U.S. Department of War.</b><br/>
  Sourced verbatim from <a href="https://www.war.gov/UFO/">war.gov/UFO</a><br/>
  UAP = Unidentified Anomalous Phenomena &nbsp;·&nbsp; PURSUE = Presidential Unsealing and Reporting System for UAP Encounters
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Releases-2-red?style=flat-square"/>
  <img src="https://img.shields.io/badge/Documents-132-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/Videos-85-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/Source-war.gov%2FUFO-black?style=flat-square"/>
  <img src="https://img.shields.io/badge/Status-Declassified-brightgreen?style=flat-square"/>
</p>

---

## What is PURSUE?

**PURSUE** stands for **Presidential Unsealing and Reporting System for UAP Encounters** — the formal interagency declassification program created after President Trump issued a directive on **February 19, 2026** instructing the Department of War, FBI, NASA, and intelligence agencies to identify, review, and release UAP records.

**UAP** stands for **Unidentified Anomalous Phenomena** — redefined from "Aerial" to "Anomalous" by the James M. Inhofe National Defense Authorization Act (FY2023, signed December 23, 2022), expanding scope beyond air to include maritime, undersea, space-based, and transmedium observations.

---

## Download Everything

> **All files — PDFs, photographs, and videos — are on Google Drive, publicly accessible, no sign-in required.**

### [⬇️ Download Full Archive on Google Drive](https://drive.google.com/drive/folders/1j-cW20aJ1tGMDag6cTldIKtXMMFdpRKo?usp=sharing)

---

## Release 01 — May 8, 2026

The first large-scale official declassification of UAP materials in U.S. history. Documents span from the late 1940s to 2025.

<p>
  <img src="https://img.shields.io/badge/PDFs-126-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/Photos-14-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/Videos-28-blue?style=flat-square"/>
</p>

| Folder | Contents | Size |
|---|---|---|
| `pdfs/` | 126 declassified PDF documents | ~2.3 GB |
| `images/` | 14 photographs (FBI, NASA, DoD) | ~15 MB |
| `videos/` | 28 original videos from DVIDS | ~1.2 GB |
| `videos-with-music/` | 28 videos with cinematic instrumental soundtrack | ~1.3 GB |

The release covers incidents spanning multiple decades and commands:

- **DOW-UAP-D series** — Mission Reports documenting UAP encounters
- **DOW-UAP-PR series** — Unresolved UAP Incident Reports (Middle East, Iraq, Syria, INDOPACOM, Africa)
- **FBI files** — Historical UAP investigation documents and photographs
- **NASA files** — Apollo 12 & 17 photographs, Gemini 7 audio excerpt (1965)
- **DIA / NSA / NRO** — Intelligence agency UAP assessments
- **Video footage** — Raw military UAP encounter video from DVIDS

Two files (`Serial_153` and one other) return 404 on war.gov itself — they are not missing from this archive, they simply do not exist at the source.

---

## Release 02 — May 22, 2026

The second tranche under PURSUE. Includes intelligence agency records spanning the CIA, DOE, DOW, and ODNI — plus 57 DoD videos.

<p>
  <img src="https://img.shields.io/badge/PDFs-6-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/Videos-57-blue?style=flat-square"/>
</p>

| Folder | Contents | Size |
|---|---|---|
| `documents/` | 6 declassified PDFs | ~70 MB |
| `videos/` | 57 DoD UAP videos | ~5.4 GB |

Documents in this release:

| File | Agency | Description |
|---|---|---|
| `CIA-UAP-D001` | CIA | Intelligence Information Report — USSR, 1973 |
| `DOE-UAP-D001` | DOE | PANTEX Image |
| `DOE-UAP-D002` | DOE | James Tuck Correspondence |
| `DOE-UAP-D003` | DOE | Pajarito Astronomers |
| `DOW-UAP-D017` | DOW | General Correspondence of Sandia |
| `ODNI-UAP-D001` | ODNI | USPER Narrative — Senior USIC |

---

## Download Yourself

### Release 01

```bash
pip install curl_cffi
python download_uap.py
```

Uses Chrome TLS impersonation to bypass Akamai CDN bot detection.

### Release 02

```bash
pip install curl_cffi
python download_release02.py
```

Downloads the document bundle via chunked range requests (Akamai blocks full-file streaming) and streams the video archive directly from CloudFront.

### Add Cinematic Music to Release 01 Videos

```bash
python add_music.py
```

Pulls dark/thriller instrumental tracks from Pixabay (royalty-free, no lyrics) and mixes one unique track per video using ffmpeg.

**Requirements:** `pip install curl_cffi` · `ffmpeg` · `yt-dlp`

---

## Source

All files sourced from the official U.S. Department of War UAP portal:
**[https://www.war.gov/UFO/](https://www.war.gov/UFO/)**

This archive is for research, journalism, and public record purposes.
