class Check:
    def check(self, check):
        try:
            with open("info.txt","r") as f:
                read=f.read()
                return check in read
        except:
            return False
