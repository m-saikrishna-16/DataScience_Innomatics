class Solution:
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        m=max(candies)
        l=[]
        for i in candies:
            if i+extraCandies>=m:
                l.append(True)
            else:
                l.append(False)
        return l