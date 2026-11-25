# Computational Linguistics BA at Tübingen: early leavers and graduates

**Live page: https://wooweeiao.github.io/cl-ba-graduation/** (中文 / English)

An interactive page that follows each entry cohort of the Computational Linguistics bachelor's major (Bachelor Hauptfach) at the University of Tübingen, semester by semester: how many students leave after each of the first five semesters, and how many graduate from semester 6 onwards.

图宾根大学计算语言学本科主修各入学届的逐学期去向：前 5 个学期各有多少人中途离开，第 6 学期起各有多少人毕业。

## What the numbers are

- **Source**: the [Studierendenstatistik](https://uni-tuebingen.de/en/einrichtungen/verwaltung/iv-studierende/studierendenabteilung/statistiken/) published each semester by Universität Tübingen, table "Studienfachbelegung nach Abschlusszielen", winter 2016/17 – winter 2026/27 (21 semesters). The original PDFs are not included in this repository.
- **Programme**: subject codes 160, 161 and 162 are versions of the same programme under different exam regulations; their Bachelor Hauptfach counts are added together. Minor and master's students are not included.
- **Rule**: the statistics give head counts per Fachsemester, with no individual records. A cohort's count in semester k minus its count in semester k+1 one semester later is the number who left after semester k. Leaving after semesters 1–5 is counted as leaving early; leaving after semester 6 or later is counted as graduating.
- **These are estimates, not official graduation data.** Few students in this programme graduate within the first 5 semesters and few leave without a degree from semester 6 onwards; the two errors point in opposite directions and may roughly cancel out.
- The figures describe students as a whole. They are not a judgement on the quality of the programme and cannot predict what will happen to any one person.

The full method and its limitations are described at the bottom of the page.

## Files

| Path | Contents |
|---|---|
| `docs/index.html` | The published page (single file, no external dependencies) |
| `site/index.html` | Page source, without the HTML document wrapper |
| `data/stock_long.csv` | Head counts per semester, degree and Fachsemester for the three subject codes |
| `data/cohort_long.csv` | One row per entry cohort × Fachsemester: head counts, number leaving, share of entrants, share of students enrolled |
| `data/lifetable.csv` | Pooled figures across cohorts, for both cohort definitions |
| `data/cl_ba.json` | The above bundled as JSON |
| `data/parsed_rows.json` | Rows as parsed from the PDFs (each checked against the row and column totals in the source) |
| `build/parse.py` | Extracts the tables from `pdftotext -layout` output of the PDFs |
| `build/analyze.py` | Builds the cohort tables and pooled figures |
| `build/make_pages.py` | Wraps `site/index.html` into `docs/index.html` |

## Rebuilding

```sh
# 1. convert each statistics PDF to text
pdftotext -layout statistik-ws-20262027.pdf txt/statistik-ws-20262027.txt
# 2. extract the Computerlinguistik tables, then compute cohorts
python3 build/parse.py txt data/parsed_rows.json
python3 build/analyze.py data/parsed_rows.json data
# 3. rebuild the published page
python3 build/make_pages.py site/index.html docs/index.html
```

Corrections are welcome: please open an issue.
