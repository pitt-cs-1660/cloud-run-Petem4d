from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from google.cloud import firestore
from fastapi.responses import RedirectResponse

from typing import Annotated
import datetime

app = FastAPI()

# mount static files
app.mount("/static", StaticFiles(directory="/app/static"), name="static")
templates = Jinja2Templates(directory="/app/template")

# init firestore client
db = firestore.Client()
votes_collection = db.collection("votes")


@app.get("/")
async def read_root(request: Request):
    # ====================================
    # ++++ START CODE HERE ++++
    # ====================================

    # stream all votes; count tabs / spaces votes, and get recent votes
    # get all votes from firestore collection
    votes = votes_collection.stream()
    # @note: we are storing the votes in `vote_data` list because the firestore stream closes after certain period of time
    vote_data = []
    space_count = 0
    tab_count = 0
    for v in votes:
        temp = v.to_dict()
        if(temp["team"] == "TABS"):
            tab_count += 1
        else:
            space_count += 1
        vote_data.append(temp)
        
    #print(vote_data)
    # ====================================
    # ++++ STOP CODE ++++
    # ====================================
    return templates.TemplateResponse("index.html", {
        "request": request,
        "tabs_count": tab_count,
        "spaces_count": space_count,
        "recent_votes": vote_data
    })


@app.post("/")
async def create_vote(team: Annotated[str, Form()]):
    if team not in ["TABS", "SPACES"]:
        raise HTTPException(status_code=400, detail="Invalid vote")

    # ====================================
    # ++++ START CODE HERE ++++
    # ====================================
    
    votes_collection.add({
        "team": team,
        "time_cast": datetime.datetime.utcnow().isoformat()
    })
    #return RedirectResponse(url=f"/", status_code=303)


        # create a new vote document in firestore
    # return     votes_collection.add({
    #     "team": team,
    #     "time_cast": datetime.datetime.utcnow().isoformat()
    # })

    # ====================================
    # ++++ STOP CODE ++++
    # ====================================
