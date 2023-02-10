from datetime import datetime
import discord

## handle every users data

class User:
    def __init__(self,user_ctx=None):
        self.user_ctx          = user_ctx
        self.check_stack       = []
        self.__check_in_record = []  # private
        self.__check_ou_record = []  # private

    async def checkout(self):
        ## forget check in
        if (len(self.check_stack)==0) :
            await self.user_ctx.send("No check in record!!")
            self.__check_in_record.append(None)
            return False
        else:
            this_check_time = datetime.now()
            checkin_time    = self.check_stack.pop()

            self.__check_ou_record.append(this_check_time)
            await self.user_ctx.send("you check out at "+ this_check_time.strftime("%m-%d %X"))
            return True
            
    async def checkin(self):
        ## forget check out
        if (len(self.check_stack)==1) :
            last_time = self.check_stack.pop() 
            await self.user_ctx.send("you didn't check out last time\n"+"check in record : "+last_time.strftime("%m-%d %X"))
            self.__check_ou_record.append(None)
            return False
        else:
            this_check_time  = datetime.now()
            self.check_stack = [this_check_time]

            self.__check_in_record.append(this_check_time)
            await self.user_ctx.send("you check in at "+this_check_time.strftime("%m-%d %X"))
            return True


    def get_user_check_in_record(self):
        return self.__check_in_record

    def get_user_check_ou_record(self):
        return self.__check_out_record





if __name__ == '__main__':
    a = User()

