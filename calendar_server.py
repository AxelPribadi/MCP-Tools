from datetime import datetime
from dateutil import parser
from tzlocal import get_localzone_name
from mcp.server.fastmcp import FastMCP

from calendar_functions import * 

mcp = FastMCP("Calendar Helper")

@mcp.tool()
def read_calendar(
    start_time: str,
    end_time: str,
    top_n: int
) -> dict:
    """Fetch `top_n` Google Calendar events between a timeframe (in ISO format)"""

    # convert to iso format
    start_time = standardize_datetime(start_time)
    end_time = standardize_datetime(end_time)
   
    print(f"Fetching events between {start_time} and {end_time}")
    
    try:
        events = get_events(top_n, start_time, end_time)
        print(f"Events found: {len(events)}")
        
        if not events:
            print("No events between the given dates")
            return {"message": "No Events Found"}
        
        return {i: event for i, event in enumerate(events)}
            
    except Exception as e:
        print(f"Error in read_calendar: {e}")
        return {"error": str(e)}

@mcp.tool()
def create_events(
    summary: str,
    start_time: Optional[str],
    end_time: Optional[str],
    location: str=None,
    description: Optional[str]=None,
    attendees: Optional[List[dict]]=None
):
    """Create a new Google Calendar event with the provided details"""

    # convert to iso format
    start_time = standardize_datetime(start_time)
    end_time = standardize_datetime(end_time)
    timezone = get_localzone_name()
    
    event = {
        "summary": summary,
        "location": location,
        "description": description,
        "start": {
            "dateTime": start_time,
            "timeZone": timezone,
        },
        "end": {
            "dateTime": end_time,
            "timeZone": timezone,
        },
    }

    if attendees:
        event["attendees"] = attendees

    try:
        link = add_events(event)

        print("Successfully added event to calendar")
        return {"link": link}
    
    except Exception as e:
        print(f"Error in inserting event: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

    # events = read_calendar(
    #     start_time="4/11/2025",
    #     end_time="16/4/2025",
    #     top_n=10
    # )
    # print(events)
    

    # event = create_events(
    #     summary="Attendee Test",
    #     start_time="2025-04-13 21:00",
    #     end_time="2025-04-13 22:00",
    #     location="Online",
    #     description="Axel's Test. Hopefully works with Claude",
    #     attendees=[{"email": "glorianath20@gmail.com"}]
    # )
    # print(event)
    