class Check:
    def check(self, check):
        with open("info.txt","r") as f:
            read=f.read()
            return check in read