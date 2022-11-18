class Solution(object):  
    def findTheDifference(self, s, t):  
        ls_s = [s[i] for i in range(len(s))]  
        ls_t = [t[i] for i in range(len(t))]  
        for elem in ls_s:  
            ls_t.remove(elem)  
        return(ls_t[0])  

obj = Solution()  
s = "oBBCCoooFGHoAAFGHooooGooxoEEoooooooo"  
t = "oBBCCoooFGHoAAFGHooooGooxooEEooooooo"  
print(obj.findTheDifference(s, t))