"""
Unit tests for Calculator memory functions and history features.
"""

import unittest
import sys
import os
import json
import tempfile
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from calculator import Calculator


class TestCalculatorMemoryFunctions(unittest.TestCase):
    """Test suite for calculator memory functions."""
    
    def setUp(self):
        """Set up a fresh calculator instance for each test."""
        self.calc = Calculator()
    
    def test_initial_memory_is_zero(self):
        """Test that memory starts at zero."""
        self.assertEqual(self.calc.get_memory_value(), 0.0)
    
    def test_memory_add_with_value(self):
        """Test adding a specific value to memory."""
        self.calc.memory_add(10)
        self.assertEqual(self.calc.get_memory_value(), 10)
        self.calc.memory_add(5)
        self.assertEqual(self.calc.get_memory_value(), 15)
    
    def test_memory_add_negative_value(self):
        """Test adding negative values to memory."""
        self.calc.memory_add(-5)
        self.assertEqual(self.calc.get_memory_value(), -5)
    
    def test_memory_add_decimal_value(self):
        """Test adding decimal values to memory."""
        self.calc.memory_add(3.5)
        self.calc.memory_add(2.7)
        self.assertAlmostEqual(self.calc.get_memory_value(), 6.2, places=7)
    
    def test_memory_add_without_value_uses_last_result(self):
        """Test that memory_add without value uses last calculation result."""
        self.calc.add(10, 5)  # Result: 15
        self.calc.memory_add()  # Should add 15 to memory
        self.assertEqual(self.calc.get_memory_value(), 15)
    
    def test_memory_add_without_value_no_last_result_error(self):
        """Test that memory_add without value raises error when no last result."""
        with self.assertRaises(ValueError):
            self.calc.memory_add()
    
    def test_memory_subtract_with_value(self):
        """Test subtracting a specific value from memory."""
        self.calc.memory_add(20)
        self.calc.memory_subtract(5)
        self.assertEqual(self.calc.get_memory_value(), 15)
    
    def test_memory_subtract_negative_value(self):
        """Test subtracting negative values from memory."""
        self.calc.memory_add(10)
        self.calc.memory_subtract(-5)  # Subtracting -5 is like adding 5
        self.assertEqual(self.calc.get_memory_value(), 15)
    
    def test_memory_subtract_without_value_uses_last_result(self):
        """Test that memory_subtract without value uses last calculation result."""
        self.calc.memory_add(20)
        self.calc.multiply(3, 2)  # Result: 6
        self.calc.memory_subtract()  # Should subtract 6 from memory
        self.assertEqual(self.calc.get_memory_value(), 14)
    
    def test_memory_recall(self):
        """Test recalling memory value."""
        self.calc.memory_add(42)
        recalled = self.calc.memory_recall()
        self.assertEqual(recalled, 42)
        self.assertEqual(self.calc.get_memory_value(), 42)  # Memory unchanged
    
    def test_memory_clear(self):
        """Test clearing memory."""
        self.calc.memory_add(100)
        self.calc.memory_clear()
        self.assertEqual(self.calc.get_memory_value(), 0.0)
    
    def test_memory_persistence_during_session(self):
        """Test that memory persists across multiple operations."""
        self.calc.memory_add(10)
        self.calc.add(5, 3)  # Perform other operations
        self.calc.subtract(10, 2)
        self.calc.multiply(2, 3)
        # Memory should still be 10
        self.assertEqual(self.calc.get_memory_value(), 10)
    
    def test_memory_operations_in_history(self):
        """Test that memory operations are recorded in history."""
        self.calc.memory_add(15)
        self.calc.memory_subtract(5)
        self.calc.memory_recall()
        self.calc.memory_clear()
        
        history = self.calc.get_history()
        self.assertEqual(len(history), 4)
        self.assertIn("M+ 15", history[0])
        self.assertIn("M- 5", history[1])
        self.assertIn("MR", history[2])
        self.assertIn("MC", history[3])
    
    def test_memory_invalid_input_type(self):
        """Test memory functions with invalid input types."""
        with self.assertRaises(TypeError):
            self.calc.memory_add("ten")
        with self.assertRaises(TypeError):
            self.calc.memory_subtract("five")
    
    def test_complex_memory_sequence(self):
        """Test a complex sequence of memory operations."""
        # Start with some calculations
        self.calc.add(10, 5)  # 15
        self.calc.memory_add()  # Memory: 15
        
        self.calc.multiply(3, 4)  # 12
        self.calc.memory_add()  # Memory: 27
        
        self.calc.divide(100, 10)  # 10
        self.calc.memory_subtract()  # Memory: 17
        
        final_memory = self.calc.memory_recall()
        self.assertEqual(final_memory, 17)


class TestCalculatorHistory(unittest.TestCase):
    """Test suite for calculator history features."""
    
    def setUp(self):
        """Set up a fresh calculator instance for each test."""
        self.calc = Calculator(max_history=5)
    
    def test_initial_history_empty(self):
        """Test that history starts empty."""
        history = self.calc.get_history()
        self.assertEqual(len(history), 0)
    
    def test_history_stores_calculations(self):
        """Test that calculations are stored in history."""
        self.calc.add(5, 3)
        self.calc.subtract(10, 4)
        self.calc.multiply(3, 7)
        self.calc.divide(20, 5)
        
        history = self.calc.get_history()
        self.assertEqual(len(history), 4)
    
    def test_history_includes_timestamps(self):
        """Test that history entries include timestamps."""
        self.calc.add(5, 3)
        history = self.calc.get_history()
        
        # Check that timestamp is present in format [YYYY-MM-DD HH:MM:SS]
        self.assertIn("[", history[0])
        self.assertIn("]", history[0])
        # Check that the current year is in the timestamp
        current_year = str(datetime.now().year)
        self.assertIn(current_year, history[0])
    
    def test_history_max_limit(self):
        """Test that history respects maximum limit."""
        for i in range(10):
            self.calc.add(i, 1)
        
        history = self.calc.get_history()
        self.assertEqual(len(history), 5)  # Should only keep last 5
        
        # Verify it's the last 5 operations
        self.assertIn("5 + 1 = 6", history[0])
        self.assertIn("9 + 1 = 10", history[4])
    
    def test_clear_history(self):
        """Test clearing history."""
        self.calc.add(5, 3)
        self.calc.subtract(10, 4)
        self.calc.clear_history()
        
        history = self.calc.get_history()
        self.assertEqual(len(history), 0)
    
    def test_history_export_to_file(self):
        """Test exporting history to JSON file."""
        # Perform some calculations
        self.calc.add(10, 5)
        self.calc.multiply(3, 4)
        self.calc.divide(20, 5)
        
        # Export to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_filename = f.name
        
        try:
            # Export history
            success = self.calc.export_history(temp_filename)
            self.assertTrue(success)
            
            # Read and verify the exported file
            with open(temp_filename, 'r') as f:
                data = json.load(f)
            
            self.assertIn('export_time', data)
            self.assertIn('calculations', data)
            self.assertEqual(len(data['calculations']), 3)
            
        finally:
            # Clean up temp file
            import os
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
    
    def test_export_history_empty(self):
        """Test exporting empty history."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_filename = f.name
        
        try:
            success = self.calc.export_history(temp_filename)
            self.assertTrue(success)
            
            with open(temp_filename, 'r') as f:
                data = json.load(f)
            
            self.assertEqual(len(data['calculations']), 0)
            
        finally:
            import os
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
    
    def test_get_history_returns_copy(self):
        """Test that get_history returns a copy, not the original list."""
        self.calc.add(5, 3)
        history1 = self.calc.get_history()
        history1.append("fake entry")
        
        history2 = self.calc.get_history()
        self.assertEqual(len(history2), 1)  # Should still be 1, not 2
    
    def test_custom_max_history(self):
        """Test calculator with custom max_history value."""
        calc = Calculator(max_history=3)
        for i in range(5):
            calc.add(i, 1)
        
        history = calc.get_history()
        self.assertEqual(len(history), 3)
    
    def test_history_with_all_operation_types(self):
        """Test that all operation types are properly recorded in history."""
        self.calc.add(10, 5)
        self.calc.subtract(20, 8)
        self.calc.multiply(3, 4)
        self.calc.divide(15, 3)
        self.calc.memory_add(10)
        
        history = self.calc.get_history()
        
        # Check that each operation type is in history
        operations = ' '.join(history)
        self.assertIn('+', operations)
        self.assertIn('-', operations)
        self.assertIn('*', operations)
        self.assertIn('/', operations)
        self.assertIn('M+', operations)


class TestCalculatorIntegration(unittest.TestCase):
    """Integration tests for calculator functionality."""
    
    def setUp(self):
        """Set up a fresh calculator instance for each test."""
        self.calc = Calculator()
    
    def test_calculation_memory_history_integration(self):
        """Test integration of calculations, memory, and history."""
        # Perform calculation
        result = self.calc.add(15, 25)  # 40
        self.assertEqual(result, 40)
        
        # Store in memory
        self.calc.memory_add()  # Memory: 40
        self.assertEqual(self.calc.get_memory_value(), 40)
        
        # More calculations
        self.calc.multiply(5, 3)  # 15
        self.calc.memory_subtract()  # Memory: 25
        self.assertEqual(self.calc.get_memory_value(), 25)
        
        # Check history has all operations
        history = self.calc.get_history()
        self.assertEqual(len(history), 4)
        
        # Use memory in calculation
        memory_val = self.calc.memory_recall()
        result = self.calc.add(memory_val, 75)
        self.assertEqual(result, 100)
    
    def test_error_recovery(self):
        """Test that calculator recovers from errors properly."""
        # Cause an error
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10, 0)
        
        # Calculator should still work after error
        result = self.calc.add(5, 3)
        self.assertEqual(result, 8)
        
        # Memory should be unaffected
        self.calc.memory_add(10)
        self.assertEqual(self.calc.get_memory_value(), 10)
    
    def test_precision_in_complex_calculations(self):
        """Test precision in complex decimal calculations."""
        # Test that doesn't lose precision in chain calculations
        self.calc.add(0.1, 0.2)  # Known floating point issue
        self.calc.memory_add()
        
        result = self.calc.multiply(0.3, 3)
        self.assertAlmostEqual(result, 0.9, places=10)
        
        # Memory should maintain precision
        memory = self.calc.get_memory_value()
        self.assertAlmostEqual(memory, 0.3, places=10)


if __name__ == '__main__':
    unittest.main()