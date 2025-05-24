#!/usr/bin/env python3
"""
TeX Heading Math Formula Fixer

This script fixes hyperref errors when section/subsection headings contain math formulas
by wrapping them in \texorpdfstring{math}{unicode} commands.
"""

import re
import json
import os
from typing import Dict, Optional

class TexHeadingFixer:
    def __init__(self, mapping_file: str = "math_mappings.json", auto_yes: bool = False):
        self.mapping_file = mapping_file
        self.auto_yes = auto_yes
        self.math_mappings = self.load_mappings()
        
    def load_mappings(self) -> Dict[str, str]:
        """Load math formula to unicode mappings from file."""
        default_mappings = {
            # Greek letters (lowercase)
            r'\alpha': 'α',
            r'\beta': 'β',
            r'\gamma': 'γ',
            r'\delta': 'δ',
            r'\epsilon': 'ε',
            r'\varepsilon': 'ε',
            r'\zeta': 'ζ',
            r'\eta': 'η',
            r'\theta': 'θ',
            r'\vartheta': 'ϑ',
            r'\iota': 'ι',
            r'\kappa': 'κ',
            r'\lambda': 'λ',
            r'\mu': 'μ',
            r'\nu': 'ν',
            r'\xi': 'ξ',
            r'\pi': 'π',
            r'\varpi': 'ϖ',
            r'\rho': 'ρ',
            r'\varrho': 'ϱ',
            r'\sigma': 'σ',
            r'\varsigma': 'ς',
            r'\tau': 'τ',
            r'\upsilon': 'υ',
            r'\phi': 'φ',
            r'\varphi': 'φ',
            r'\chi': 'χ',
            r'\psi': 'ψ',
            r'\omega': 'ω',
            
            # Greek letters (uppercase)
            r'\Gamma': 'Γ',
            r'\Delta': 'Δ',
            r'\Theta': 'Θ',
            r'\Lambda': 'Λ',
            r'\Xi': 'Ξ',
            r'\Pi': 'Π',
            r'\Sigma': 'Σ',
            r'\Upsilon': 'Υ',
            r'\Phi': 'Φ',
            r'\Psi': 'Ψ',
            r'\Omega': 'Ω',
            
            # Mathematical operators and symbols
            r'\pm': '±',
            r'\mp': '∓',
            r'\times': '×',
            r'\div': '÷',
            r'\cdot': '·',
            r'\ast': '∗',
            r'\star': '⋆',
            r'\circ': '∘',
            r'\bullet': '•',
            r'\cap': '∩',
            r'\cup': '∪',
            r'\sqcap': '⊓',
            r'\sqcup': '⊔',
            r'\vee': '∨',
            r'\wedge': '∧',
            r'\setminus': '∖',
            r'\wr': '≀',
            r'\diamond': '⋄',
            r'\bigtriangleup': '△',
            r'\bigtriangledown': '▽',
            r'\triangleleft': '◁',
            r'\triangleright': '▷',
            r'\lhd': '⊲',
            r'\rhd': '⊳',
            r'\unlhd': '⊴',
            r'\unrhd': '⊵',
            r'\oplus': '⊕',
            r'\ominus': '⊖',
            r'\otimes': '⊗',
            r'\oslash': '⊘',
            r'\odot': '⊙',
            r'\bigcirc': '◯',
            r'\dagger': '†',
            r'\ddagger': '‡',
            r'\amalg': '⨿',
            
            # Relations
            r'\leq': '≤',
            r'\le': '≤',
            r'\geq': '≥',
            r'\ge': '≥',
            r'\equiv': '≡',
            r'\models': '⊨',
            r'\prec': '≺',
            r'\succ': '≻',
            r'\sim': '∼',
            r'\perp': '⊥',
            r'\preceq': '⪯',
            r'\succeq': '⪰',
            r'\simeq': '≃',
            r'\mid': '∣',
            r'\ll': '≪',
            r'\gg': '≫',
            r'\asymp': '≍',
            r'\parallel': '∥',
            r'\subset': '⊂',
            r'\supset': '⊃',
            r'\approx': '≈',
            r'\bowtie': '⋈',
            r'\subseteq': '⊆',
            r'\supseteq': '⊇',
            r'\cong': '≅',
            r'\sqsubset': '⊏',
            r'\sqsupset': '⊐',
            r'\neq': '≠',
            r'\ne': '≠',
            r'\smile': '⌣',
            r'\sqsubseteq': '⊑',
            r'\sqsupseteq': '⊒',
            r'\doteq': '≐',
            r'\frown': '⌢',
            r'\in': '∈',
            r'\ni': '∋',
            r'\propto': '∝',
            r'\vdash': '⊢',
            r'\dashv': '⊣',
            
            # Arrows
            r'\leftarrow': '←',
            r'\gets': '←',
            r'\rightarrow': '→',
            r'\to': '→',
            r'\leftrightarrow': '↔',
            r'\uparrow': '↑',
            r'\downarrow': '↓',
            r'\updownarrow': '↕',
            r'\Leftarrow': '⇐',
            r'\Rightarrow': '⇒',
            r'\Leftrightarrow': '⇔',
            r'\Uparrow': '⇑',
            r'\Downarrow': '⇓',
            r'\Updownarrow': '⇕',
            r'\mapsto': '↦',
            r'\longmapsto': '⟼',
            r'\hookleftarrow': '↩',
            r'\hookrightarrow': '↪',
            r'\leftharpoonup': '↼',
            r'\leftharpoondown': '↽',
            r'\rightharpoonup': '⇀',
            r'\rightharpoondown': '⇁',
            r'\rightleftharpoons': '⇌',
            r'\iff': '⟺',
            
            # Miscellaneous symbols
            r'\ldots': '…',
            r'\cdots': '⋯',
            r'\vdots': '⋮',
            r'\ddots': '⋱',
            r'\aleph': 'ℵ',
            r'\prime': '′',
            r'\forall': '∀',
            r'\exists': '∃',
            r'\mho': '℧',
            r'\partial': '∂',
            r'\emptyset': '∅',
            r'\infty': '∞',
            r'\nabla': '∇',
            r'\triangle': '△',
            r'\Box': '□',
            r'\Diamond': '◊',
            r'\bot': '⊥',
            r'\top': '⊤',
            r'\angle': '∠',
            r'\surd': '√',
            r'\diamondsuit': '♦',
            r'\heartsuit': '♥',
            r'\clubsuit': '♣',
            r'\spadesuit': '♠',
            r'\neg': '¬',
            r'\lnot': '¬',
            r'\flat': '♭',
            r'\natural': '♮',
            r'\sharp': '♯',
            
            # Large operators
            r'\sum': '∑',
            r'\prod': '∏',
            r'\coprod': '∐',
            r'\int': '∫',
            r'\oint': '∮',
            r'\bigcap': '⋂',
            r'\bigcup': '⋃',
            r'\bigsqcup': '⨆',
            r'\bigvee': '⋁',
            r'\bigwedge': '⋀',
            r'\bigodot': '⨀',
            r'\bigotimes': '⨂',
            r'\bigoplus': '⨁',
            r'\biguplus': '⨄',
            
            # Common formulas with superscripts/subscripts
            r'x^2': 'x²',
            r'x^3': 'x³',
            r'x^n': 'xⁿ',
            r'x_i': 'xᵢ',
            r'x_0': 'x₀',
            r'x_1': 'x₁',
            r'x_2': 'x₂',
            r'x_n': 'xₙ',
            r'a_i': 'aᵢ',
            r'a_n': 'aₙ',
            r'f(x)': 'f(x)',
            r'g(x)': 'g(x)',
            r'h(x)': 'h(x)',
            r'F(x)': 'F(x)',
            r'G(x)': 'G(x)',
            r'H(x)': 'H(x)',
            
            # Common mathematical expressions
            r'\sum_{i=1}^n': '∑ᵢ₌₁ⁿ',
            r'\sum_{i=0}^n': '∑ᵢ₌₀ⁿ',
            r'\prod_{i=1}^n': '∏ᵢ₌₁ⁿ',
            r'\int_0^\infty': '∫₀^∞',
            r'\int_{-\infty}^\infty': '∫₋∞^∞',
            r'\int_a^b': '∫ₐᵇ',
            r'\frac{1}{2}': '½',
            r'\frac{1}{3}': '⅓',
            r'\frac{2}{3}': '⅔',
            r'\frac{1}{4}': '¼',
            r'\frac{3}{4}': '¾',
            r'\frac{1}{5}': '⅕',
            r'\frac{1}{6}': '⅙',
            r'\frac{1}{8}': '⅛',
            r'\frac{a}{b}': 'a/b',
            r'\frac{x}{y}': 'x/y',
            r'\sqrt{x}': '√x',
            r'\sqrt{2}': '√2',
            r'\sqrt{3}': '√3',
            r'\sqrt{n}': '√n',
            r'e^x': 'eˣ',
            r'e^{-x}': 'e⁻ˣ',
            r'e^{i\pi}': 'e^(iπ)',
            r'2^n': '2ⁿ',
            r'10^n': '10ⁿ',
            
            # Trigonometric functions
            r'\sin x': 'sin x',
            r'\cos x': 'cos x',
            r'\tan x': 'tan x',
            r'\cot x': 'cot x',
            r'\sec x': 'sec x',
            r'\csc x': 'csc x',
            r'\arcsin x': 'arcsin x',
            r'\arccos x': 'arccos x',
            r'\arctan x': 'arctan x',
            r'\sinh x': 'sinh x',
            r'\cosh x': 'cosh x',
            r'\tanh x': 'tanh x',
            
            # Logarithmic functions
            r'\log x': 'log x',
            r'\ln x': 'ln x',
            r'\log_2 x': 'log₂ x',
            r'\log_{10} x': 'log₁₀ x',
            r'\lg x': 'lg x',
            
            # Common expressions with operators
            r'A \times B': 'A × B',
            r'A \cdot B': 'A · B',
            r'a \leq b': 'a ≤ b',
            r'a \geq b': 'a ≥ b',
            r'a \neq b': 'a ≠ b',
            r'a \approx b': 'a ≈ b',
            r'a \equiv b': 'a ≡ b',
            r'a \in B': 'a ∈ B',
            r'a \notin B': 'a ∉ B',
            r'A \subset B': 'A ⊂ B',
            r'A \supset B': 'A ⊃ B',
            r'A \subseteq B': 'A ⊆ B',
            r'A \supseteq B': 'A ⊇ B',
            r'A \cup B': 'A ∪ B',
            r'A \cap B': 'A ∩ B',
            r'A \setminus B': 'A ∖ B',
        }
        
        if os.path.exists(self.mapping_file):
            try:
                with open(self.mapping_file, 'r', encoding='utf-8') as f:
                    custom_mappings = json.load(f)
                    default_mappings.update(custom_mappings)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load custom mappings from {self.mapping_file}: {e}")
        
        return default_mappings
      
    def confirm_change(self, line_num: int, original_line: str, formula: str, unicode_repr: str) -> bool:
      """Ask user to confirm a change before applying it."""
      if self.auto_yes:
          return True
      
      print(f"\n--- Line {line_num} ---")
      print(f"Original: {original_line.strip()}")
      print(f"Math formula found: ${formula}$")
      print(f"Default mapping: {unicode_repr}")
      
      while True:
          response = input("Apply this change? [Y/n/c(ustom)]: ").strip().lower()
          if response in ['', 'y', 'yes']:
              return True
          elif response in ['n', 'no']:
              return False
          elif response in ['c', 'custom']:
              custom_mapping = input(f"Enter custom mapping for '${formula}$': ").strip()
              if custom_mapping:
                  self.math_mappings[formula] = custom_mapping
                  return True
              else:
                  print("No custom mapping provided, skipping change.")
                  return False
          else:
              print("Please enter 'y' (yes), 'n' (no), or 'c' (custom)")

    def save_mappings(self):
        """Save current mappings to file."""
        try:
            with open(self.mapping_file, 'w', encoding='utf-8') as f:
                json.dump(self.math_mappings, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save mappings to {self.mapping_file}: {e}")
    
    def convert_formula_to_unicode(self, formula: str) -> str:
        """Convert a complete math formula to unicode representation."""
        # First check if we have an exact mapping for this formula
        if formula in self.math_mappings:
            return self.math_mappings[formula]
        
        # If not found, ask the user
        print(f"\nUnknown math formula found: ${formula}$")
        
        while True:
            user_input = input(f"Enter unicode/text representation for '${formula}$' (or press Enter to use formula as-is): ").strip()
            if user_input == "":
                # Use the formula as-is, removing LaTeX commands for readability
                unicode_repr = self.create_fallback_representation(formula)
                break
            else:
                # Add to mappings and use the user's input
                self.math_mappings[formula] = user_input
                unicode_repr = user_input
                print(f"Added mapping: ${formula}$ -> {user_input}")
                break
        
        return unicode_repr
    
    def create_fallback_representation(self, formula: str) -> str:
        """Create a fallback text representation using intelligent conversion."""
        fallback = formula
        
        # First, try to use existing mappings for individual components
        fallback = self._apply_known_mappings(fallback)
        
        # Handle complex structures (these handle their own spacing)
        fallback = self._handle_fractions(fallback)
        fallback = self._handle_square_roots(fallback)
        fallback = self._handle_superscripts_subscripts(fallback)
        
        # Clean up remaining LaTeX commands (but preserve spacing from above)
        fallback = self._cleanup_latex_commands(fallback)
        
        # Final cleanup
        fallback = re.sub(r'\s+', ' ', fallback).strip()
        
        return fallback
    
    def _apply_known_mappings(self, text: str) -> str:
        """Apply known mappings to LaTeX commands in the text."""
        result = text
        
        # Sort by length (longest first) to avoid partial replacements
        sorted_mappings = sorted(self.math_mappings.items(), key=lambda x: len(x[0]), reverse=True)
        
        for latex_cmd, unicode_repr in sorted_mappings:
            # Only replace if it's a complete command (word boundary or specific context)
            if latex_cmd.startswith('\\'):
                # For LaTeX commands, ensure word boundary
                pattern = re.escape(latex_cmd) + r'(?![a-zA-Z])'
                result = re.sub(pattern, unicode_repr, result)
            else:
                # For other patterns (like x^2), do direct replacement
                result = result.replace(latex_cmd, unicode_repr)
        
        return result
    
    def _handle_fractions(self, text: str) -> str:
        """Handle fraction notation."""
        # Handle \frac{numerator}{denominator}
        def replace_frac(match):
            num = match.group(1)
            den = match.group(2)
            # Recursively process numerator and denominator but don't apply cleanup yet
            num_processed = self._apply_known_mappings(num)
            den_processed = self._apply_known_mappings(den)
            
            # Clean up spaces in the components
            num_processed = re.sub(r'\s+', '', num_processed)
            den_processed = re.sub(r'\s+', '', den_processed)
            
            # Use parentheses if the parts contain operators
            if any(op in num_processed for op in ['+', '-', '*']):
                num_processed = f"({num_processed})"
            if any(op in den_processed for op in ['+', '-', '*']):
                den_processed = f"({den_processed})"
            
            # Use a special marker to prevent cleanup from adding spaces around this /
            return f"{num_processed}⟨FRAC⟩{den_processed}"
        
        result = re.sub(r'\\frac\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', 
                       replace_frac, text)
        
        # Replace the marker with / after cleanup
        return result
    
    def _handle_square_roots(self, text: str) -> str:
        """Handle square root notation."""
        def replace_sqrt(match):
            content = match.group(1)
            # Recursively process content
            content_processed = self._apply_known_mappings(content)
            
            # Clean up spaces in the content
            content_clean = re.sub(r'\s+', '', content_processed)
            
            # Use parentheses if content contains operators
            if any(op in content_clean for op in ['+', '-', '*', '/']):
                return f"√({content_clean})"
            else:
                return f"√{content_clean}"
        
        return re.sub(r'\\sqrt\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', replace_sqrt, text)
    
    def _handle_superscripts_subscripts(self, text: str) -> str:
        """Handle superscripts and subscripts with Unicode characters."""
        # Superscript mappings
        superscript_map = {
            '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', 
            '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '+': '⁺', '-': '⁻',
            '=': '⁼', '(': '⁽', ')': '⁾', 'n': 'ⁿ', 'i': 'ⁱ', 'x': 'ˣ'
        }
        
        # Subscript mappings
        subscript_map = {
            '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅',
            '6': '₆', '7': '₇', '8': '₈', '9': '₉', '+': '₊', '-': '₋',
            '=': '₌', '(': '₍', ')': '₎', 'a': 'ₐ', 'e': 'ₑ', 'h': 'ₕ',
            'i': 'ᵢ', 'j': 'ⱼ', 'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ',
            'o': 'ₒ', 'p': 'ₚ', 'r': 'ᵣ', 's': 'ₛ', 't': 'ₜ', 'u': 'ᵤ',
            'v': 'ᵥ', 'x': 'ₓ'
        }
        
        def convert_script(text_part, script_map):
            """Convert text to superscript or subscript."""
            result = ""
            for char in text_part:
                result += script_map.get(char, char)
            return result
        
        # Handle superscripts ^{...} and ^x
        def replace_superscript(match):
            content = match.group(1) if match.group(1) else match.group(2)
            return convert_script(content, superscript_map)
        
        text = re.sub(r'\^\{([^}]+)\}|\^([a-zA-Z0-9])', replace_superscript, text)
        
        # Handle subscripts _{...} and _x
        def replace_subscript(match):
            content = match.group(1) if match.group(1) else match.group(2)
            return convert_script(content, subscript_map)
        
        text = re.sub(r'_\{([^}]+)\}|_([a-zA-Z0-9])', replace_subscript, text)
        
        return text
    
    def _cleanup_latex_commands(self, text: str) -> str:
        """Clean up remaining LaTeX commands and formatting."""
        # Remove remaining unknown LaTeX commands (including backslash)
        text = re.sub(r'\\[a-zA-Z]+\*?', '', text)
        
        # Convert remaining braces to parentheses for readability
        text = re.sub(r'\{([^{}]*)\}', r'(\1)', text)
        
        # Clean up multiple spaces first
        text = re.sub(r'\s+', ' ', text)
        
        # Clean up orphaned operators from removed commands
        text = re.sub(r'^\s*[+\-*/=<>]\s*', '', text)  # Remove leading operators
        text = re.sub(r'\s*[+\-*/=<>]\s*$', '', text)  # Remove trailing operators
        text = re.sub(r'([+\-*/=<>])\s*\1+', r'\1', text)  # Remove double operators
        
        # Only add spaces around operators that are NOT within parentheses or after fractions/roots
        # This is a more conservative approach - only add spaces where clearly needed
        # Don't modify operators that are already properly formatted by fractions/roots
        if not ('(' in text and ')' in text) and not ('√' in text) and not ('⟨FRAC⟩' in text):
            text = re.sub(r'\s*([+\-*/=<>])\s*', r' \1 ', text)
        
        # Replace fraction markers with / (after spacing decisions are made)
        text = text.replace('⟨FRAC⟩', '/')
        
        # Final cleanup - collapse multiple spaces but preserve single spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def is_inside_texorpdfstring(self, line: str, match_start: int) -> bool:
        """Check if the math formula is already inside a \\texorpdfstring command."""
        # Look backwards from the match to see if we're inside \texorpdfstring
        before_match = line[:match_start]
        
        # Find the last \texorpdfstring before our position
        texorpdf_pattern = r'\\texorpdfstring\s*\{'
        texorpdf_matches = list(re.finditer(texorpdf_pattern, before_match))
        
        if not texorpdf_matches:
            return False
        
        # Check if we're inside the scope of the last \texorpdfstring
        last_match = texorpdf_matches[-1]
        start_pos = last_match.end()
        
        # Count braces to find the end of the \texorpdfstring
        brace_count = 1
        pos = start_pos
        first_arg_end = -1
        
        while pos < len(line) and brace_count > 0:
            if line[pos] == '{':
                brace_count += 1
            elif line[pos] == '}':
                brace_count -= 1
                if brace_count == 0 and first_arg_end == -1:
                    first_arg_end = pos
            pos += 1
        
        # If our math formula is within the first argument of \texorpdfstring
        if start_pos <= match_start <= first_arg_end:
            return True
        
        return False
    
    def process_line(self, line_num: int, line: str) -> str:
        """Process a single line, replacing math formulas in section headings."""
        # Check if line starts with \section or \subsection
        if not re.match(r'^\s*\\(sub)?section\s*\{', line):
            return line
        
        # Find all math formulas (content between single $)
        math_pattern = r'\$([^$]+)\$'
        matches = list(re.finditer(math_pattern, line))
        
        if not matches:
            return line
        
        # Process matches in reverse order to maintain positions
        modified_line = line
        
        for match in reversed(matches):
            start, end = match.span()
            full_formula = match.group(0)  # includes the $ signs
            formula_content = match.group(1)  # content without $ signs
            
            # Check if already inside \texorpdfstring
            if self.is_inside_texorpdfstring(line, start):
                continue
            
            # Convert formula to unicode representation
            unicode_repr = self.convert_formula_to_unicode(formula_content)
            # Ask for confirmation before making the change
            if not self.confirm_change(line_num, line, formula_content, unicode_repr):
                continue
            # Create replacement
            replacement = f'\\texorpdfstring{{{full_formula}}}{{{unicode_repr}}}'
            
            # Replace in the line
            modified_line = modified_line[:start] + replacement + modified_line[end:]
        
        return modified_line

    def process_file(self, input_file: str, output_file: Optional[str] = None) -> None:
        """Process a TeX file, fixing math formulas in section headings."""
        if output_file is None:
            output_file = input_file
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except IOError as e:
            print(f"Error reading file {input_file}: {e}")
            return
        
        modified_lines = []
        changes_made = False
        
        for i, line in enumerate(lines, 1):
            original_line = line
            processed_line = self.process_line(line_num, line)
            
            if processed_line != original_line:
                changes_made = True
                print(f"Line {i}: Modified section heading")
                print(f"  Before: {original_line.strip()}")
                print(f"  After:  {processed_line.strip()}")
                print()
            
            modified_lines.append(processed_line)
        
        if changes_made:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.writelines(modified_lines)
                print(f"File processed successfully. Output written to: {output_file}")
                
                # Save any new mappings
                self.save_mappings()
                
            except IOError as e:
                print(f"Error writing to file {output_file}: {e}")
        else:
            print("No changes needed - no math formulas found in section headings.")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Fix TeX hyperref errors by wrapping math formulas in section headings with \\texorpdfstring"
    )
    parser.add_argument("input_file", help="Input TeX file to process")
    parser.add_argument("-o", "--output", help="Output file (default: overwrite input file)")
    parser.add_argument("-m", "--mappings", default="math_mappings.json", 
                       help="JSON file for custom math formula mappings (default: math_mappings.json)")
    parser.add_argument("-y", "--yes", action="store_true",
                       help="Automatically accept all default mappings without prompting")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
        return 1
    
    fixer = TexHeadingFixer(args.mappings, args.yes)  # Pass the --yes flag
    fixer.process_file(args.input_file, args.output)
    
    return 0


if __name__ == "__main__":
    exit(main())
