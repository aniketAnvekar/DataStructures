"""
Custom Hashmap Implementation with Linear Probing
=================================================

This module implements a hash table (hashmap) data structure using:
- Open addressing with linear probing for collision resolution
- Dynamic key-value pair storage
- Python magic methods for dictionary-like behavior

Author: Aniket Anvekar
"""

class Hashmap:
    """
    A hash table implementation using linear probing for collision resolution.
    
    This class provides O(1) average time complexity for insertion, deletion,
    and lookup operations. Uses two parallel arrays to store keys and values.
    
    Attributes:
        capacity (int): Maximum number of slots in the hash table
        slots (list): Array storing keys (None for empty slots)
        values (list): Array storing values corresponding to keys
        size (int): Current number of key-value pairs stored
    """
    
    def __init__(self, capacity):
        """
        Initialize the hashmap with a given capacity.
        
        Args:
            capacity (int): Maximum number of elements the hashmap can hold
            
        Time Complexity: O(n) where n is capacity
        Space Complexity: O(n)
        """
        self.capacity = capacity                    # Set maximum size
        self.slots = [None] * self.capacity        # Initialize key storage
        self.values = [None] * self.capacity       # Initialize value storage
        self.size = 0                              # Track current number of elements
    
    def get_hash(self, key):
        """
        Calculate the hash index for a given key.
        
        Uses Python's built-in hash() function and modulo operation
        to map keys to valid array indices.
        
        Args:
            key: The key to hash (must be hashable)
            
        Returns:
            int: Index in the range [0, capacity-1]
            
        Time Complexity: O(1)
        """
        return abs(hash(key)) % self.capacity

    def rehash(self, index):
        """
        Calculate the next index for linear probing collision resolution.
        
        When a collision occurs, this method finds the next available slot
        by incrementing the index (with wraparound).
        
        Args:
            index (int): Current index that caused collision
            
        Returns:
            int: Next index to probe
            
        Time Complexity: O(1)
        """
        return (index + 1) % self.capacity  # Linear probing: move to next slot
    
    def insert(self, key, value):
        """
        Insert or update a key-value pair in the hashmap.
        
        If the key already exists, updates its value.
        If collision occurs, uses linear probing to find next available slot.
        
        Args:
            key: The key to insert/update (must be hashable)
            value: The value to associate with the key
            
        Time Complexity: O(1) average, O(n) worst case
        Space Complexity: O(1)
        """
        index = self.get_hash(key)              # Get initial hash index
        
        # Case 1: Slot is empty - direct insertion
        if self.slots[index] == None:
            self.slots[index] = key
            self.values[index] = value
            self.size += 1                      # Increment size for new key
        else:
            # Case 2: Key already exists - update value
            if self.slots[index] == key:
                self.values[index] = value      # Update existing key's value
            else:
                # Case 3: Collision occurred - use linear probing
                new_index = self.rehash(index)
                
                # Find next available slot or matching key
                while(self.slots[new_index] != None and self.slots[new_index] != key):
                    new_index = self.rehash(new_index)

                # Insert new key or update existing key
                if self.slots[new_index] == None:
                    self.slots[new_index] = key
                    self.values[new_index] = value
                    self.size += 1              # Increment size for new key
                else:
                    self.values[new_index] = value  # Update existing key
        
    def get(self, key):
        """
        Retrieve the value associated with a given key.
        
        Uses linear probing to handle collisions during lookup.
        
        Args:
            key: The key to search for
            
        Returns:
            The value associated with the key, or error message if not found
            
        Time Complexity: O(1) average, O(n) worst case
        """
        index = self.get_hash(key)              # Get initial hash index
        initial_index = index                   # Remember starting position
        
        # Search through slots until key is found or we've checked all slots
        while(self.slots[index] != None):
            # Key found - return corresponding value
            if self.slots[index] == key:
                return self.values[index]
            
            # Move to next slot using linear probing
            index = self.rehash(index)
            
            # If we've come full circle, key doesn't exist
            if index == initial_index:
                return "Not found (Traversed entire list)"
                
        # Reached empty slot - key doesn't exist
        return "Key doesn't exist"

    def delete(self, key):
        """
        Remove a key-value pair from the hashmap.
        
        WARNING: This implementation has a bug - it should be rehash(index)
        instead of rehash(key) in the loop.
        
        Args:
            key: The key to delete
            
        Returns:
            str: Success or failure message
            
        Time Complexity: O(1) average, O(n) worst case
        """
        index = self.get_hash(key)              # Get initial hash index
        
        # Search for the key to delete
        while(self.slots[index] != None):
            # Key found - delete it
            if self.slots[index] == key:
                self.slots[index] = None
                self.values[index] = None
                self.size -= 1                  # Decrement size
                return "Key has been deleted"
            
            # BUG: Should be rehash(index), not rehash(key)
            new_index = self.rehash(key)        # This line has an error!
            
            # Prevent infinite loop
            if new_index == index:
                break
            
        return "Key not found"
    
    def __setitem__(self, key, value):
        """
        Magic method to enable dictionary-style assignment: hmap[key] = value
        
        Args:
            key: The key to insert/update
            value: The value to associate with the key
            
        Example:
            hmap["apple"] = 10  # Calls hmap.__setitem__("apple", 10)
        """
        return self.insert(key, value)
    
    def __getitem__(self, key):
        """
        Magic method to enable dictionary-style access: value = hmap[key]
        
        Args:
            key: The key to retrieve
            
        Returns:
            The value associated with the key
            
        Example:
            value = hmap["apple"]  # Calls hmap.__getitem__("apple")
        """
        return self.get(key)
    
    def __str__(self):
        """
        Magic method to provide string representation of the hashmap.
        
        Returns a dictionary-like string showing all key-value pairs.
        
        Returns:
            str: String representation of the hashmap
            
        Example:
            print(hmap)  # Calls hmap.__str__()
        """
        result = {}
        
        # Iterate through all slots and collect non-empty key-value pairs
        for i in range(self.capacity):
            if self.slots[i] != None and self.values[i] != None:
                result[self.slots[i]] = self.values[i]
                
        return str(result)

# ============================================================================
# DEMONSTRATION AND TESTING
# ============================================================================

# Create a hashmap with capacity of 5 slots
hmap = Hashmap(5)

# Insert key-value pairs
hmap.insert("orange", 10)    # Direct insertion
hmap.insert("apple", 15)     # May cause collision depending on hash values

# Test string representation
print("Current hashmap contents:")
print(hmap)

# Test dictionary-style operations (magic methods)
print(f"\nUsing dictionary-style access:")
print(f"hmap['orange'] = {hmap['orange']}")

# Uncomment to test deletion (note: has a bug)
# print(f"\nDeleting 'pineapple': {hmap.delete('pineapple')}")

# Test retrieval of non-existent key
print(f"\nTrying to get non-existent key:")
print(f"hmap.get('banana') = {hmap.get('banana')}")