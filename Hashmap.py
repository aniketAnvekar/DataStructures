class Hashmap:
    def __init__(self, capacity):
        self.capacity = capacity
        self.slots = [None]*self.capacity
        self.values = [None]*self.capacity
        self.size = 0
    
    def get_hash(self, key):
        return abs(hash(key)) % self.capacity

    def rehash(self, key):
        return (key+1) % self.capacity  # applying linear probing for rehash
    
    def insert(self, key, value):
        index = self.get_hash(key)
        
        if self.slots[index] == None:
            self.slots[index] = key
            self.values[index] = value
        else:
            if self.slots[index] == key:
                self.values[index] = value
            else:
                new_index = self.rehash(index)
                
                while(self.slots[new_index] != None and self.slots[new_index] != key):
                    new_index = self.rehash(new_index)

                if self.slots[new_index] == None:
                    self.slots[new_index] = key
                    self.values[new_index] = value
                else:
                    self.values[new_index] = value
        
    def get(self, key):
        index = self.get_hash(key)
        initial_index = index
        while(self.slots[index] != None):
            if self.slots[index] == key:
                return self.values[index]
            
            index = self.rehash(index)
            
            if index == initial_index:
                return "Not found (Traversed entire list)"
        return "Key doesn't exist"

    def delete(self, key):
        index = self.get_hash(key)
        while(self.slots[index] != None):
            if self.slots[index] == key:
                self.slots[index] = None
                self.values[index] = None
                return "Key has been deleted"
            
            new_index = self.rehash(key)
            
            if new_index == index:
                break
            
        return "Key not found"
    
    def __setitem__(self,key,value):
        return self.insert(key,value)
    
    def __getitem__(self,key):
        return self.get(key)
    
    def __str__(self):
        result = {}
        for i in range(self.capacity):
            if self.slots[i] != None and self.values[i] != None:
                result[self.slots[i]] = self.values[i]
        return str(result)
    
hmap = Hashmap(5)
hmap.insert("orange", 10)
hmap.insert("apple", 15)
# print(hmap.delete("pineapple"))
print(hmap)