class A():
    def some_number(self): return 5
    def pick_a_nice_number(self): return self.some_number() + 1

class B(A):
    def some_number(self): return 10
    def pick_a_nice_number(self): return self.some_number() + 2


print(
    B().pick_a_nice_number()    
)