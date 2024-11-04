


class FailedSoupInit(Exception):
    def __init__(self, message="An error occurred in CustomError"):
        self.message = message
        super().__init__(self.message)



class ElementNotFound(Exception):
    def __init__(self, message="Could not find the element while parsing"):
        self.message = message
        super().__init__(self.message)    

class PageNotFound(Exception):
    def __init__(self, message="Could not fetch the page"):
        self.message = message
        super().__init__(self.message)    
