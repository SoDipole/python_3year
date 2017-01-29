class Stack:
    def __init__(self): 
        self.arr = []
    def push(self, item): 
        self.arr.append(item)
    def pop(self): 
        return self.arr.pop()
    def peek(self): 
        return self.arr[len(self.arr)-1]
    def isEmpty(self):
        if len(self.arr) == 0:
            return True
        else:
            return False
        
class MyQueue:
    def __init__(self):
        self.stack1 = Stack()
        self.stack2 = Stack()
        
    def push_1(self, item): 
        self.stack1.push(item)
    def push_2(self, item): 
        self.stack2.push(item)
    
    def pop_1(self): 
        return self.stack1.pop()
    def pop_2(self): 
        return self.stack2.pop()
    
    def peek_1(self): 
        return self.stack1.peek()
    def peek_2(self): 
        return self.stack2.peek()
    
    def isEmpty_1(self): 
        return self.stack1.isEmpty()
    def isEmpty_2(self): 
        return self.stack2.isEmpty()

    def transfer_1to2(self, n = ''):
        if n == '':
            n = len(self.stack1.arr)
        for i in range(n):
            self.push_2(self.pop_1())
    def transfer_2to1(self, n = ''):
        if n == '':
            n = len(self.stack2.arr)
        for i in range(n):
            self.push_1(self.pop_2())
            
items = [1,2,3,4,1,5]
        
my = MyQueue()
for i in range(len(items)):
    my.push_1(items[i])
    my.push_2(items[len(items)-i-1])
    print(my.stack1.arr, my.stack2.arr)
print('stacked')

my.transfer_2to1()
print(my.stack1.arr, my.stack2.arr)
my.transfer_1to2()
print(my.stack1.arr, my.stack2.arr)
my.transfer_2to1(6)
print(my.stack1.arr, my.stack2.arr)