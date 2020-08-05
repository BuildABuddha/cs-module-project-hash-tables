class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        # Your code here
        self.capacity = capacity if capacity > MIN_CAPACITY else MIN_CAPACITY
        self.storage = [None] * self.capacity
        self.entries = 0


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return self.capacity


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        return self.entries / self.capacity


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit
        Implement this, and/or DJB2.
        """
        hval = 0x811c9dc5
        fnv_32_prime = 0x01000193
        uint32_max = 2 ** 32
        for s in key:
            hval = hval ^ ord(s)
            hval = (hval * fnv_32_prime) % uint32_max
        return hval


    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        # Your code here
        pass


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        return self.fnv1(key) % self.capacity
        # return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        key_index = self.hash_index(key)
        if self.storage[key_index] is None:
            self.storage[key_index] = HashTableEntry(key=key, value=value)
            self.entries += 1
        else:
            previous = self.storage[key_index]

            # Find a previous that either has a next of None or has the same key as our entry
            while previous.next is not None and previous.key != key:
                previous = previous.next

            # Store the entry if we don't have a duplicate key
            if previous.key != key:
                previous.next = HashTableEntry(key=key, value=value)
                self.entries += 1
            # Else, overwrite value.
            else:
                previous.value = value

        # Resize if load factor is too high
        if self.get_load_factor() > 0.7:
            self.resize(self.capacity * 2)

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        key_index = self.hash_index(key)

        # Check if any entries for this index exist yet.
        if self.storage[key_index] is not None:
            # Check if length of chain is 1.
            if self.storage[key_index].next is None:
                # If length is one and key matches, delete slot in storage.
                if self.storage[key_index].key == key:
                    self.storage[key_index] = None
                    self.entries -= 1
                else:
                    # Length is one but key is not found.
                    pass
            else:
                # Length is >1, search for key. 
                # Is it the head? If it is, change the head to the thing after it. 
                if self.storage[key_index].key == key:
                    self.storage[key_index] = self.storage[key_index].next
                # It's not the head so we'll have to search harder and 'snip' it out. 
                else:
                    previous_entry = self.storage[key_index]
                    current_entry = previous_entry.next

                    # Keep moving forward until we find either the end of the chain or a matching key.
                    while current_entry is not None:
                        if current_entry.key == key:
                            # We found it! Snip it out by adjusting 'next' values and break out of loop.
                            previous_entry.next = current_entry.next
                            self.entries -= 1
                            break
                        previous_entry = previous_entry.next
                        current_entry = current_entry.next

        # Resize if load factor is too low
        if self.get_load_factor() < 0.2 and self.capacity > MIN_CAPACITY:
            calculated_capacity = int(self.capacity / 2)
            new_capacity = MIN_CAPACITY if calculated_capacity < MIN_CAPACITY else calculated_capacity
            self.resize(new_capacity)


    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        key_index = self.hash_index(key)
        entry = self.storage[key_index]
        if entry is None:
            return None
        else:
            while entry is not None:
                if entry.key == key:
                    return entry.value
                entry = entry.next

            return None


    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        storage_copy = self.storage.copy()
        self.capacity = new_capacity
        self.storage = [None] * self.capacity
        self.entries = 0

        for entry in storage_copy:
            if entry is not None:
                # Loop through chain and add everything back in.
                while entry is not None:
                    self.put(entry.key, entry.value)
                    entry = entry.next




if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
