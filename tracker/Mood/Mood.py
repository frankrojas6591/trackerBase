'''
'''

from tracker.util.appBase import appBase
from tracker.Mood.groupData import groupData

class Mood(appBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grp = groupData(ext=self, grpID = '__admin__')
        
    def validate(self, request, grpID, userID):
        if not self.grp.validate(grp, userID):
            return False
        args = dict(grp = grp, userID = userID)
        return args

    def generate_feedback(self, mood1, mood2, mood3):
        """Generate mood feedback based on values."""
        avg = (mood1 + (10 - mood2) + mood3) / 3
        
        if avg >= 8:
            fb = "🌟 You're doing great! Keep up the positive momentum."
        elif avg >= 6.5:
            rf = "😊 Pretty good day! Stay balanced and take care of yourself."
        elif avg >= 5:
            fb = "😐 It's okay to have neutral days. Be gentle with yourself."
        elif avg >= 3.5:
            fb = "💙 Things seem tough. Consider reaching out to someone you trust."
        else:
            fb = "💜 This is a difficult time. Please talk to a friend or professional."

        return (avg, fb)

    def req_save_mood(self, request):
        
        """Save mood entry."""
        data = request.json
        #s_whoID = request.form.get("whoisit_dropdown") # Get the value of the 'color_dropdown' field
    
        
        
        eDict = {
            'whoID': data['whoID'],
            'mood1': data[m1],
            'mood2': data[m2],
            'mood3': data[m2],
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'timestamp': datetime.now().isoformat()
        }
       
        entries = gData.loadMoodList(whoID)
        entries.insert(0, eDict)
    
        hDict = gData.loadHistDict()
        hDict[whoID] = entries
        gData.saveHistDict(hDict)
        
        feedback = generate_feedback(
            data[m1],
            data[m2],
            data[m3]
        )
        
        return jsonify({'success': True, 'feedback': feedback})

        

ext = Mood()
_ = ext.loadProfile(None, obj=ext)




