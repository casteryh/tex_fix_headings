# TeX Heading Math Formula Fixer

This Python script fixes hyperref errors when section/subsection headings contain math formulas by wrapping them in `\texorpdfstring{math}{unicode}` commands.

## Problem

When using the `hyperref` package in LaTeX, math formulas in section headings can cause errors because hyperref tries to create PDF bookmarks from the section titles, but PDF bookmarks cannot contain LaTeX math commands.

## Solution

This script automatically finds math formulas (content between `$...$`) in `\section` and `\subsection` headings and wraps them with `\texorpdfstring{$formula$}{unicode_representation}`, where:
- The first argument contains the original math formula for the PDF content
- The second argument contains a unicode/text representation for the PDF bookmark

## Usage

```bash
# Process a file and overwrite it
python3 tex_fix_heading.py input.tex

# Process a file and save to a different output file
python3 tex_fix_heading.py input.tex -o output.tex

# Use a custom mappings file
python3 tex_fix_heading.py input.tex -m custom_mappings.json
```

## Features

- **Automatic Detection**: Finds `\section` and `\subsection` lines with math formulas
- **Smart Replacement**: Only processes formulas not already inside `\texorpdfstring`
- **Default Mappings**: Includes sensible defaults for common math symbols and formulas
- **Interactive Mode**: Prompts for unknown formulas and saves custom mappings
- **Persistent Storage**: Saves custom mappings to JSON file for future use

## Default Mappings

The script includes comprehensive default mappings for:
- Greek letters: `\alpha` → α, `\beta` → β, `\gamma` → γ, etc.
- Mathematical operators: `\times` → ×, `\cdot` → ·, `\pm` → ±, `\leq` → ≤, `\geq` → ≥, etc.
- Set theory: `\in` → ∈, `\subset` → ⊂, `\cup` → ∪, `\cap` → ∩, `\emptyset` → ∅, etc.
- Arrows: `\rightarrow` → →, `\leftarrow` → ←, `\Rightarrow` → ⇒, `\Leftrightarrow` → ⇔, etc.
- Common formulas: `x^2` → x², `\frac{a}{b}` → a/b, `\sqrt{x}` → √x, `e^x` → eˣ, etc.
- Large operators: `\sum` → ∑, `\prod` → ∏, `\int` → ∫, etc.
- Functions: `\sin x` → sin x, `\cos x` → cos x, `\log x` → log x, etc.

## Example

**Before:**
```latex
\section{Introduction to $\alpha$ particles}
\subsection{The $x^2$ function}
```

**After:**
```latex
\section{Introduction to \texorpdfstring{$\alpha$}{α} particles}
\subsection{The \texorpdfstring{$x^2$}{x²} function}
```

## Custom Mappings

The script saves custom mappings to `math_mappings.json` (or a file specified with `-m`). You can also manually edit this file to add your own mappings:

```json
{
  "\\alpha": "α",
  "x^2": "x²",
  "\\frac{a}{b}": "a/b",
  "custom_formula": "Custom Text"
}
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Notes

- The script treats each `$...$` as a complete formula unit
- It preserves existing `\texorpdfstring` commands
- Unknown formulas trigger interactive prompts for mapping input
- All custom mappings are automatically saved for future use
