#!/usr/bin/env python3
"""
API Response Bingo - Because guessing error formats is more fun than documentation!
"""

import json
import random
from typing import Dict, Any, List

class APIBingo:
    """
    Turns API error inconsistency into a fun game! 
    Collect all error formats to win absolutely nothing.
    """
    
    def __init__(self):
        # The bingo card of API sadness
        self.error_patterns = {
            "error": "message",  # Too obvious, rarely used
            "error_message": "string",  # Sometimes they're descriptive!
            "err": "msg",  # For the minimalists
            "message": "error",  # The classic switcheroo
            "status": "error",  # When HTTP codes aren't confusing enough
            "result": "failure",  # Optimistic naming for pessimistic outcomes
            "success": False,  # Boolean roulette
            "code": 500,  # Because who needs consistent error codes?
            "data": None,  # The "we have no idea what happened" special
            "details": "",  # Empty promises
            "trace": "stack",  # For when you want 1000 lines of Java in JSON
            "fault": {"faultstring": "string"},  # Inception errors
        }
        self.found_patterns = set()
    
    def check_response(self, response_data: Dict[str, Any]) -> List[str]:
        """
        Check which error patterns are present in the API response.
        Returns list of found patterns. BINGO when you get 5 in a row!
        """
        found = []
        
        for pattern, expected_type in self.error_patterns.items():
            if pattern in response_data:
                actual_value = response_data[pattern]
                
                # Type checking - because APIs love surprising us!
                if isinstance(expected_type, type):
                    if isinstance(actual_value, expected_type):
                        found.append(pattern)
                elif actual_value == expected_type:
                    found.append(pattern)
                
                # Special case: nested fault objects (looking at you, SOAP APIs)
                elif isinstance(expected_type, dict) and isinstance(actual_value, dict):
                    if "faultstring" in actual_value:
                        found.append(pattern)
        
        self.found_patterns.update(found)
        return found
    
    def get_score(self) -> int:
        """Return how many unique error patterns you've collected."""
        return len(self.found_patterns)
    
    def is_bingo(self) -> bool:
        """
        Check if you've won the API lottery!
        (Spoiler: Everyone loses when dealing with inconsistent APIs)
        """
        return self.get_score() >= 5
    
    def print_card(self):
        """Display your beautiful collection of API inconsistencies."""
        print("\n=== API BINGO CARD ===")
        print("Collected patterns:")
        for pattern in sorted(self.found_patterns):
            print(f"  ✓ {pattern}")
        print(f"\nScore: {self.get_score()}/12")
        if self.is_bingo():
            print("🎉 BINGO! You've mastered API inconsistency!")
        else:
            print("Keep trying! More inconsistent APIs await!")


def main():
    """Demo the tool with some "realistic" API responses."""
    bingo = APIBingo()
    
    # Sample API responses (because real APIs are too unpredictable)
    sample_responses = [
        {"error": "Invalid token", "code": 401},
        {"message": "Not found", "success": False},
        {"err": "Database timeout", "trace": "java.lang..."},
        {"status": "error", "details": "Missing parameter"},
        {"fault": {"faultstring": "Rate limit exceeded"}},
        {"result": "failure", "data": None},
    ]
    
    print("Playing API Response Bingo!\n")
    
    for i, response in enumerate(sample_responses, 1):
        print(f"Response {i}: {json.dumps(response)}")
        found = bingo.check_response(response)
        if found:
            print(f"Found: {', '.join(found)}")
        print()
    
    bingo.print_card()

if __name__ == "__main__":
    main()
