class Student(object):
    count = 0
    books = []
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.hobbies = ["table tenis"]
    pass

Student.books.extend(["python"[3].upper(), "javascript"])  
print "Student book list: %s" %Student.books    
# class can add class attribute after class defination
#Student.hobbies = ["reading", "jogging", "swimming"]
#print "Student hobby list: %s" %Student.hobbies    
print dir(Student)
 
print 
 
wilber = Student("Wilber", 28) 
print "%s is %d years old" %(wilber.name, wilber.age)   
# class instance can add new attribute 
# "gender" is the instance attribute only belongs to wilber
wilber.gender = "male"
print "%s is %s" %(wilber.name, wilber.gender)   
# class instance can access class attribute
print dir(wilber)
wilber.books.append("C#")
print wilber.books
print wilber.hobbies 
wilber.hobbies.append("play game") #why can't add the item in the self attrible 
#ilber.hobbies = "play cumputer game"
print wilber.hobbies
 
will = Student("Will", 27) 
print "%s is %d years old" %(will.name, will.age)   
# will shares the same class attribute with wilber
# will don't have the "gender" attribute that belongs to wilber
print dir(will)     
print will.books
print will.hobbies

print Student.__name__
print Student.__doc__
print Student.__bases__
print Student.__dict__
print Student.__module__
print Student.__class__

print "Student.count is wilber.count: ", Student.count is wilber.count
wilber.count = 1    
print "Student.count is wilber.count: ", Student.count is wilber.count
print Student.__dict__
print wilber.__dict__
del wilber.count
print "Student.count is wilber.count: ", Student.count is wilber.count
 
print 
 
wilber.count += 3    
print "Student.count is wilber.count: ", Student.count is wilber.count
print Student.__dict__
print wilber.__dict__
 
del wilber.count
print
 
print "Student.books is wilber.books: ", Student.books is wilber.books
wilber.books = ["C#", "Python"]
print "Student.books is wilber.books: ", Student.books is wilber.books
print Student.__dict__
print wilber.__dict__
del wilber.books
print "Student.books is wilber.books: ", Student.books is wilber.books
 
print 
 
wilber.books.append("CSS")
print "Student.books is wilber.books: ", Student.books is wilber.books
print Student.__dict__
print wilber.__dict__
