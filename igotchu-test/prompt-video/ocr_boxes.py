"""Word boxes for each screenshot (Tesseract), used to place highlights exactly on the words being read."""
import csv, json, subprocess
out = {}
for i in ["01", "02", "03", "04", "05"]:
    subprocess.run(["tesseract", f"assets/screens/{i}.png", f"ocr/{i}", "-l", "eng", "tsv"], capture_output=True)
    rows = list(csv.DictReader(open(f"ocr/{i}.tsv"), delimiter="\t", quoting=csv.QUOTE_NONE))
    out[i] = [{"t": r["text"], "x": int(r["left"]), "y": int(r["top"]), "w": int(r["width"]), "h": int(r["height"]),
               "line": f'{r["block_num"]}.{r["par_num"]}.{r["line_num"]}'} for r in rows if r["level"] == "5" and r["text"].strip()]
json.dump(out, open("ocr/words.json", "w"))
print({k: len(v) for k, v in out.items()})
