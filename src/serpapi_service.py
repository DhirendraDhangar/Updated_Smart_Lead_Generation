from serpapi import GoogleSearch
from config import SERPAPI_KEY

def search_businesses(location, industry, num_leads):
    leads=[]
    start=0
    while len(leads)<num_leads:
        params={"engine":"google_maps","q":f"{industry} in {location}","hl":"en","start":start,"api_key":SERPAPI_KEY}
        results=GoogleSearch(params).get_dict()
        local=results.get("local_results",[])
        if not local:
            break
        for place in local:
            website=place.get("website","")
            leads.append({"Lead Name":place.get("title",""),"Website":website, "Website Available":"Yes" if website else "No","Phone":place.get("phone",""),"Source":"SerpAPI","Location":place.get("address",""),"Industry":industry})
            if len(leads)>=num_leads:
                break
        start+=20
    return leads[:num_leads]
def google_search(query):
    try:
        params = {
            "engine": "google",
            "q": query,
            "hl": "en",
            "num": 10,
            "api_key": SERPAPI_KEY
        }

        data = GoogleSearch(params).get_dict()

        if data.get("error"):
            print("SerpAPI Error:", data["error"])
            return []

        return data.get("organic_results", [])

    except Exception as e:
        print("SerpAPI error:", e)
        return []
