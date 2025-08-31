"""
Calculator Module
A comprehensive calculator with basic operations, memory functions, and history tracking.
"""

from typing import List, Optional, Union
from datetime import datetime
import json


class Calculator:
    """
    A calculator class that supports basic arithmetic operations,
    memory functions, and calculation history.
    
    Attributes:
        memory (float): The current value stored in memory
        history (List[str]): List of recent calculations (max 5)
        max_history (int): Maximum number of calculations to store in history
    """
    
    def __init__(self, max_history: int = 5):
        """
        Initialize the Calculator with empty memory and history.
        
        Args:
            max_history (int): Maximum number of calculations to store (default: 5)
        """
        self.memory: float = 0.0
        self.history: List[str] = []
        self.max_history: int = max_history
        self._last_result: Optional[float] = None
    
    # Basic Operations
    def add(self, a: Union[int, float], b: Union[int, float]) -> float:
        """
        Add two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            float: Sum of a and b
            
        Raises:
            TypeError: If inputs are not numeric
            OverflowError: If result is too large
        """
        try:
            result = float(a) + float(b)
            self._add_to_history(f"{a} + {b} = {result}")
            self._last_result = result
            return result
        except (TypeError, ValueError) as e:
            raise TypeError(f"Invalid input types for addition: {type(a)}, {type(b)}") from e
        except OverflowError as e:
            raise OverflowError("Result too large to compute") from e
    
    def subtract(self, a: Union[int, float], b: Union[int, float]) -> float:
        """
        Subtract b from a.
        
        Args:
            a: Number to subtract from
            b: Number to subtract
            
        Returns:
            float: Difference of a and b
            
        Raises:
            TypeError: If inputs are not numeric
        """
        try:
            result = float(a) - float(b)
            self._add_to_history(f"{a} - {b} = {result}")
            self._last_result = result
            return result
        except (TypeError, ValueError) as e:
            raise TypeError(f"Invalid input types for subtraction: {type(a)}, {type(b)}") from e
    
    def multiply(self, a: Union[int, float], b: Union[int, float]) -> float:
        """
        Multiply two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            float: Product of a and b
            
        Raises:
            TypeError: If inputs are not numeric
            OverflowError: If result is too large
        """
        try:
            result = float(a) * float(b)
            self._add_to_history(f"{a} * {b} = {result}")
            self._last_result = result
            return result
        except (TypeError, ValueError) as e:
            raise TypeError(f"Invalid input types for multiplication: {type(a)}, {type(b)}") from e
        except OverflowError as e:
            raise OverflowError("Result too large to compute") from e
    
    def divide(self, a: Union[int, float], b: Union[int, float]) -> float:
        """
        Divide a by b.
        
        Args:
            a: Dividend
            b: Divisor
            
        Returns:
            float: Quotient of a divided by b
            
        Raises:
            TypeError: If inputs are not numeric
            ZeroDivisionError: If b is zero
        """
        try:
            if float(b) == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            result = float(a) / float(b)
            self._add_to_history(f"{a} / {b} = {result}")
            self._last_result = result
            return result
        except (TypeError, ValueError) as e:
            raise TypeError(f"Invalid input types for division: {type(a)}, {type(b)}") from e
    
    # Memory Functions
    def memory_add(self, value: Optional[Union[int, float]] = None) -> None:
        """
        Add a value to memory (M+).
        
        Args:
            value: Value to add to memory. If None, uses last result.
            
        Raises:
            ValueError: If no value provided and no last result exists
        """
        if value is None:
            if self._last_result is None:
                raise ValueError("No value to add to memory")
            value = self._last_result
        
        try:
            self.memory += float(value)
            self._add_to_history(f"M+ {value} (Memory: {self.memory})")
        except (TypeError, ValueError) as e:
            raise TypeError(f"Invalid value for memory add: {value}") from e
    
    def memory_subtract(self, value: Optional[Union[int, float]] = None) -> None:
        """
        Subtract a value from memory (M-).
        
        Args:
            value: Value to subtract from memory. If None, uses last result.
            
        Raises:
            ValueError: If no value provided and no last result exists
        """
        if value is None:
            if self._last_result is None:
                raise ValueError("No value to subtract from memory")
            value = self._last_result
        
        try:
            self.memory -= float(value)
            self._add_to_history(f"M- {value} (Memory: {self.memory})")
        except (TypeError, ValueError) as e:
            raise TypeError(f"Invalid value for memory subtract: {value}") from e
    
    def memory_recall(self) -> float:
        """
        Recall the value stored in memory (MR).
        
        Returns:
            float: Current memory value
        """
        self._add_to_history(f"MR (Memory: {self.memory})")
        return self.memory
    
    def memory_clear(self) -> None:
        """
        Clear the memory (MC).
        """
        self.memory = 0.0
        self._add_to_history("MC (Memory cleared)")
    
    # History Functions
    def _add_to_history(self, entry: str) -> None:
        """
        Add an entry to the calculation history.
        
        Args:
            entry: String representation of the calculation
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamped_entry = f"[{timestamp}] {entry}"
        
        self.history.append(timestamped_entry)
        
        # Keep only the last max_history entries
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_history(self) -> List[str]:
        """
        Get the calculation history.
        
        Returns:
            List[str]: List of recent calculations with timestamps
        """
        return self.history.copy()
    
    def clear_history(self) -> None:
        """
        Clear the calculation history.
        """
        self.history = []
        print("History cleared")
    
    def display_history(self) -> None:
        """
        Display the calculation history in a formatted way.
        """
        if not self.history:
            print("No calculation history available")
            return
        
        print("\n" + "="*50)
        print("CALCULATION HISTORY")
        print("="*50)
        for i, entry in enumerate(self.history, 1):
            print(f"{i}. {entry}")
        print("="*50 + "\n")
    
    def export_history(self, filename: str = "history.json") -> bool:
        """
        Export calculation history to a JSON file.
        
        Args:
            filename: Name of the file to export to
            
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            with open(filename, 'w') as f:
                json.dump({
                    "export_time": datetime.now().isoformat(),
                    "calculations": self.history
                }, f, indent=2)
            print(f"History exported to {filename}")
            return True
        except Exception as e:
            print(f"Error exporting history: {e}")
            return False
    
    def get_memory_value(self) -> float:
        """
        Get the current memory value.
        
        Returns:
            float: Current value stored in memory
        """
        return self.memory


# Interactive CLI Interface
def main():
    """
    Main function to run the calculator in interactive mode.
    """
    calc = Calculator()
    
    print("\n" + "="*50)
    print("PYTHON CALCULATOR")
    print("="*50)
    print("\nCommands:")
    print("  Basic: add, sub, mul, div")
    print("  Memory: m+, m-, mr, mc")
    print("  History: history, clear_history, export")
    print("  Other: help, quit")
    print("\n" + "="*50 + "\n")
    
    while True:
        try:
            command = input("Enter command (or 'help'): ").strip().lower()
            
            if command == 'quit':
                print("Thank you for using the calculator!")
                break
            
            elif command == 'help':
                print("\nAvailable commands:")
                print("  add <a> <b> - Add two numbers")
                print("  sub <a> <b> - Subtract b from a")
                print("  mul <a> <b> - Multiply two numbers")
                print("  div <a> <b> - Divide a by b")
                print("  m+ [value] - Add to memory")
                print("  m- [value] - Subtract from memory")
                print("  mr - Recall memory")
                print("  mc - Clear memory")
                print("  history - Show calculation history")
                print("  clear_history - Clear history")
                print("  export - Export history to file")
                print("  quit - Exit calculator\n")
            
            elif command.startswith('add'):
                parts = command.split()
                if len(parts) != 3:
                    print("Usage: add <number1> <number2>")
                    continue
                result = calc.add(float(parts[1]), float(parts[2]))
                print(f"Result: {result}")
            
            elif command.startswith('sub'):
                parts = command.split()
                if len(parts) != 3:
                    print("Usage: sub <number1> <number2>")
                    continue
                result = calc.subtract(float(parts[1]), float(parts[2]))
                print(f"Result: {result}")
            
            elif command.startswith('mul'):
                parts = command.split()
                if len(parts) != 3:
                    print("Usage: mul <number1> <number2>")
                    continue
                result = calc.multiply(float(parts[1]), float(parts[2]))
                print(f"Result: {result}")
            
            elif command.startswith('div'):
                parts = command.split()
                if len(parts) != 3:
                    print("Usage: div <number1> <number2>")
                    continue
                result = calc.divide(float(parts[1]), float(parts[2]))
                print(f"Result: {result}")
            
            elif command.startswith('m+'):
                parts = command.split()
                if len(parts) > 1:
                    calc.memory_add(float(parts[1]))
                else:
                    calc.memory_add()
                print(f"Memory: {calc.get_memory_value()}")
            
            elif command.startswith('m-'):
                parts = command.split()
                if len(parts) > 1:
                    calc.memory_subtract(float(parts[1]))
                else:
                    calc.memory_subtract()
                print(f"Memory: {calc.get_memory_value()}")
            
            elif command == 'mr':
                print(f"Memory value: {calc.memory_recall()}")
            
            elif command == 'mc':
                calc.memory_clear()
                print("Memory cleared")
            
            elif command == 'history':
                calc.display_history()
            
            elif command == 'clear_history':
                calc.clear_history()
            
            elif command == 'export':
                calc.export_history()
            
            else:
                print(f"Unknown command: {command}. Type 'help' for available commands.")
        
        except ValueError as e:
            print(f"Error: Invalid number format - {e}")
        except ZeroDivisionError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()