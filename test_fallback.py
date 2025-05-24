#!/usr/bin/env python3
"""
Simple test script to verify the refactored fallback strategy
"""

from tex_fix_heading import TexHeadingFixer

def test_fallback_strategy():
    """Test the improved fallback strategy."""
    fixer = TexHeadingFixer()
    
    test_cases = [
        # Basic Greek letters
        (r'\alpha + \beta', 'α + β'),
        
        # Fractions
        (r'\frac{x+1}{y-1}', '(x+1)/(y-1)'),
        (r'\frac{a}{b}', 'a/b'),
        
        # Square roots
        (r'\sqrt{x+1}', '√(x+1)'),
        (r'\sqrt{x}', '√x'),
        
        # Superscripts and subscripts
        (r'x^2 + y_i', 'x² + yᵢ'),
        (r'x^{n+1}', 'xⁿ⁺¹'),
        (r'a_{i-1}', 'aᵢ₋₁'),
        
        # Complex expressions
        (r'\alpha^2 + \beta_i', 'α² + βᵢ'),
        (r'\int_0^\infty f(x) dx', '∫₀^∞ f(x) dx'),
        (r'\sum_{i=1}^n x_i', '∑ᵢ₌₁ⁿ xᵢ'),
        
        # Mixed known and unknown
        (r'\alpha + \unknown + \beta', 'α + β'),
        (r'x + y + 123 + \gamma', 'x + y + 123 + γ'),
    ]
    
    print("Testing improved fallback strategy:")
    print("=" * 50)
    
    all_passed = True
    for i, (input_formula, expected) in enumerate(test_cases, 1):
        result = fixer.create_fallback_representation(input_formula)
        passed = result == expected
        all_passed = all_passed and passed
        
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"Test {i:2d}: {status}")
        print(f"  Input:    {input_formula}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {result}")
        if not passed:
            print(f"  ERROR: Expected '{expected}' but got '{result}'")
        print()
    
    print("=" * 50)
    if all_passed:
        print("✓ All tests PASSED! Fallback strategy is working correctly.")
    else:
        print("✗ Some tests FAILED. Please check the implementation.")
    
    return all_passed

def test_section_processing():
    """Test section line processing."""
    fixer = TexHeadingFixer()
    
    test_cases = [
        (r'\section{Introduction to $\alpha$ particles}', 
         r'\section{Introduction to \texorpdfstring{$\alpha$}{α} particles}'),
        
        (r'\subsection{The $x^2$ function}', 
         r'\subsection{The \texorpdfstring{$x^2$}{x²} function}'),
        
        (r'\section{Study of $\frac{a}{b}$ ratios}', 
         r'\section{Study of \texorpdfstring{$\frac{a}{b}$}{a/b} ratios}'),
    ]
    
    print("Testing section processing:")
    print("=" * 50)
    
    all_passed = True
    for i, (input_line, expected) in enumerate(test_cases, 1):
        result = fixer.process_line(input_line)
        passed = result == expected
        all_passed = all_passed and passed
        
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"Test {i}: {status}")
        print(f"  Input:    {input_line}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {result}")
        if not passed:
            print(f"  ERROR: Mismatch in processing")
        print()
    
    return all_passed

if __name__ == '__main__':
    print("Testing TeX Heading Fixer - Refactored Fallback Strategy")
    print("=" * 60)
    print()
    
    fallback_passed = test_fallback_strategy()
    print()
    section_passed = test_section_processing()
    
    print("=" * 60)
    if fallback_passed and section_passed:
        print("🎉 ALL TESTS PASSED! The refactored code is working correctly.")
    else:
        print("❌ SOME TESTS FAILED. Please review the implementation.")
