"""
Unit tests for Calculator basic operations.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from calculator import Calculator


class TestCalculatorBasicOperations(unittest.TestCase):
    """Test suite for basic calculator operations."""
    
    def setUp(self):
        """Set up a fresh calculator instance for each test."""
        self.calc = Calculator()
    
    # Addition Tests
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        result = self.calc.add(5, 3)
        self.assertEqual(result, 8)
    
    def test_add_negative_numbers(self):
        """Test adding negative numbers."""
        result = self.calc.add(-5, -3)
        self.assertEqual(result, -8)
    
    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        result = self.calc.add(10, -3)
        self.assertEqual(result, 7)
    
    def test_add_decimal_numbers(self):
        """Test adding decimal numbers."""
        result = self.calc.add(3.5, 2.7)
        self.assertAlmostEqual(result, 6.2, places=7)
    
    def test_add_zero(self):
        """Test adding zero."""
        result = self.calc.add(5, 0)
        self.assertEqual(result, 5)
    
    def test_add_large_numbers(self):
        """Test adding large numbers."""
        result = self.calc.add(999999999, 1)
        self.assertEqual(result, 1000000000)
    
    # Subtraction Tests
    def test_subtract_positive_numbers(self):
        """Test subtracting positive numbers."""
        result = self.calc.subtract(10, 3)
        self.assertEqual(result, 7)
    
    def test_subtract_negative_numbers(self):
        """Test subtracting negative numbers."""
        result = self.calc.subtract(-5, -3)
        self.assertEqual(result, -2)
    
    def test_subtract_resulting_negative(self):
        """Test subtraction resulting in negative number."""
        result = self.calc.subtract(3, 10)
        self.assertEqual(result, -7)
    
    def test_subtract_decimal_numbers(self):
        """Test subtracting decimal numbers."""
        result = self.calc.subtract(7.5, 2.3)
        self.assertAlmostEqual(result, 5.2, places=7)
    
    def test_subtract_zero(self):
        """Test subtracting zero."""
        result = self.calc.subtract(5, 0)
        self.assertEqual(result, 5)
    
    # Multiplication Tests
    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers."""
        result = self.calc.multiply(4, 5)
        self.assertEqual(result, 20)
    
    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers."""
        result = self.calc.multiply(-4, -5)
        self.assertEqual(result, 20)
    
    def test_multiply_mixed_signs(self):
        """Test multiplying numbers with different signs."""
        result = self.calc.multiply(-4, 5)
        self.assertEqual(result, -20)
    
    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        result = self.calc.multiply(100, 0)
        self.assertEqual(result, 0)
    
    def test_multiply_decimal_numbers(self):
        """Test multiplying decimal numbers."""
        result = self.calc.multiply(2.5, 3.2)
        self.assertAlmostEqual(result, 8.0, places=7)
    
    def test_multiply_by_one(self):
        """Test multiplying by one."""
        result = self.calc.multiply(42, 1)
        self.assertEqual(result, 42)
    
    # Division Tests
    def test_divide_positive_numbers(self):
        """Test dividing positive numbers."""
        result = self.calc.divide(20, 4)
        self.assertEqual(result, 5)
    
    def test_divide_negative_numbers(self):
        """Test dividing negative numbers."""
        result = self.calc.divide(-20, -4)
        self.assertEqual(result, 5)
    
    def test_divide_mixed_signs(self):
        """Test dividing numbers with different signs."""
        result = self.calc.divide(-20, 4)
        self.assertEqual(result, -5)
    
    def test_divide_decimal_result(self):
        """Test division resulting in decimal."""
        result = self.calc.divide(10, 3)
        self.assertAlmostEqual(result, 3.333333, places=5)
    
    def test_divide_decimal_numbers(self):
        """Test dividing decimal numbers."""
        result = self.calc.divide(7.5, 2.5)
        self.assertAlmostEqual(result, 3.0, places=7)
    
    def test_divide_by_one(self):
        """Test dividing by one."""
        result = self.calc.divide(42, 1)
        self.assertEqual(result, 42)
    
    def test_divide_by_zero_error(self):
        """Test that dividing by zero raises ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10, 0)
    
    def test_divide_zero_by_number(self):
        """Test dividing zero by a number."""
        result = self.calc.divide(0, 5)
        self.assertEqual(result, 0)
    
    # Type Error Tests
    def test_add_invalid_input_type(self):
        """Test adding with invalid input types."""
        with self.assertRaises(TypeError):
            self.calc.add("five", 3)
    
    def test_subtract_invalid_input_type(self):
        """Test subtracting with invalid input types."""
        with self.assertRaises(TypeError):
            self.calc.subtract(10, "three")
    
    def test_multiply_invalid_input_type(self):
        """Test multiplying with invalid input types."""
        with self.assertRaises(TypeError):
            self.calc.multiply("two", "three")
    
    def test_divide_invalid_input_type(self):
        """Test dividing with invalid input types."""
        with self.assertRaises(TypeError):
            self.calc.divide(10, "two")
    
    # Edge Cases
    def test_add_very_small_numbers(self):
        """Test adding very small numbers."""
        result = self.calc.add(0.0000001, 0.0000002)
        self.assertAlmostEqual(result, 0.0000003, places=10)
    
    def test_scientific_notation(self):
        """Test operations with scientific notation."""
        result = self.calc.multiply(1e10, 2)
        self.assertEqual(result, 2e10)
    
    # History Tests for Basic Operations
    def test_operation_adds_to_history(self):
        """Test that operations are added to history."""
        self.calc.add(5, 3)
        self.calc.subtract(10, 4)
        history = self.calc.get_history()
        self.assertEqual(len(history), 2)
        # Check that history entries contain the operations
        self.assertIn("5 + 3 = 8", history[0])
        self.assertIn("10 - 4 = 6", history[1])
    
    def test_history_limit(self):
        """Test that history respects the maximum limit."""
        # Create calculator with max_history of 3
        calc = Calculator(max_history=3)
        for i in range(5):
            calc.add(i, 1)
        history = calc.get_history()
        self.assertEqual(len(history), 3)
        # Should contain only the last 3 operations
        self.assertIn("2 + 1 = 3", history[0])
        self.assertIn("3 + 1 = 4", history[1])
        self.assertIn("4 + 1 = 5", history[2])


class TestCalculatorChainOperations(unittest.TestCase):
    """Test suite for chaining calculator operations."""
    
    def setUp(self):
        """Set up a fresh calculator instance for each test."""
        self.calc = Calculator()
    
    def test_chain_multiple_operations(self):
        """Test performing multiple operations in sequence."""
        result1 = self.calc.add(10, 5)  # 15
        result2 = self.calc.multiply(result1, 2)  # 30
        result3 = self.calc.subtract(result2, 10)  # 20
        result4 = self.calc.divide(result3, 4)  # 5
        self.assertEqual(result4, 5)
    
    def test_operations_with_previous_results(self):
        """Test using results from previous operations."""
        self.calc.add(8, 2)  # 10
        self.calc.memory_add()  # Memory should be 10
        memory_value = self.calc.memory_recall()
        self.assertEqual(memory_value, 10)


if __name__ == '__main__':
    unittest.main()