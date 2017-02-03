class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedList:
    def __init__(self, head=None):
        self.head = head

    def empty(self):
        if self.head:
            return False
        return True

    def printList(self):
        node = self.head
        while node:
            print(node.data, end="->")
            node = node.next
        print()

    def push(self, data):
        node = Node(data, next=self.head)
        self.head = node

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            node = self.head
            while node.next:
                node = node.next
            node.next = new_node
    
    def size(self):
        node = self.head
        i = 0
        while node:
            i += 1
            node = node.next 
        return i
    
    def delete(self, value):
        node = self.head
        while node:
            if node.next and node.next.data == value:
                node.next = node.next.next
                break
            node = node.next 
    
    def insert(self, index, value):
        if index == 0:
            self.push(value)
        else:
            new_node = Node(value)
            node = self.head
            i = 1
            while i < index and node:
                node = node.next
                i += 1
            if node:
                new_node.next = node.next
                node.next = new_node
    
    def deleteAtPosition(self, index):
        if index == 0:
            self.head = self.head.next
        else:
            node = self.head
            i = 1
            while i < index and node.next:
                node = node.next
                i += 1
            if node.next:
                node.next = node.next.next
    
    def value_at(self, index):
        node = self.head
        i = 0
        while i < index and node:
            node = node.next
            i += 1
        if node:
            return node.data
    
    def pop_front(self):
        if not self.empty():
            node = self.head
            self.head = self.head.next
        return node.data
    
    def pop_back(self):
        if not self.empty():
            node = self.head
            while node.next.next:
                node = node.next
            data = node.next.data
            node.next = None            
        return data  
    
    def front(self):
        if not self.empty():
            return self.head.data     
    
    def back(self):
        if not self.empty():
            node = self.head
            while node.next:
                node = node.next
            return node.data
    
    def reverse(self):
        if not self.empty():
            node = self.head
            i = 1
            while node.next:
                node = node.next
                self.push(node.data)
                self.deleteAtPosition(i+1)
                i += 1
                
    def value_n_from_end(self, n):
        s = self.size() - n
        if s >= 0 and n > 0:
            node = self.head
            i = 0
            while i < s:
                node = node.next
                i += 1
            return node.data
                
n3 = Node(3)
n2 = Node(2, next=n3)
n1 = Node(1, next=n2)

l = LinkedList(head=n1)
for i in [1,2,3,4,5,4,5,6,6,6,6,1,1,54,3]:
    l.append(i)
l.printList()

print('size:', l.size())
#l.delete(6)
#l.insert(5,999)
#l.deleteAtPosition(16)
#print(l.value_at(16))
#print(l.pop_front())
#print(l.pop_back())
#print(l.front())
#print(l.back())
n = 2
print(n, 'node from end:', l.value_n_from_end(n))
l.reverse()

l.printList()

