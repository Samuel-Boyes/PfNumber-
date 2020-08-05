import copy
import time

class pnumber:
    #Stores numbers as a dictionary of prime factors, in the format of {factor:exponent}
    def __init__(self, numerator, denominator):
        #Error Checking
        if(not isinstance(numerator, int)):
            raise ValueError("Numerator must be an integer!")
        if(not isinstance(denominator, int)):
            raise ValueError("Denominator must be an integer!")
        if(denominator == 0):
            raise ValueError("Denominator cannot be Zero!")
        #default value is 1
        self.values = {}
        self.isNegative = 1
        self.isZero = False
        self.__storeValues(numerator, denominator)

    def __storeValues(self, numerator, denominator):
        #refreshes default values for use with the addition and subtraction functions.
        #If the numerator is 0, this is represented with a special state.
        #If the total value is 1, this is represented with an empty dictionary.
        self.values = {}
        self.isNegative = 1
        self.isZero = False
        if(numerator == 0):
            self.isZero = True
        else: #Else, factorize
            if(numerator < 0):
                self.isNegative = self.isNegative * -1
                numerator = numerator * -1
                self.values = self.__factorize(numerator)
            else:
                self.values = self.__factorize(numerator)
            if(denominator < 0):
                self.isNegative = self.isNegative * -1
                denominator = denominator * -1
                newValues = self.__factorize(denominator)
                for key, value in newValues.items():
                    if (key == 1):
                        pass
                    elif(key in self.values):
                        self.values[key] = self.values[key] - value
                    else:
                        self.values[key] = 0 - value
                    if (key in self.values):
                        if (self.values[key] == 0):
                            self.values.pop(key)
            else:
                newValues = self.__factorize(denominator)
                for key, value in newValues.items():
                    if (key == 1):
                        pass
                    elif(key in self.values):
                        self.values[key] = self.values[key] - value                   
                    else:
                        self.values[key] = 0 - value
                    if (key in self.values):
                        if (self.values[key] == 0):
                            self.values.pop(key)

    def __factorize(self, number):
        #used for finding all prime factors of the number provided
        #0 will raise errors because it should be handled before this.
        if(number == 0):
            raise ZeroError("0 should not be handled in the factorize method")
        if(number == 1):
            return {}
        factors = {}
        ii = 2
        current_number = number
        while ii*ii <= number:
            #check if ii is a factor
            if (current_number%ii == 0):
                #check if ii is already in the factors dictionary
                if(ii in factors):
                    #increment if so
                    factors[ii] = factors[ii] + 1
                else:
                    #create it if not
                    factors[ii] = 1
                #remove the factor from number and repeat.
                current_number = current_number//ii
            else:
                #only increment ii if the current value isn't a factor.
                ii = ii + 1
        if (current_number != 1):
            factors[current_number] = 1
        return factors

    def unfactorize(self):
        #returns a tuple containing numerator and denominator
        #return 0 if isZero is true
        #return 1 if dictionary is empty
        if (self.isZero == True):
            return (0,1) #This should not occur, but it might be useful in the future?
        if (len(self.values.items()) == 0):
            return (1,1)
        #else multiply out
        numerator = self.isNegative
        denominator = 1
        for key, value in self.values.items():
            if value > 0:
                numerator = numerator * (key ** value)
            else:
                denominator = denominator * (key ** (value * -1))
        return (numerator, denominator)

    def display(self):
        #displays the current data
        return (self.isNegative,self.isZero,self.values)

    def displayValue(self):
        #displays the value as numerator/denominator
        #return 0 if isZero is set to True
        #return 1 if dictionary is empty
        if (self.isZero == True):
            return "0/1"
        if (len(self.values.items()) == 0):
            return "1/1"
        #else multiply out
        numerator = self.isNegative
        denominator = 1
        for key, value in self.values.items():
            if value > 0:
                numerator = numerator * (key ** value)
            else:
                denominator = denominator * (key ** (value * -1))
        if (denominator == 1):
            return(str(numerator))
        return (str(numerator) + "/" + str(denominator))

    def getValue(self):
        #returns the value of the dictionary
        #return 0 if isZero is true
        #return 1 if dictionary is empty
        if (self.isZero == True):
            return 0
        if (len(self.values.items()) == 1):
            return 1
        #else multiply out
        float_value = self.isNegative
        for key, value in self.values.items():
            float_value = float_value * (key**value)
        return (float_value)

    def __mul__(self, other):
        selfcopy = copy.deepcopy(self)
        if (other.isZero == True or selfcopy.isZero == True):
            selfcopy.isZero = True
            selfcopy.isNegative = 1
            selfcopy.values = {}
            #multiplying by 0 deletes everything
        elif (len(other.values.items()) == 0):
            selfcopy.isNegative = selfcopy.isNegative * other.isNegative
            #multiplying by 1 does nothing.
        elif (len(selfcopy.values.items()) == 0):
            selfcopy.isNegative = selfcopy.isNegative * other.isNegative
            selfcopy.values = copy.deepcopy(other.values)
            #multiplying 1 by a value creates a copy of that value.
        else:
            #else, multiply out.
            selfcopy.isNegative = selfcopy.isNegative * other.isNegative
            for key, value in other.values.items():
                if(key in selfcopy.values):
                    selfcopy.values[key] = selfcopy.values[key] + other.values[key]
                else:
                    selfcopy.values[key] = other.values[key]
                if (key in selfcopy.values):
                    if (selfcopy.values[key] == 0):
                        selfcopy.values.pop(key)
        return selfcopy
            

    def __truediv__(self, other):
        selfcopy = copy.deepcopy(self)
        if (other.isZero == True):
            raise DivideByZeroError("Cannot divide by zero!")
        elif(selfcopy.isZero == True):
            pass
            #0 Divided by anything = 0
        elif (len(other.values.items()) == 0):
            selfcopy.isNegative = selfcopy.isNegative * other.isNegative
            #dividing by 1 does nothing.
        else:
            #Else, divide out.
            selfcopy.isNegative = selfcopy.isNegative * other.isNegative
            for key, value in other.values.items():
                if(key in selfcopy.values):
                    selfcopy.values[key] = selfcopy.values[key] - other.values[key]
                else:
                    selfcopy.values[key] = 0 - other.values[key]
                if (key in selfcopy.values):
                    if (selfcopy.values[key] == 0):
                        selfcopy.values.pop(key)
        return selfcopy

    def __add__(self, other):
        
        selfcopy = copy.deepcopy(self)
        if (other.isZero == True):
            pass
        elif(selfcopy.isZero == True):
            selfcopy.isZero = other.isZero
            selfcopy.isNegative = other.isNegative
            selfcopy.values = copy.deepcopy(other.values)
        else:
            x = selfcopy.unfactorize()
            y = other.unfactorize()
            numerator = x[0]*y[1] + y[0]*x[1]
            denominator = x[1]*y[1]
            selfcopy.__storeValues(numerator, denominator)
        return selfcopy
            

    def __sub__(self, other):
        selfcopy = copy.deepcopy(self)
        if (other.isZero == True):
            pass
        elif(selfcopy.isZero == True):
            selfcopy.isZero = other.isZero
            selfcopy.isNegative = other.isNegative * -1
            selfcopy.values = copy.deepcopy(other.values)
        else:
            x = selfcopy.unfactorize()
            y = other.unfactorize()
            numerator = x[0]*y[1] - y[0]*x[1]
            denominator = x[1]*y[1]
            selfcopy.__storeValues(numerator, denominator)
        return selfcopy
        

#muller's recurrence stuff
#Constants
x1 = pnumber(108,1)
x2 = pnumber(815,1)
x3 = pnumber(1500,1)
outlist = [pnumber(4,1),pnumber(17,4)]

n=15
start = time.time()
for ii in range(2,n+1):
    print("Start:",ii)
    outlist.append(x1 - ((x2 - (x3/outlist[ii-2]))/outlist[ii-1]))
    print("Time: ",time.time() - start)
    print(outlist[ii].display()," ", outlist[ii].displayValue()," ",outlist[ii].getValue())
