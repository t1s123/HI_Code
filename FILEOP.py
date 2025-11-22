class FILE:
    def read(self,file):
        try:
            with open(file,"r") as f:
                return f.read()
            
        except Exception as e:
            return f"ERROR: {e}"
        f.close()
    
    def readlines(self,file):
        try:
            with open(file,"r") as f:
                return f.readlines()
            
        except Exception as e:
            return f"ERROR: {e}"
        f.close()