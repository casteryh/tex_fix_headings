#!/usr/bin/env python3
"""
Unit tests for TeX Heading Math Formula Fixer
"""

import unittest
import tempfile
import os
import json
from unittest.mock import patch, mock_open
from tex_fix_heading import TexHeadingFixer


class TestTexHeadingFixer(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary mapping file for testing
        self.temp_mapping_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_mapping_file.close()
        self.fixer = TexHeadingFixer(self.temp_mapping_file.name)
    
    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.temp_mapping_file.name):
            os.unlink(self.temp_mapping_file.name)
    
    def test_load_default_mappings(self):
        """Test that default mappings are loaded correctly."""
        # Test some key default mappings
        self.assertEqual(self.fixer.math_mappings[r'\alpha'], 'α')
        self.assertEqual(self.fixer.math_mappings[r'\beta'], 'β')
        self.assertEqual(self.fixer.math_mappings['x^2'], 'x²')
        self.assertEqual(self.fixer.math_mappings[r'\times'], '×')
        self.assertEqual(self.fixer.math_mappings[r'\leq'], '≤')
        self.assertEqual(self.fixer.math_mappings[r'\in'], '∈')
        self.assertEqual(self.fixer.math_mappings[r'\sum'], '∑')
    
    def test_load_custom_mappings(self):
        """Test loading custom mappings from file."""
        custom_mappings = {
            "custom_formula": "Custom Unicode",
            r"\alpha": "custom_alpha"  # Override default
        }
        
        with open(self.temp_mapping_file.name, 'w') as f:
            json.dump(custom_mappings, f)
        
        fixer = TexHeadingFixer(self.temp_mapping_file.name)
        
        # Check that custom mappings are loaded
        self.assertEqual(fixer.math_mappings["custom_formula"], "Custom Unicode")
        # Check that custom mapping overrides default
        self.assertEqual(fixer.math_mappings[r"\alpha"], "custom_alpha")
        # Check that other defaults are still present
        self.assertEqual(fixer.math_mappings[r'\beta'], 'β')
    
    def test_save_mappings(self):
        """Test saving mappings to file."""
        # Add a new mapping
        self.fixer.math_mappings["test_formula"] = "test_unicode"
        
        # Save mappings
        self.fixer.save_mappings()
        
        # Load and verify
        with open(self.temp_mapping_file.name, 'r') as f:
            saved_mappings = json.load(f)
        
        self.assertEqual(saved_mappings["test_formula"], "test_unicode")
        self.assertEqual(saved_mappings[r"\alpha"], "α")
    
    def test_convert_formula_to_unicode_known(self):
        """Test converting known formulas to unicode."""
        # Test exact matches
        self.assertEqual(self.fixer.convert_formula_to_unicode(r'\alpha'), 'α')
        self.assertEqual(self.fixer.convert_formula_to_unicode('x^2'), 'x²')
        self.assertEqual(self.fixer.convert_formula_to_unicode(r'\frac{a}{b}'), 'a/b')
    
    def test_create_fallback_representation(self):
        """Test fallback representation creation."""
        # Test simple Greek letter
        result = self.fixer.create_fallback_representation(r'\alpha')
        self.assertEqual(result, 'α')  # Should use mapping
        
        # Test unknown command - should be removed
        result = self.fixer.create_fallback_representation(r'\unknown')
        self.assertEqual(result, '')  # Should remove unknown command
        
        # Test complex expression
        result = self.fixer.create_fallback_representation(r'x + \alpha + y')
        self.assertEqual(result, 'x + α + y')
        
        # Test fraction
        result = self.fixer.create_fallback_representation(r'\frac{x+1}{y-1}')
        self.assertEqual(result, '(x+1)/(y-1)')
        
        # Test square root
        result = self.fixer.create_fallback_representation(r'\sqrt{x+1}')
        self.assertEqual(result, '√(x+1)')
        
        # Test mixed expression
        result = self.fixer.create_fallback_representation(r'\alpha^2 + \beta_i')
        self.assertEqual(result, 'α² + βᵢ')
    
    def test_is_inside_texorpdfstring(self):
        """Test detection of formulas already inside texorpdfstring."""
        # Test formula not inside texorpdfstring
        line = r'\section{Test $\alpha$ formula}'
        self.assertFalse(self.fixer.is_inside_texorpdfstring(line, line.find('$')))
        
        # Test formula inside texorpdfstring
        line = r'\section{Test \texorpdfstring{$\alpha$}{alpha} formula}'
        alpha_pos = line.find('$')
        self.assertTrue(self.fixer.is_inside_texorpdfstring(line, alpha_pos))
        
        # Test formula after texorpdfstring
        line = r'\section{Test \texorpdfstring{$\alpha$}{alpha} and $\beta$}'
        beta_pos = line.rfind('$')
        self.assertFalse(self.fixer.is_inside_texorpdfstring(line, beta_pos))
        
        # Test multiple texorpdfstring commands
        line = r'\section{\texorpdfstring{$\alpha$}{α} and \texorpdfstring{$\beta$}{β}}'
        alpha_pos = line.find('$')
        beta_pos = line.rfind('$')
        self.assertTrue(self.fixer.is_inside_texorpdfstring(line, alpha_pos))
        self.assertTrue(self.fixer.is_inside_texorpdfstring(line, beta_pos))
    
    def test_process_line_section(self):
        """Test processing section lines."""
        # Test basic section with formula
        line = r'\section{Introduction to $\alpha$ particles}'
        result = self.fixer.process_line(line)
        expected = r'\section{Introduction to \texorpdfstring{$\alpha$}{α} particles}'
        self.assertEqual(result, expected)
        
        # Test subsection with formula
        line = r'\subsection{The $x^2$ function}'
        result = self.fixer.process_line(line)
        expected = r'\subsection{The \texorpdfstring{$x^2$}{x²} function}'
        self.assertEqual(result, expected)
        
        # Test section with multiple formulas
        line = r'\section{Study of $\alpha$ and $\beta$ particles}'
        result = self.fixer.process_line(line)
        expected = r'\section{Study of \texorpdfstring{$\alpha$}{α} and \texorpdfstring{$\beta$}{β} particles}'
        self.assertEqual(result, expected)
    
    def test_process_line_non_section(self):
        """Test that non-section lines are not processed."""
        # Test regular text with formula
        line = r'This is text with $\alpha$ formula'
        result = self.fixer.process_line(line)
        self.assertEqual(result, line)  # Should be unchanged
        
        # Test other LaTeX commands
        line = r'\begin{equation} $\alpha$ \end{equation}'
        result = self.fixer.process_line(line)
        self.assertEqual(result, line)  # Should be unchanged
        
        # Test chapter (not section/subsection)
        line = r'\chapter{Introduction to $\alpha$ particles}'
        result = self.fixer.process_line(line)
        self.assertEqual(result, line)  # Should be unchanged
    
    def test_process_line_already_fixed(self):
        """Test that already fixed lines are not processed again."""
        line = r'\section{Test \texorpdfstring{$\alpha$}{α} particles}'
        result = self.fixer.process_line(line)
        self.assertEqual(result, line)  # Should be unchanged
    
    def test_process_line_whitespace_handling(self):
        """Test handling of whitespace in section commands."""
        # Test with spaces around section command
        line = r'  \section  {  Introduction to $\alpha$ particles  }  '
        result = self.fixer.process_line(line)
        expected = r'  \section  {  Introduction to \texorpdfstring{$\alpha$}{α} particles  }  '
        self.assertEqual(result, expected)
    
    def test_complex_formulas(self):
        """Test processing of complex mathematical formulas."""
        # Test fraction
        line = r'\section{Analysis of $\frac{a}{b}$ ratios}'
        result = self.fixer.process_line(line)
        expected = r'\section{Analysis of \texorpdfstring{$\frac{a}{b}$}{a/b} ratios}'
        self.assertEqual(result, expected)
        
        # Test square root
        line = r'\section{Square root $\sqrt{x}$ functions}'
        result = self.fixer.process_line(line)
        expected = r'\section{Square root \texorpdfstring{$\sqrt{x}$}{√x} functions}'
        self.assertEqual(result, expected)
        
        # Test exponential
        line = r'\section{Exponential $e^x$ growth}'
        result = self.fixer.process_line(line)
        expected = r'\section{Exponential \texorpdfstring{$e^x$}{eˣ} growth}'
        self.assertEqual(result, expected)
    
    def test_edge_cases(self):
        """Test edge cases and potential error conditions."""
        # Test empty formula
        line = r'\section{Test $$ formula}'
        result = self.fixer.process_line(line)
        self.assertEqual(result, line)  # Should be unchanged (empty formula)
        
        # Test single dollar sign (not a formula)
        line = r'\section{Cost is $5}'
        result = self.fixer.process_line(line)
        self.assertEqual(result, line)  # Should be unchanged (not a math formula)
        
        # Test nested braces in section title
        line = r'\section{Test $\frac{a}{b}$ with {nested} braces}'
        result = self.fixer.process_line(line)
        expected = r'\section{Test \texorpdfstring{$\frac{a}{b}$}{a/b} with {nested} braces}'
        self.assertEqual(result, expected)
    
    def test_unicode_subscripts_superscripts(self):
        """Test Unicode subscript and superscript handling."""
        # Test superscripts
        result = self.fixer.create_fallback_representation('x^2')
        self.assertEqual(result, 'x²')
        
        result = self.fixer.create_fallback_representation('x^3')
        self.assertEqual(result, 'x³')
        
        result = self.fixer.create_fallback_representation('x^n')
        self.assertEqual(result, 'xⁿ')
        
        # Test subscripts
        result = self.fixer.create_fallback_representation('x_0')
        self.assertEqual(result, 'x₀')
        
        result = self.fixer.create_fallback_representation('x_i')
        self.assertEqual(result, 'xᵢ')
        
        result = self.fixer.create_fallback_representation('x_n')
        self.assertEqual(result, 'xₙ')
    
    def test_mathematical_operators(self):
        """Test mathematical operator conversion."""
        # Test basic operators
        result = self.fixer.create_fallback_representation(r'a \times b')
        self.assertEqual(result, 'a × b')
        
        result = self.fixer.create_fallback_representation(r'a \cdot b')
        self.assertEqual(result, 'a · b')
        
        result = self.fixer.create_fallback_representation(r'a \pm b')
        self.assertEqual(result, 'a ± b')
        
        # Test relations
        result = self.fixer.create_fallback_representation(r'a \leq b')
        self.assertEqual(result, 'a ≤ b')
        
        result = self.fixer.create_fallback_representation(r'a \geq b')
        self.assertEqual(result, 'a ≥ b')
        
        result = self.fixer.create_fallback_representation(r'a \neq b')
        self.assertEqual(result, 'a ≠ b')


class TestFallbackStrategy(unittest.TestCase):
    """Test the fallback representation strategy."""
    
    def setUp(self):
        self.fixer = TexHeadingFixer()
    
    def test_fallback_with_known_symbols(self):
        """Test fallback when formula contains known symbols."""
        result = self.fixer.create_fallback_representation(r'\alpha + \beta')
        self.assertEqual(result, 'α + β')
    
    def test_fallback_with_unknown_symbols(self):
        """Test fallback when formula contains unknown symbols."""
        result = self.fixer.create_fallback_representation(r'\unknown + x')
        self.assertEqual(result, 'x')  # Unknown symbol removed, x remains
    
    def test_fallback_mixed_known_unknown(self):
        """Test fallback with mix of known and unknown symbols."""
        result = self.fixer.create_fallback_representation(r'\alpha + \unknown + \beta')
        self.assertEqual(result, 'α + β')
    
    def test_fallback_complex_expressions(self):
        """Test fallback with complex mathematical expressions."""
        # Test integral with limits
        result = self.fixer.create_fallback_representation(r'\int_0^\infty f(x) dx')
        self.assertEqual(result, '∫₀^∞ f(x) dx')
        
        # Test sum with limits
        result = self.fixer.create_fallback_representation(r'\sum_{i=1}^n x_i')
        self.assertEqual(result, '∑ᵢ₌₁ⁿ xᵢ')
    
    def test_fallback_preserves_variables(self):
        """Test that fallback preserves variable names and numbers."""
        result = self.fixer.create_fallback_representation(r'x + y + 123 + \alpha')
        self.assertEqual(result, 'x + y + 123 + α')
    
    def test_fallback_handles_braces(self):
        """Test that fallback properly handles braces."""
        result = self.fixer.create_fallback_representation(r'x^{n+1} + y_{i-1}')
        self.assertEqual(result, 'xⁿ⁺¹ + yᵢ₋₁')  # Unicode superscripts/subscripts


if __name__ == '__main__':
    unittest.main()
