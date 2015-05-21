import nsb_format_points
import nsb_database

def readable_name(name):
    split_name = name.split('_')
    return ' '.join([split_name[0], split_name[-1]])
    #result = name.replace('deathless_score', 'deathless')
    #result = name.replace('_', ' ')
    #return result



    


class leaderboard:


    def __init__(self, name):
        self._name = name
        self.name = readable_name(name)


        self.url = 'http://www.necrolab.com/api/' + name
        self._url = self.url + '/latest_rankings'

        self.date = None


    def __str__(self):
        return self.name

    def parseResponse(self, response):
        return nsb_database.jsonToList(response)

    def include(self):
        return True

    def unit(self):
        return 'points'

    def pre_unit(self):
        return None

    def parseScore(self, score):
        return str(round(float(score)))

    def entriesToReportOnPointsDiff(self):
        return 0

    def entriesToReportOnRankDiff(self):
        return 5

    def entriesToPrivateReportOnPointsDiff(self):
        return 0

    def entriesToPrivateReportOnRankDiff(self):
        return 100
    
    def formatPoints(self, points):
        return str(int(float(points)))

    def relativePoints(self, points, prevPoints):
        return nsb_format_points.relativeScore(float(points), float(prevPoints))

        
