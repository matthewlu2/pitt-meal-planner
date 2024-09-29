import os
import google.generativeai as genai
import requests
from datetime import datetime
from typing import Any, Dict

# Configuration for Gemini AI
genai.configure(api_key="AIzaSyC7H8T9ZGy1dmzBEQvHPeWy0P4GBK_u1f0")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

chat_session = model.start_chat(
    history=[]
)

# Constants for the Pitt API
REQUEST_HEADERS = {"User-Agent": "Chrome/103.0.5026.0"}
LOCATIONS_URL = "https://api.dineoncampus.com/v1/locations/status?site_id=5e6fcc641ca48e0cacd93b04&platform="
MENU_URL = "https://api.dineoncampus.com/v1/location/{location_id}/periods/{period_id}?platform=0&date={date_str}"

LOCATIONS = {
    "ETHEL'S",
    "THE EATERY",
    "PANERA BREAD",
    "TRUE BURGER",
    "THE PERCH",
    "FORBES STREET MARKET",
    "BUNSEN BREWER",
    "WICKED PIE",
    "SMOKELAND BBQ AT THE PETERSEN EVENTS CENTER",
    "THE MARKET AT TOWERS",
    "THE DELICATESSEN",
    "CAMPUS COFFEE & TEA CO - TOWERS",
    "PA TACO CO.",
    "FT. PITT SUBS",
    "CREATE",
    "POM & HONEY",
    "THE ROOST",
    "CATHEDRAL SUSHI",
    "BURRITO BOWL",
    "CHICK-FIL-A",
    "SHAKE SMART",
    "STEEL CITY KITCHEN",
    "SMOKELAND BBQ FOOD TRUCK",
    "CAMPUS COFFEE & TEA CO - SUTHERLAND",
    "THE MARKET AT SUTHERLAND",
    "PLATE TO PLATE AT SUTHERLAND MARKET",
    "EINSTEIN BROS. BAGELS - POSVAR",
    "EINSTEIN BROS. BAGELS - BENEDUM",
    "BOTTOM LINE BISTRO",
    "CAFE VICTORIA",
    "CAFE 1787",
    "CAMPUS COFFEE & TEA CO - PUBLIC HEALTH",
    "RXPRESSO",
    "SIDEBAR CAFE",
    "CAFE 1923",
    }

def get_locations() -> Dict[str, Any]:
    resp = requests.get(LOCATIONS_URL, headers=REQUEST_HEADERS)
    locations = resp.json()["locations"]
    dining_locations = {location["name"].upper(): location for location in locations}
    return dining_locations

def get_location_menu(location: str, date: datetime | None = None) -> Any:
    location = location.upper()
    if location not in LOCATIONS:
        raise ValueError("Invalid Dining Location")
    
    if date is None:
        date = datetime.today()

    date_str = date.strftime("%y-%m-%d")
    location_id = get_locations()[location]["id"]
    
    # Get periods first
    periods_resp = requests.get(
        f"https://api.dineoncampus.com/v1/location/{location_id}/periods?platform=0&date={date_str}",
        headers=REQUEST_HEADERS,
    )
    
    periods = periods_resp.json()["periods"]
    if not periods:
        return {}

    # Get the menu for the first period
    period_id = periods[0]["id"]
    menu_resp = requests.get(
        MENU_URL.format(location_id=location_id, period_id=period_id, date_str=date_str),
        headers=REQUEST_HEADERS,
    )
    return menu_resp.json().get("menu", {})

# Get the menu for THE EATERY
eatery_menu = get_location_menu("THE EATERY", datetime.today())
# perch_menu = get_location_menu("THE PERCH", datetime.today())


# Format the menu data for sending to Gemini AI
menu_output = f"Today's menu for THE EATERY:\n{eatery_menu}"
# menu_output_2 = f"Today's menu for THE PERCH:\n{eatery_menu}"


# Send the menu data to Gemini AI

response = chat_session.send_message(menu_output+ " Give me a summarized version of the menu, organized by station")
print(response.text)

#response2 = chat_session.send_message(menu_output_2+ " Give me a summarized version of the menu, organized by station")
#print(response2.text)

while True:
    s = "> "
    inp = input(s)

    r = chat_session.send_message(inp)
    print(r.text)