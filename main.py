from pyswip import *
import re

# Create a Prolog object
prolog = Prolog()

assertz = Functor("assertz", 1)
parent = Functor("parent", 2)
sibling = Functor("sibling", 2)
brother = Functor("brother", 2)
sister = Functor("sister", 2)
father = Functor("father", 2)
mother = Functor("mother", 2)
grandmother = Functor("grandmother", 2) 
grandfather = Functor("grandfather", 2)
child = Functor("child", 2)
daughter = Functor("daughter", 2)
son = Functor("son", 2) 
uncle = Functor("uncle", 2)
aunt = Functor("aunt", 2)
relative = Functor("relative", 2)
male = Functor("male", 1) 
female = Functor("female", 1)
grandchild = Functor("grandchild", 2) 


def add_fact(fact):
    try:
        call(assertz(fact))  # Call assertz to add the fact
    except Exception as e:
        print(f"Error: Could not add fact - {e}")


def infer_sibling_relationships(x, y):
    X = Variable()
    # Query siblings of x
    q_x = Query(sibling(x, X))
    siblings_of_x = []
    while q_x.nextSolution():
        siblings_of_x.append(str(X.value))
    q_x.closeQuery()

    # Query siblings of y
    q_y = Query(sibling(y, X))
    siblings_of_y = []
    while q_y.nextSolution():
        siblings_of_y.append(str(X.value))
    q_y.closeQuery()

    # Add inferred relationships
    for s in siblings_of_x:
        if s != y:
            add_fact(sibling(s, y))
            add_fact(sibling(y, s))
    for s in siblings_of_y:
        if s != x:
            add_fact(sibling(s, x))
            add_fact(sibling(x, s))

def infer_relative_relationships(x, y):
    X = Variable()

    # Query relatives of x
    q_x = Query(relative(x, X))
    relatives_of_x = set()
    while q_x.nextSolution():
        relatives_of_x.add(str(X.value))
    q_x.closeQuery()

    # Query relatives of y
    q_y = Query(relative(y, X))
    relatives_of_y = set()
    while q_y.nextSolution():
        relatives_of_y.add(str(X.value))
    q_y.closeQuery()

    for r in relatives_of_x:
        if r != y:
            add_fact(relative(r, y))
            add_fact(relative(y, r))

    for r in relatives_of_y:
        if r != x:
            add_fact(relative(r, x))
            add_fact(relative(x, r))

def process_statement(statement):
    if re.match(r"([A-Z][a-z]+) and ([A-Z][a-z]+) are siblings\.", statement):
        match = re.match(r"([A-Z][a-z]+) and ([A-Z][a-z]+) are siblings\.", statement)
        x, y = match.groups()

        if x.lower() == y.lower():
            print("That's impossible!")
        else:
            add_fact(sibling(x.lower(), y.lower()))
            add_fact(sibling(y.lower(), x.lower()))
            add_fact(relative(x.lower(), y.lower()))
            add_fact(relative(y.lower(), x.lower()))
            infer_sibling_relationships(x.lower(), y.lower())
            infer_relative_relationships(x.lower(), y.lower())
            print("OK! I learned something.")
    
    elif re.match(r"([A-Z][a-z]+) is a brother of ([A-Z][a-z]+)\.", statement):
        match = re.match(r"([A-Z][a-z]+) is a brother of ([A-Z][a-z]+)\.", statement)
        x, y = match.groups()
        q = Query(female(x.lower()))

        if x.lower() == y.lower() or q.nextSolution():
            print("That's impossible!")
        else:
            add_fact(male(x.lower()))
            add_fact(brother(x.lower(), y.lower()))
            add_fact(sibling(x.lower(), y.lower()))
            add_fact(sibling(y.lower(), x.lower()))
            add_fact(relative(x.lower(), y.lower()))
            add_fact(relative(y.lower(), x.lower()))
            infer_sibling_relationships(x.lower(), y.lower())
            infer_relative_relationships(x.lower(), y.lower())
            print("OK! I learned something.")
        q.closeQuery
    
    elif re.match(r"([A-Z][a-z]+) is a sister of ([A-Z][a-z]+)\.", statement):
        match = re.match(r"([A-Z][a-z]+) is a sister of ([A-Z][a-z]+)\.", statement)
        x, y = match.groups()
        q = Query(male(x.lower()))
        
        if x.lower() == y.lower() or q.nextSolution():
            print("That's impossible!")
        else:
            add_fact(female(x.lower()))
            add_fact(sister(x.lower(), y.lower()))
            add_fact(sibling(x.lower(), y.lower()))
            add_fact(sibling(y.lower(), x.lower()))
            add_fact(relative(x.lower(), y.lower()))
            add_fact(relative(y.lower(), x.lower()))
            infer_sibling_relationships(x.lower(), y.lower())
            infer_relative_relationships(x.lower(), y.lower())
            print("OK! I learned something.")
        q.closeQuery
    
    elif re.match(r"([A-Z][a-z]+) is the father of ([A-Z][a-z]+)\.", statement):
        match = re.match(r"([A-Z][a-z]+) is the father of ([A-Z][a-z]+)\.", statement)
        x, y = match.groups()
        q = Query(female(x.lower()))

        if x.lower() == y.lower() or q.nextSolution():
            print("That's impossible!")
        else:
            add_fact(father(x.lower(), y.lower())) # x is the father of y
            add_fact(parent(x.lower(), y.lower())) # x is the parent of y
            add_fact(male(x.lower())) # x is a male
            add_fact(child(y.lower(), x.lower())) # y is the child of x
            add_fact(relative(x.lower(), y.lower()))
            add_fact(relative(y.lower(), x.lower()))
            infer_relative_relationships(x.lower(), y.lower())
            print("OK! I learned something.")
        q.closeQuery
    
    elif re.match(r"([A-Z][a-z]+) is the mother of ([A-Z][a-z]+)\.", statement):
        match = re.match(r"([A-Z][a-z]+) is the mother of ([A-Z][a-z]+)\.", statement)
        x, y = match.groups()
        q = Query(male(x.lower()))

        if x.lower() == y.lower() or q.nextSolution():
            print("That's impossible!")
        else:
            add_fact(mother(x.lower(), y.lower())) # x is the mother of y
            add_fact(parent(x.lower(), y.lower())) # x is the parent of y
            add_fact(female(x.lower())) # x is a female
            add_fact(child(y.lower(), x.lower())) # y is the child of x
            add_fact(relative(x.lower(), y.lower()))
            add_fact(relative(y.lower(), x.lower()))
            infer_relative_relationships(x.lower(), y.lower())
            print("OK! I learned something.")
        q.closeQuery

    elif (match := re.match(r"([A-Z][a-z]+) is a child of ([A-Z][a-z]+)\.", statement)):
        x, y = match.groups()

        if x.lower() == y.lower():
            print("That's impossible!")
        else:
            add_fact(child(x.lower(), y.lower()))  # x is a child of y
            add_fact(parent(y.lower(), x.lower()))  # y is the parent of x
            add_fact(relative(x.lower(), y.lower()))
            add_fact(relative(y.lower(), x.lower()))
            infer_relative_relationships(x.lower(), y.lower())
            print("OK! I learned something.")

    elif (match := re.match(r"([A-Z][a-z]+) and ([A-Z][a-z]+) are the parents of ([A-Z][a-z]+)\.", statement)):
        x, y, z = match.groups()  
        
        if x.lower() == y.lower():
            print("That's impossible!")
        else:
            add_fact(parent(x.lower(), z.lower()))  # x is a parent of z
            add_fact(parent(y.lower(), z.lower()))  # y is a parent of z
            add_fact(child(z.lower(), x.lower())) # z is a child of x
            add_fact(child(z.lower(), y.lower())) # z is a child of y
            add_fact(relative(x.lower(), y.lower()))
            add_fact(relative(y.lower(), x.lower()))
            infer_relative_relationships(x.lower(), y.lower())
            print("OK! I learned something.")
     
    elif (match := re.match(r"([A-Z][a-z]+) is a grandmother of ([A-Z][a-z]+)\.", statement)):
        x, y = match.groups()  
        q = Query(male(x.lower()))

        if x.lower() == y.lower() or q.nextSolution():
            print("That's impossible!")
        else:
            add_fact(female(x.lower())) # X is a female
            add_fact(grandmother(x.lower(), y.lower()))  # x is the grandmother of y
            add_fact(grandchild(y.lower(), x.lower())) # y is a grandchild of x
            add_fact(relative(x.lower(), y.lower()))
            add_fact(relative(y.lower(), x.lower()))
            infer_relative_relationships(x.lower(), y.lower())
            print("OK! I learned something.")
        q.closeQuery
    
    elif (match := re.match(r"([A-Z][a-z]+) is a grandfather of ([A-Z][a-z]+)\.", statement)):
        x, y = match.groups()  
        q = Query(female(x.lower()))

        if x.lower() == y.lower() or q.nextSolution():
            print("That's impossible!")
        else:
            add_fact(male(x.lower())) # X is a male
            add_fact(grandfather(x.lower(), y.lower()))  # x is the grandfather of y 
            add_fact(grandchild(y.lower(), x.lower()))  # y is a grandchild of x
            add_fact(relative(x.lower(), y.lower()))
            add_fact(relative(y.lower(), x.lower()))
            infer_relative_relationships(x.lower(), y.lower())
            print("OK! I learned something.")
        q.closeQuery
    
    elif (match := re.match(r"([A-Z][a-z]+) is a daughter of ([A-Z][a-z]+)\.", statement)):
        x, y = match.groups()  
        q = Query(male(x.lower()))

        if x.lower() == y.lower() or q.nextSolution():
            print("That's impossible!")
        else:
            add_fact(female(x.lower())) # x is a female
            add_fact(daughter(x.lower(), y.lower()))  # x is a daughter of y 
            add_fact(parent(y.lower(), x.lower()))  # y is the parent of x
            add_fact(child(x.lower(), y.lower())) # x is a child of y
            add_fact(relative(x.lower(), y.lower()))
            add_fact(relative(y.lower(), x.lower()))
            infer_relative_relationships(x.lower(), y.lower())
            print("OK! I learned something.")
        q.closeQuery
    
    elif (match := re.match(r"([A-Z][a-z]+) is a son of ([A-Z][a-z]+)\.", statement)):
        x, y = match.groups()  
        q = Query(female(x.lower()))

        if x.lower() == y.lower() or q.nextSolution():
            print("That's impossible!")
        else:
            add_fact(male(x.lower())) # x is a male
            add_fact(son(x.lower(), y.lower()))  # x is a son of y 
            add_fact(parent(y.lower(), x.lower()))  # y is the parent of x
            add_fact(child(x.lower(), y.lower())) # x is a child of y
            add_fact(relative(x.lower(), y.lower()))
            add_fact(relative(y.lower(), x.lower()))
            infer_relative_relationships(x.lower(), y.lower())
            print("OK! I learned something.")
        q.closeQuery
    
    elif (match := re.match(r"([A-Z][a-z]+), ([A-Z][a-z]+) and ([A-Z][a-z]+) are children of ([A-Z][a-z]+)\.", statement)):  # Andrei, Zia and Zandre are children of Lizdrei.
        x, y, z, p = match.groups()  

        if p.lower() in {x.lower(), y.lower(), z.lower()} or len({x.lower(), y.lower(), z.lower()}) < 3:
            print("That’s impossible!")
        else:
            add_fact(parent(p.lower(), x.lower())) # p is a parent of x  
            add_fact(parent(p.lower(), y.lower())) # p is a parent of y
            add_fact(parent(p.lower(), z.lower())) # p is a parent of z
            add_fact(child(x.lower(), p.lower())) # is a child of p
            add_fact(child(y.lower(), p.lower())) # is a child of p
            add_fact(child(z.lower(), p.lower())) # is a child of p
            
            add_fact(sibling(x.lower(), y.lower()))  # x is a sibling of y
            add_fact(sibling(y.lower(), x.lower()))  # y is a sibling of x  
            add_fact(sibling(x.lower(), z.lower()))  # x is a sibling of z 
            add_fact(sibling(z.lower(), x.lower()))  # z is a sibling of x  
            add_fact(sibling(y.lower(), z.lower()))  # y is a sibling of z 
            add_fact(sibling(z.lower(), y.lower()))  # z is a sibling of y  

            add_fact(relative(x.lower(), y.lower()))
            add_fact(relative(y.lower(), z.lower()))
            add_fact(relative(z.lower(), p.lower()))
            add_fact(relative(p.lower(), x.lower()))
            add_fact(relative(x.lower(), z.lower()))
            add_fact(relative(z.lower(), y.lower()))
            add_fact(relative(y.lower(), p.lower()))
            add_fact(relative(p.lower(), z.lower()))
            add_fact(relative(x.lower(), p.lower()))
            add_fact(relative(p.lower(), y.lower()))
            add_fact(relative(y.lower(), x.lower()))
            add_fact(relative(z.lower(), x.lower()))

            infer_relative_relationships(x.lower(), y.lower())
            print("OK! I learned something.")
    
    elif (match := re.match(r"([A-Z][a-z]+) is an uncle of ([A-Z][a-z]+)\.", statement)):
        x, y = match.groups()  
        q = Query(female(x.lower()))

        if x.lower() == y.lower() or q.nextSolution():
            print("That's impossible!")
        else:
            add_fact(male(x.lower())) # x is a male
            add_fact(uncle(x.lower(), y.lower())) # x is an uncle of y
            add_fact(relative(x.lower(), y.lower()))
            add_fact(relative(y.lower(), x.lower()))
            infer_relative_relationships(x.lower(), y.lower())
            print("OK! I learned something.")
        q.closeQuery
    
    elif (match := re.match(r"([A-Z][a-z]+) is an aunt of ([A-Z][a-z]+)\.", statement)):
        x, y = match.groups()  
        q = Query(male(x.lower()))

        if x.lower() == y.lower() or q.nextSolution():
            print("That's impossible!")
        else:
            add_fact(female(x.lower())) # x is a female
            add_fact(aunt(x.lower(), y.lower())) # x is an aunt of y
            add_fact(relative(x.lower(), y.lower()))
            add_fact(relative(y.lower(), x.lower()))
            infer_relative_relationships(x.lower(), y.lower())
            print("OK! I learned something.")
        q.closeQuery
    
    else:
        print("Statement not recognized.")

def process_question(question):
    X = Variable()
    
    if re.match(r"Are ([A-Z][a-z]+) and ([A-Z][a-z]+) siblings\?", question):
        match = re.match(r"Are ([A-Z][a-z]+) and ([A-Z][a-z]+) siblings\?", question)
        x, y = match.groups()
        q = Query(sibling(x.lower(), y.lower()))
        print("Yes" if q.nextSolution() else "No")
        q.closeQuery()

    elif re.match(r"Who are the siblings of ([A-Z][a-z]+)\?", question):
        match = re.match(r"Who are the siblings of ([A-Z][a-z]+)\?", question)
        x = match.group(1)
        q = Query(sibling(x.lower(), X))
        siblings = []
        while q.nextSolution():
            siblings.append(str(X.value).capitalize())
        q.closeQuery()
        print("Siblings of", x, ":", ", ".join(siblings) if siblings else "None")

    elif re.match(r"Is ([A-Z][a-z]+) a brother of ([A-Z][a-z]+)\?", question):
        match = re.match(r"Is ([A-Z][a-z]+) a brother of ([A-Z][a-z]+)\?", question)
        x, y = match.groups()
        q = Query(brother(x.lower(), y.lower()))
        print("Yes" if q.nextSolution() else "No")
        q.closeQuery()

    elif re.match(r"Who are the brothers of ([A-Z][a-z]+)\?", question):
        # Question format: Who are the brothers of x?
        match = re.match(r"Who are the brothers of ([A-Z][a-z]+)\?", question)
        x = match.group(1)
        q = Query(brother(X, x.lower()))
        brothers = []
        while q.nextSolution():
            brothers.append(str(X.value).capitalize())
        q.closeQuery()
        print("Brothers of", x, ":", ", ".join(brothers) if brothers else "None")
    
    elif re.match(r"Is ([A-Z][a-z]+) the mother of ([A-Z][a-z]+)\?", question):
        match = re.match(r"Is ([A-Z][a-z]+) the mother of ([A-Z][a-z]+)\?", question)
        x, y = match.groups()
        q = Query(mother(x.lower(), y.lower())) # x is the mother of y
        print("Yes" if q.nextSolution() else "No")
        q.closeQuery()

    elif re.match(r"Is ([A-Z][a-z]+) a sister of ([A-Z][a-z]+)\?", question):
        match = re.match(r"Is ([A-Z][a-z]+) a sister of ([A-Z][a-z]+)\?", question)
        x, y = match.groups()
        q = Query(sister(x.lower(), y.lower()))
        print("Yes" if q.nextSolution() else "No")
        q.closeQuery()

    elif re.match(r"Who are the sisters of ([A-Z][a-z]+)\?", question):
        # Question format: Who are the sisters of x?
        match = re.match(r"Who are the sisters of ([A-Z][a-z]+)\?", question)
        x = match.group(1)
        q = Query(sister(X, x.lower()))
        sisters = []
        while q.nextSolution():
            sisters.append(str(X.value).capitalize())
        q.closeQuery()
        print("Brothers of", x, ":", ", ".join(sisters) if sisters else "None")
    
    elif (match := re.match(r"Who is the mother of ([A-Z][a-z]+)\?", question)): # test
        x = match.group(1)
        Y = Variable() 
        q = Query(mother(Y, x.lower()))  
        if q.nextSolution():  
            mother_name = str(Y.get_value())
            print(f"The mother of {x} is {mother_name.capitalize()}.")
        else:
            print(f"No mother found for {x}.")
        q.closeQuery()

    elif (match := re.match(r"Who is the father of ([A-Z][a-z]+)\?", question)): # test
        x = match.group(1)
        Y = Variable() 
        q = Query(father(Y, x.lower()))  
        if q.nextSolution():  
            father_name = str(Y.get_value()); 
            print(f"The father of {x} is {father_name.capitalize()}.")
        else:
            print(f"No father found for {x}.")
        q.closeQuery()
    
    elif re.match(r"Is ([A-Z][a-z]+) the father of ([A-Z][a-z]+)\?", question):
        match = re.match(r"Is ([A-Z][a-z]+) the father of ([A-Z][a-z]+)\?", question)
        x, y = match.groups()
        q = Query(father(x.lower(), y.lower()))
        print("Yes" if q.nextSolution() else "No")
        q.closeQuery()
    
    elif (match := re.match(r"Is ([A-Z][a-z]+) a child of ([A-Z][a-z]+)\?", question)):
        x, y = match.groups()  
        q = Query(child(x.lower(), y.lower()))  # x is a child of y
        print("Yes" if q.nextSolution() else "No")
        q.closeQuery()
   
    elif (match := re.match(r"Is ([A-Z][a-z]+) a male\?", question)): # extra
        x = match.group(1)  
        q = Query(male(x.lower()))  
        print("Yes" if q.nextSolution() else "No")
        q.closeQuery()

    elif (match := re.match(r"Is ([A-Z][a-z]+) a female\?", question)): # extra
        x = match.group(1)  
        q = Query(female(x.lower())) 
        print("Yes" if q.nextSolution() else "No")
        q.closeQuery()
    
    elif (match := re.match(r"Are ([A-Z][a-z]+) and ([A-Z][a-z]+) the parents of ([A-Z][a-z]+)\?", question)):
        x, y, z = match.groups()
        try:
            q1 = Query(parent(x.lower(), z.lower()))
            solution1 = q1.nextSolution()
            solution1 = int(solution1)
            q1.closeQuery()

            q2 = Query(parent(y.lower(), z.lower()))
            solution2 = q2.nextSolution()
            solution2 = int(solution2)
            q2.closeQuery()

            if (solution1 == 1 and solution2 == solution1):
                print("Yes")
            elif (solution1 == 1 and solution2 == 0):
                print(f"Only {x} is the parent of {z}")
            elif (solution1 == 0 and solution2 == 1):
                print(f"Only {y} is the parent of {z}")
            else:
                print("No")    
        except Exception as e: 
            print(f"Error message: {e}")
    
    elif (match := re.match(r"Is ([A-Z][a-z]+) a grandmother of ([A-Z][a-z]+)\?", question)): 
        x, y = match.groups()  
        Y = Variable()

        q1 = Query(grandmother(x.lower(), y.lower())) 
        result1 = q1.nextSolution()
        q1.closeQuery()

        q2a = Query(mother(x.lower(), Y)) 
        result2a = q2a.nextSolution()
        q2a.closeQuery()

        q2b = Query(parent(Y, y.lower())) 
        result2b = q2b.nextSolution()
        q2b.closeQuery()

        result2 = result2a and result2b

        print("Yes" if result1 or result2 else "No")
    
    elif (match := re.match(r"Is ([A-Z][a-z]+) a grandfather of ([A-Z][a-z]+)\?", question)): 
        x, y = match.groups()  
        Y = Variable()

        q1 = Query(grandfather(x.lower(), y.lower())) 
        result1 = q1.nextSolution()
        q1.closeQuery()

        q2a = Query(father(x.lower(), Y)) 
        result2a = q2a.nextSolution()
        q2a.closeQuery()

        q2b = Query(parent(Y, y.lower())) 
        result2b = q2b.nextSolution()
        q2b.closeQuery()

        result2 = result2a and result2b

        print("Yes" if result1 or result2 else "No")
        
    elif (match := re.match(r"Is ([A-Z][a-z]+) a daughter of ([A-Z][a-z]+)\?", question)): 
        x, y = match.groups()  
        q = Query(daughter(x.lower(), y.lower())) 
        print("Yes" if q.nextSolution() else "No")
        q.closeQuery()
    
    elif (match := re.match(r"Is ([A-Z][a-z]+) a son of ([A-Z][a-z]+)\?", question)): 
        x, y = match.groups()  
        q = Query(son(x.lower(), y.lower())) 
        print("Yes" if q.nextSolution() else "No")
        q.closeQuery()

    elif (match := re.match(r"Are ([A-Z][a-z]+), ([A-Z][a-z]+) and ([A-Z][a-z]+) children of ([A-Z][a-z]+)\?", question)):
        x, y, z, a = match.groups() 
        
        q1 =  Query(child(x.lower(), a.lower()))
        sol1 = q1.nextSolution()
        sol1 = int(sol1)
        q1.closeQuery()
        
        q2 = Query(child(y.lower(), a.lower()))
        sol2 = q2.nextSolution()
        sol2 = int(sol2)
        q2.closeQuery()
        
        q = Query(child(z.lower(), a.lower()))
        sol3 = q.nextSolution()
        sol3 = int(sol3)
        q.closeQuery()
        if (sol1 == 1 and sol2 == 1 and sol3 == 1):
            print("Yes")
        else:
            print("No")
    
    elif (match := re.match(r"Is ([A-Z][a-z]+) an uncle of ([A-Z][a-z]+)\?", question)): 
        x, y = match.groups()  
        Y = Variable()

        q1 = Query(uncle(x.lower(), y.lower())) 
        result1 = q1.nextSolution()
        q1.closeQuery()

        q2a = Query(brother(x.lower(), Y)) 
        result2a = q2a.nextSolution()
        q2a.closeQuery()

        q2b = Query(parent(Y, y.lower())) 
        result2b = q2b.nextSolution()
        q2b.closeQuery()

        result2 = result2a and result2b

        print("Yes" if result1 or result2 else "No")
        
    elif (match := re.match(r"Is ([A-Z][a-z]+) an aunt of ([A-Z][a-z]+)\?", question)): 
        x, y = match.groups()  
        Y = Variable()

        q1 = Query(aunt(x.lower(), y.lower())) 
        result1 = q1.nextSolution()
        q1.closeQuery()

        q2a = Query(sister(x.lower(), Y)) 
        result2a = q2a.nextSolution()
        q2a.closeQuery()

        q2b = Query(parent(Y, y.lower())) 
        result2b = q2b.nextSolution()
        q2b.closeQuery()

        result2 = result2a and result2b

        print("Yes" if result1 or result2 else "No")

    elif (match := re.match(r"Who are the parents of ([A-Z][a-z]+)\?", question)): 
        x = match.group(1)
        q = Query(parent(X, x.lower()))  
        parents_of = []
        while q.nextSolution():
            temp = str(X.get_value())
            parents_of.append(temp.capitalize())  
        q.closeQuery()
        print("Parents of", x, ":", ", ".join(parents_of) if parents_of else "None")
    
    elif (match := re.match(r"Who are the daughters of ([A-Z][a-z]+)\?", question)): 
        x = match.group(1)
        q = Query(daughter(X, x.lower()))  
        daughters_of = []
        while q.nextSolution():
            temp = str(X.get_value())
            daughters_of.append(temp.capitalize())  
        q.closeQuery()
        print("Daughters of", x, ":", ", ".join(daughters_of) if daughters_of else "None")
    
    elif (match := re.match(r"Who are the sons of ([A-Z][a-z]+)\?", question)): 
        x = match.group(1)
        q = Query(son(X, x.lower()))  
        sons_of = []
        while q.nextSolution():
            temp = str(X.get_value())
            sons_of.append(temp.capitalize())  
        q.closeQuery()
        print("Sons of", x, ":", ", ".join(sons_of) if sons_of else "None")
        
    elif (match := re.match(r"Who are the children of ([A-Z][a-z]+)\?", question)): 
        x = match.group(1)
        q = Query(child(X, x.lower()))  
        children_of = []
        while q.nextSolution():
            temp = str(X.get_value())
            children_of.append(temp.capitalize())  
        q.closeQuery()
        print("Children of", x, ":", ", ".join(children_of) if children_of else "None")

    elif (match := re.match(r"Are ([A-Z][a-z]+) and ([A-Z][a-z]+) relatives\?", question)): 
        x, y = match.groups()  
        q = Query(relative(x.lower(), y.lower())) 
        print("Yes" if q.nextSolution() else "No")
        q.closeQuery() 

def main():
    list_prompt = []  # Store prompts to prevent duplicates

    print("\nWelcome to the chatbot!")
    print("Please enter your prompt below.\n")

    while True:
        prompt = input("> ")

        if not prompt.strip():
            print("Please enter a valid prompt.")
            continue

        if prompt in list_prompt:
            print("This prompt has already been entered. Please try a different one.")
            continue 

        if prompt.endswith('?'):  # Question
            process_question(prompt)
        elif prompt.endswith('.'):  # Statement
            process_statement(prompt)
            list_prompt.append(prompt)  # Add the prompt to the list of previous prompts
        else:  
            print("Prompt should end with either ? or .") # Invalid input
            
main() 