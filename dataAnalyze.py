from decimal import Decimal

class DataPoint:
    x = 0
    y = 0
    z = 0
    id = 0x0000
    time = 0

    def __init__(self, x, y, z, id, time):
            self.x = Decimal(x)
            self.y = Decimal(y)
            self.z = Decimal(z)
            self.id = id
            self.time = int(time.split(".")[0].replace(":", ""))

class DataSet:
    points = []
    xmin = 10000000
    xmax = 0
    xmedian = 0
    ymin = 10000000
    ymax = 0
    ymedian = 0
    zmin = 10000000
    zmax = 0
    zmedian = 0
    startTime = 0
    endTime = 0

    def __init__(self, points):
        noPoints = len(points)
        self.points = points
        xsum = 0
        ysum = 0
        zsum = 0
        for p in points:
            xsum += p.x
            ysum += p.y
            zsum += p.z
            if self.xmin > p.x:
                self.xmin =p.x
            if self.xmax < p.x:
                self.xmax = p.x
            if self.ymin > p.y:
                self.ymin =p.y
            if self.ymax < p.y:
                self.ymax = p.y
            if self.zmin > p.z:
                self.zmin =p.z
            if self.zmax < p.z:
                self.zmax = p.z
            
        self.xmedian = xsum / noPoints
        self.ymedian = ysum / noPoints
        self.zmedian = zsum / noPoints


    def printself(self):
        print(len(self.points))
        return "(x,y) \t& (" + "{:.1f}".format(self.xmedian / 10) + ", "+ "{:.1f}".format(self.ymedian / 10) + ", " + "{:.1f}".format(self.zmedian / 10) + ") \t & (" + "{:.1f}".format(self.xmin / 10) + ") \t& (" + "{:.1f}".format(self.xmax / 10) + ")\t& (" + "{:.1f}".format(self.ymin / 10) + ")\t & (" + "{:.1f}".format(self.ymax / 10) + ") \t & (" + "{:.1f}".format(self.zmin / 10) + ")\t & (" + "{:.1f}".format(self.zmax / 10) + ")\t \\\\ \\hline\n"
        # print("x min: " + str(self.xmin) + ", xmax: " + str(self.xmax) + ", xmed: " + str(self.xmedian))
        # print("y min: " + str(self.ymin) + ", ymax: " + str(self.ymax) + ", ymed: " + str(self.ymedian))
        # print("z min: " + str(self.zmin) + ", zmax: " + str(self.zmax) + ", zmed: " + str(self.zmedian))

def getData(inputString):
    f = open(inputString)
    resultName = inputString.replace(".txt", "") + "result.txt"
    resultFile = open(resultName, "w")
    startLatexTable = "\\begin{table}[] \n    \\begin{tabular}{|l|l|l|l|l|l|l|l|}\n    \\hline\n    Actual grid & Average grid (x,y,z)   & x min   & x max   & y min    & y max   & z min   & z max    \\\\ \\hline\n"
    resultFile.write(startLatexTable)
    lines = f.readlines()
    points = []
    for l in lines:
        if l != 'test1\n':
            subl = l.split()
            points.append(DataPoint(subl[4][:-1], subl[6][:-1], subl[8][:-1], subl[2][:-1], subl[10]))
    
    clusteredPoints = []
    clusteredPoints.append([])
    i = 0
    moving = False
    time = points[0].time
    for p in points:
        if time + 5 > p.time:
            if not moving:
                clusteredPoints[i].append(p)
        else:
            if not moving:
                clusteredPoints.append([])
                
                clusteredPoints[i].append(p)
                i += 1
            time = p.time
            moving = not moving

    dataSets = []
    for p in clusteredPoints:
        if len(p) > 0:
            dataSets.append(DataSet(p))
    
    i = 0
    for p in dataSets:
        print(i)
        i += 1
        resultS = p.printself()
        resultFile.write(resultS)
    resultFile.write("\\end{tabular}\n\\label{Tab:one-tag-experiment-result}\\end{table}")
    resultFile.close
    f.close


if __name__ == "__main__":
    getData("C:/Users/frede/Desktop/tests/3 tag/test1/26467data.txt")
    getData("C:/Users/frede/Desktop/tests/3 tag/test1/26895data.txt")
    getData("C:/Users/frede/Desktop/tests/3 tag/test1/24622data.txt")

    # getData("C:/Users/frede/Desktop/tests/5 tag/test1/26895data.txt")
    # getData("C:/Users/frede/Desktop/tests/5 tag/test1/24622data.txt")
    # getData("C:/Users/frede/Desktop/tests/5 tag/test1/26467data.txt")
    # getData("C:/Users/frede/Desktop/tests/5 tag/test1/26901data.txt")
    # getData("C:/Users/frede/Desktop/tests/5 tag/test1/27001data.txt")

        
    


