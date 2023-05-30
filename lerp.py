def Lerp(start, end, pct):
    '''
    Base Lerp function. Pass additional functions
    from this file to modify.

    Example: 
    Lerp(0, 1, EaseIn(elapsedTime / duration))
    
    Parameters:
    start (int | float): The start value to lerp from. This value can be an integer/float
    end (int | float): The end value to lerp to. This value can be an integer/float
    pct (float): The percentage of the lerp completed. Must be a value between 0.0 and 1.0
    '''
    pct = max(0, min(1, pct))
    return start + (end - start) * pct

def EaseIn(time):
    '''
    Description: Starts slow, then speeds up
    Function: x*x
    '''
    return time * time

def EaseOut(time):
    '''
    Description: Starts fast, then slows down
    Function: 1-((1-x)*(1-x))
    '''
    return Flip(EaseIn(Flip(time)))

def EaseInOut(time):
    '''
    Description: EaseIn, then EaseOut
    Function: Lerp(x*x, 1-((1-x)*(1-x)), x)
    '''
    return Lerp(EaseIn(time), EaseOut(time), time)

def Spike(time):
    '''
    Description: EaseIn, then Reverse EaseIn
    Function: x <= 0.5: (x/0.5)*(x/0.5), x > 0.5: ((1-x)/0.5)*((1-x)/0.5)
    '''
    if time <= 0.5:
        return EaseIn(time / 0.5)
    return EaseIn(Flip(time) / 0.5)



def Flip(x):
    '''
    Description: Flips the input
    Function: 1-x
    '''
    return 1 - x
