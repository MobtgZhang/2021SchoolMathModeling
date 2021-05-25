class MonthTime:
    def __init__(self,year=None,month=None,time_str=None):
        self.year = year
        self.month = month
        if time_str is not None:
            self.year,self.month,_ = time_str.split('/')
        self.year, self.month = int(self.year),int(self.month)
    def __lt__(self,other):
        if self.year < other.year:
            return True
        elif self.year == other.year and self.month <other.month:
            return True
        else:
            return False
    def __eq__(self, other):
        if self.year == other.year and self.month == other.month :
            return True
        else:
            return False
    def __gt__(self,other):
        if self.year > other.year:
            return True
        elif self.year == other.year and self.month > other.month:
            return True
        else:
            return False
    def __ge__(self,other):
        return self>other or self == other
    def __le__(self, other):
        return self<other or self == other



class DateTime:
    def __init__(self,year=None,month=None,day=None,time_str=None):
        self.year = year
        self.month = month
        self.day = day
        if time_str is not None:
            self.year,self.month,self.day = time_str.split('/')
        self.year, self.month, self.day = int(self.year),int(self.month),int(self.day)
    def __lt__(self,other):
        if self.year < other.year:
            return True
        elif self.year == other.year and self.month <other.month:
            return True
        elif self.year == other.year and self.month == other.month and self.day<other.day:
            return True
        else:
            return False
    def __eq__(self, other):
        if self.year == other.year and self.month == other.month and self.day == other.day:
            return True
        else:
            return False
    def __gt__(self,other):
        if self.year > other.year:
            return True
        elif self.year == other.year and self.month > other.month:
            return True
        elif self.year == other.year and self.month == other.month and self.day > other.day:
            return True
        else:
            return False
    def __ge__(self,other):
        return self>other or self == other
    def __le__(self, other):
        return self<other or self == other
    def __set__(self, instance, value):
        if isinstance(instance,TimeSect):
            return TimeSect(value)
        if isinstance(instance,str):
            return TimeSect(value)
    def __str__(self):
        return "%d/%d/%d"%(self.year,self.month,self.day)
class TimeSect:
    def __init__(self,time_str=None,time_sect = None):
        if time_str:
            outstr = time_str.split()
            years = outstr[0]
            times = outstr[1]
            self.year,self.month,self.day = [int(k) for k in years.split("/")]
            self.hour,self.minute,self.second = [int(k) for k in times.split(":")]
        elif time_sect:
            self.year = time_sect.year
            self.month = time_sect.month
            self.day = time_sect.day
            self.year = time_sect.hour
            self.minute = time_sect.mintue
            self.second = time_sect.second
        else:
            self.year, self.month, self.day = None,None,None
            self.hour, self.minute, self.second = None,None,None
    def __lt__(self,other):
        if self.year < other.year:
            return True
        elif self.year == other.year and self.month <other.month:
            return True
        elif self.year == other.year and self.month == other.month and self.day<other.day:
            return True
        elif self.year == other.year and self.month == other.month and self.day==other.day and\
                 self.hour < other.hour:
            return True
        elif self.year == other.year and self.month == other.month and self.day==other.day and\
                 self.hour == other.hour and self.minute < other.minute :
            return True
        elif self.year == other.year and self.month == other.month and self.day==other.day and\
                 self.hour == other.hour and self.minute == other.minute and self.second <other.second:
            return True
        else:
            return False
    def __eq__(self, other):
        if self.year == other.year and self.month == other.month and self.day == other.day and \
                self.hour == other.hour and self.minute == other.minute and self.second == other.second:
            return True
        else:
            return False
    def __gt__(self,other):
        if self.year > other.year:
            return True
        elif self.year == other.year and self.month > other.month:
            return True
        elif self.year == other.year and self.month == other.month and self.day > other.day:
            return True
        elif self.year == other.year and self.month == other.month and self.day==other.day and\
                 self.hour > other.hour:
            return True
        elif self.year == other.year and self.month == other.month and self.day==other.day and\
                 self.hour == other.hour and self.minute > other.minute :
            return True
        elif self.year == other.year and self.month == other.month and self.day==other.day and\
                 self.hour == other.hour and self.minute == other.minute and self.second > other.second:
            return True
        else:
            return False
    def __ge__(self,other):
        return self>other or self == other
    def __le__(self, other):
        return self<other or self == other
    def __set__(self, instance, value):
        if isinstance(instance,TimeSect):
            return TimeSect(value)
        if isinstance(instance,str):
            return TimeSect(value)
    def __str__(self):
        return "%d-%d-%d\t%d:%d:%d"%(self.year,self.month,self.day,self.hour,self.minute,self.second)

