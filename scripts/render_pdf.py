#!/usr/bin/env python3
"""Render one or more Quarto notebooks and merge them into one PDF report."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_DIR = REPO_ROOT / "analysis"
RENDER_DIR = ANALYSIS_DIR / "render"
RENDERED_REL_DIR = Path("render") / "pdf"
RENDERED_DIR = RENDER_DIR / "pdf"
PDF_PARTS_DIR = RENDER_DIR / "pdf_parts"
LOG_DIR = RENDER_DIR / "logs"
PDF_PREAMBLE = RENDER_DIR / "pdf_preamble.tex"
DEFAULT_OUTPUT = RENDERED_DIR / "analysis_notebooks_combined.pdf"


def _format_duration(seconds: float) -> str:
    seconds = max(0, int(round(seconds)))
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes:02d}m {seconds:02d}s"
    if minutes:
        return f"{minutes}m {seconds:02d}s"
    return f"{seconds}s"


def _progress_line(completed: int, total: int, started_at: float, label: str) -> str:
    percent = (completed / total * 100) if total else 100.0
    elapsed = time.monotonic() - started_at
    if completed:
        eta = elapsed / completed * (total - completed)
        eta_text = _format_duration(eta)
    else:
        eta_text = "estimating"
    return (
        f"[{completed}/{total} | {percent:5.1f}%] {label} "
        f"| elapsed {_format_duration(elapsed)} | ETA {eta_text}"
    )


def _find_notebooks() -> list[Path]:
    notebooks = sorted(ANALYSIS_DIR.glob("*.qmd"))
    if not notebooks:
        raise SystemExit("No .qmd notebooks found in analysis/.")
    return notebooks


def _parse_selection(selection: str, notebooks: list[Path]) -> list[Path]:
    selection = selection.strip()
    if not selection:
        raise ValueError("Empty selection")

    if selection.lower() in {"all", "todo", "todos", "*"}:
        return notebooks

    chosen: list[Path] = []
    seen: set[Path] = set()

    for part in selection.replace(" ", "").split(","):
        if not part:
            continue

        if "-" in part and all(piece.isdigit() for piece in part.split("-", 1)):
            start, end = [int(piece) for piece in part.split("-", 1)]
            if start > end:
                start, end = end, start
            for idx in range(start, end + 1):
                if not 1 <= idx <= len(notebooks):
                    raise ValueError(f"Selection number out of range: {idx}")
                path = notebooks[idx - 1]
                if path not in seen:
                    chosen.append(path)
                    seen.add(path)
            continue

        if part.isdigit():
            idx = int(part)
            if not 1 <= idx <= len(notebooks):
                raise ValueError(f"Selection number out of range: {idx}")
            path = notebooks[idx - 1]
        else:
            path = Path(part)
            if not path.is_absolute():
                path = REPO_ROOT / path
            path = path.resolve()
            if not path.exists() or path.suffix != ".qmd":
                raise ValueError(f"Could not find a .qmd notebook at: {part}")

        if path not in seen:
            chosen.append(path)
            seen.add(path)

    if not chosen:
        raise ValueError("No notebooks selected")
    return chosen


def _choose_notebooks(notebooks: list[Path]) -> list[Path]:
    print("Available notebooks:\n")
    for i, path in enumerate(notebooks, start=1):
        print(f"  {i}. {path.relative_to(REPO_ROOT)}")
    print("\nExamples: 2 | 1,3,4 | 1-3 | all | analysis/02_tables.qmd")

    while True:
        choice = input("\nWhich notebook(s) should be merged into one PDF?: ").strip()
        try:
            return _parse_selection(choice, notebooks)
        except ValueError as exc:
            print(exc)


def _pdf_render_cmd(notebook_name: str, output_dir_name: str) -> list[str]:
    cmd = [
        "quarto",
        "render",
        notebook_name,
        "--to",
        "pdf",
        "--output-dir",
        output_dir_name,
        "-M",
        "toc=true",
        "-M",
        "toc-depth=3",
        "-M",
        "number-sections=true",
        "-M",
        "papersize=a4",
        "-M",
        "fontsize=9pt",
        "-M",
        "code-block-font-size=\\scriptsize",
        "-M",
        "code-overflow=wrap",
        "-M",
        "fig-width=6.5",
        "-M",
        "fig-height=4.2",
    ]
    if PDF_PREAMBLE.exists():
        cmd.extend(["-M", f"include-in-header={PDF_PREAMBLE}"])
    return cmd


def render_pdf(notebook: Path, *, quiet: bool = True) -> Path | None:
    notebook = notebook.resolve()
    if not notebook.exists():
        raise FileNotFoundError(notebook)

    cmd = _pdf_render_cmd(notebook.name, str(RENDERED_REL_DIR))
    print("\nRunning:")
    print(f"  cd {notebook.parent}")
    print(f"  {' '.join(cmd)}")

    RENDERED_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"{notebook.stem}.log"

    if quiet:
        with log_path.open("w", encoding="utf-8") as log:
            proc = subprocess.run(
                cmd,
                cwd=notebook.parent,
                stdout=log,
                stderr=subprocess.STDOUT,
                text=True,
            )
    else:
        proc = subprocess.run(cmd, cwd=notebook.parent)

    if proc.returncode != 0:
        print(f"  ERROR: failed to render {notebook.name}. Log: {log_path.relative_to(REPO_ROOT)}")
        return None

    pdf_path = notebook.parent / RENDERED_REL_DIR / f"{notebook.stem}.pdf"
    if not pdf_path.exists():
        print(f"  ERROR: Quarto did not create the expected PDF: {pdf_path.relative_to(REPO_ROOT)}")
        return None

    PDF_PARTS_DIR.mkdir(parents=True, exist_ok=True)
    stable_pdf = PDF_PARTS_DIR / f"{notebook.stem}.pdf"
    shutil.copy2(pdf_path, stable_pdf)
    print(f"  OK: {stable_pdf.relative_to(REPO_ROOT)}")
    return stable_pdf


def render_master_toc(selected: list[Path], report_title: str, *, quiet: bool = True) -> Path | None:
    with tempfile.TemporaryDirectory(prefix="qmd_report_toc_") as tmp:
        tmp_dir = Path(tmp)
        toc_qmd = tmp_dir / "00_master_toc.qmd"
        lines = [
            "---",
            f"title: \"{report_title}\"",
            "format:",
            "  pdf:",
            "    toc: true",
            "    toc-depth: 3",
            "    number-sections: false",
            "execute:",
            "  echo: false",
            "---",
            "",
            "\\clearpage",
            "",
            "# Notebook Contents",
            "",
        ]
        for idx, notebook in enumerate(selected, start=1):
            lines.append(f"{idx}. {notebook.stem.replace('_', ' ')}")
        lines.append("")
        toc_qmd.write_text("\n".join(lines), encoding="utf-8")

        output_dir_name = str(RENDERED_REL_DIR)
        cmd = _pdf_render_cmd(toc_qmd.name, output_dir_name)
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_path = LOG_DIR / "00_master_toc.log"

        if quiet:
            with log_path.open("w", encoding="utf-8") as log:
                proc = subprocess.run(
                    cmd,
                    cwd=tmp_dir,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    text=True,
                )
        else:
            proc = subprocess.run(cmd, cwd=tmp_dir)

        if proc.returncode != 0:
            print(f"  ERROR: failed to render the master TOC. Log: {log_path.relative_to(REPO_ROOT)}")
            return None

        rendered = tmp_dir / output_dir_name / f"{toc_qmd.stem}.pdf"
        if not rendered.exists():
            print("  ERROR: Quarto did not create the master TOC PDF.")
            return None

        PDF_PARTS_DIR.mkdir(parents=True, exist_ok=True)
        final_toc = PDF_PARTS_DIR / "00_master_toc.pdf"
        shutil.copy2(rendered, final_toc)
        print(f"  OK master TOC: {final_toc.relative_to(REPO_ROOT)}")
        return final_toc


def merge_pdfs(pdf_paths: list[Path], output_path: Path) -> None:
    if not pdf_paths:
        raise ValueError("No PDFs to merge")

    gs = shutil.which("gs")
    if gs is None:
        raise RuntimeError("Ghostscript 'gs' is required to merge PDFs but was not found.")

    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        gs,
        "-dBATCH",
        "-dNOPAUSE",
        "-q",
        "-sDEVICE=pdfwrite",
        f"-sOutputFile={output_path}",
        *[str(path.resolve()) for path in pdf_paths],
    ]
    print("\nMerging PDFs:")
    print("  " + " ".join(cmd) + "\n")
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)
    print(f"Combined PDF saved to: {output_path.relative_to(REPO_ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render one or more analysis/*.qmd notebooks and merge them into one PDF."
    )
    parser.add_argument(
        "selection",
        nargs="?",
        help="Selection: all, 1, 1,3, 1-3, or a .qmd path. If omitted, prompts interactively.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=str(DEFAULT_OUTPUT),
        help=f"Combined PDF path. Default: {DEFAULT_OUTPUT.relative_to(REPO_ROOT)}",
    )
    parser.add_argument(
        "--title",
        default="Analysis Report",
        help="Title used for the generated master table-of-contents page.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Stop without merging if any selected notebook fails.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show full Quarto output instead of writing per-notebook logs.",
    )
    parser.add_argument(
        "--merge-existing",
        action="store_true",
        help="Do not render; merge existing PDFs for the selected notebooks.",
    )
    parser.add_argument(
        "--no-master-toc",
        action="store_true",
        help="Do not prepend a generated master table-of-contents PDF.",
    )
    args = parser.parse_args()

    notebooks = _find_notebooks()
    selected = _parse_selection(args.selection, notebooks) if args.selection else _choose_notebooks(notebooks)

    action = "Merging existing PDFs" if args.merge_existing else "Rendering and merging"
    print(f"\n{action} in this order:")
    for path in selected:
        print(f"  - {path.relative_to(REPO_ROOT)}")

    pdf_paths: list[Path] = []
    failed: list[Path] = []
    total_notebooks = len(selected)
    started_at = time.monotonic()
    print(_progress_line(0, total_notebooks, started_at, "Starting"))
    for idx, notebook in enumerate(selected, start=1):
        print(
            "\n"
            + _progress_line(
                idx - 1,
                total_notebooks,
                started_at,
                f"Next: {notebook.relative_to(REPO_ROOT)}",
            )
        )
        if args.merge_existing:
            pdf_path = PDF_PARTS_DIR / f"{notebook.stem}.pdf"
            fallback_pdf_path = notebook.parent / RENDERED_REL_DIR / f"{notebook.stem}.pdf"
            if pdf_path.exists():
                print(f"  OK existing: {pdf_path.relative_to(REPO_ROOT)}")
                pdf_paths.append(pdf_path)
            elif fallback_pdf_path.exists():
                print(f"  OK existing: {fallback_pdf_path.relative_to(REPO_ROOT)}")
                pdf_paths.append(fallback_pdf_path)
            else:
                print(f"  ERROR: no existing PDF found for {notebook.relative_to(REPO_ROOT)}")
                failed.append(notebook)
            print(_progress_line(idx, total_notebooks, started_at, "Notebook selection checked"))
            continue

        pdf_path = render_pdf(notebook, quiet=not args.verbose)
        if pdf_path is None:
            failed.append(notebook)
        else:
            pdf_paths.append(pdf_path)
        print(_progress_line(idx, total_notebooks, started_at, "Notebook render finished"))

    if failed:
        print("\nFailed notebooks:")
        for path in failed:
            print(f"  - {path.relative_to(REPO_ROOT)}")
        if args.strict:
            raise SystemExit("Strict mode: no PDF will be merged because at least one notebook failed.")

    if not args.no_master_toc:
        print("\nRendering generated master table of contents...")
        toc_pdf = render_master_toc(selected, args.title, quiet=not args.verbose)
        if toc_pdf is not None:
            pdf_paths.insert(0, toc_pdf)

    if not pdf_paths:
        raise SystemExit("No valid PDFs to merge.")

    print("\nFinal step: merging rendered PDFs.")
    merge_pdfs(pdf_paths, Path(args.output))
    print(_progress_line(total_notebooks, total_notebooks, started_at, "Done"))


if __name__ == "__main__":
    main()
