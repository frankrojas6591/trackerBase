from flask import Blueprint, jsonify
from flask import current_app as app
from flask import render_template
from flask import session, request, redirect, url_for

#---------------
# app object
#---------------

from tracker.util.appBase import appBase

from tracker.Mood.Mood import Mood

ext = Mood()
_ = ext.loadProfile(None, obj=ext)

def create_ext(app):
    return ext

#---------------
# declare blue print 
#---------------
# Blueprint Configuration
bp = Blueprint(ext.oID, __name__, url_prefix=f'/{ext.oID}/api', template_folder="templates", static_folder="static")


#---------------
# routes
#---------------
#import .routes
@bp.route('/test')
def _test():
    msg = f"{ext.oID}.routes name:{__name__} Blueprint"
    msf = f"<br>session:{str(session)}"
    msg += "<br>Status:Active"
    msg += f"<p>{str(ext).replace('\n','<br>')}"
    print("Mood Debug app:", msg)
    return msg
    
@app.route('/login', methods=['POST'])
def login():
    # Get data from the request form
    username = request.form['username']
    # Store user-specific data in the session
    session['username'] = username
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # Access the stored data in subsequent requests
    if 'username' in session:
        return f'Hello, {session["username"]}!'
    else:
        return 'You are not logged in.'

# Home page /api/company/<company_name>
@bp.route('/<grpID>/<userID>', methods=['GET'])
def home(grpID, userID):
    # In a real app, you would fetch data related to the company_name from a database.
    # For this example, we return a simple JSON response.
    # Pass the company_name variable to the HTML template

    
    ## FIXME
    #-- Validate grpID, userID
    #gData= grpData(grpID = sys.argv[1])

    

    template_data = {
    'company_name' : ext.company_name,
    'user': userID,
    'mood' : 5,
    'group' : grpID
    }
    return render_template('MoodHome.html', **template_data)

    # Render home page
    return render_template('MoodHome.html', company_name=ext.company_name) #
    '''
    <!-- <a href="{{ url_for('company_api', company_name=company_name) }}" class="api-link">/api/company/{{ company_name }}</a>
        -->
    '''


#--- ???
@app.route('/results/<color>')
def results(whoID):
    return f"Your ID: {whoID}"

#-- save mood
@app.route('/save', methods=['POST'])
def save_mood():
    """Save mood entry."""
    data = request.json
    #s_whoID = request.form.get("whoisit_dropdown") # Get the value of the 'color_dropdown' field

    whoID = data['whoID']
    if whoID == '?' :
        return jsonify({'success': False, 
                        'feedback': "****** Please identify who you are. *****"})

    print(f"DEBUG 84 data: {data}", flush=True)

    uiID = data['uiID']
    if uiID == 'UI_1':
        m1 = 'happiness'
        m2 = 'anxiety'
        m3 = 'energy'
    else:
        m1 = 'mood1'
        m2 = 'mood2'
        m3 = 'mood3'
    
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

@app.route('/averages')
def get_averages(*args):
    """Get 7-day averages."""
    
    print(f"DEBUG loadAvg 137 args: {request.args}", flush=True)
    
    whoID = request.args.get('whoID', '?') # Default to 'Guest' if 'name' is missing
    uiID = request.args.get('uiID', 'UI_3')

    if whoID == '?' :
        return jsonify({
            'mood1': 'Who?',
            'mood2': 'Who?',
            'mood3': 'Who?'
        })
        
    entries = gData.loadMoodList(whoID)
    if not entries:
        return jsonify({'mood1': 0, 'mood2': 0, 'mood3': 0})
    
    recent = entries[:min(7, len(entries))]
    
    avg_mood1 = sum(e['mood1'] for e in recent) / len(recent)
    avg_mood2 = sum(e['mood2'] for e in recent) / len(recent)
    avg_mood3 = sum(e['mood3'] for e in recent) / len(recent)
    
    return jsonify({
        'mood1': f'{avg_mood1:.1f}',
        'mood2': f'{avg_mood2:.1f}',
        'mood3': f'{avg_mood3:.1f}'
    })

@app.route('/history')
def get_history(*args):
    """Get mood history."""
    print(f"DEBUG getHist 167 args: {request.args}", flush=True)
    
    whoID = request.args.get('whoID', '?') # Default to 'Guest' if 'name' is missing
    uiID = request.args.get('uiID', 'UI_3')

    if whoID == '?' :
        return jsonify([])

    entries = gData.loadMoodList(whoID)

    return jsonify(entries[:10])
