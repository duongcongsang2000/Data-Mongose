import json
from typing import Dict

class ServiceResponse():
    def __init__(self):
        self.data = {}
        self.success = True
        self.message = ""
        
    def copy(self, res):
        self.data = res['data']
        self.success = res['success']
        self.message = res['message']    
        return self
        
    def copy2(self, res):
        self.data = res.data
        self.success = res.success
        self.message = res.message    
        return self
    
    def result(self):
        return {
            "success": self.success,
            "data": self.data,
            "message": self.message
        }