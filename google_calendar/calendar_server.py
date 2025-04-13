from datetime import datetime
from dateutil import parser
from tzlocal import get_localzone_name
from mcp.server.fastmcp import FastMCP

from calendar_functions import * 

mcp = FastMCP("Calendar Helper")

@mcp.tool()
def calendar_read_events(
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
        events = read_event(start_time=start_time, end_time=end_time, top_n=top_n)
        print(f"Events found: {len(events)}")
        
        if not events:
            print("No events between the given dates")
            return {"message": "No Events Found"}
        
        return {i: event for i, event in enumerate(events)}
            
    except Exception as e:
        print(f"Error in read_calendar: {e}")
        return {"error": str(e)}

@mcp.tool()
def calendar_create_events(
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
        link = create_event(event=event)

        print("Successfully added event to calendar")
        return {"link": link}
    
    except Exception as e:
        print(f"Error in inserting event: {e}")
        return {"error": str(e)}

@mcp.tool()
def calendar_update_events(event: dict, changes: dict):
    """Update a Google Calendar event"""

    event.update(changes)
        
    try:
        update_event(event=event)
        print("Successfully updated event in calendar")
        return {"message": f"Updated {event['summary']} in calendar"}
    
    except Exception as e:
        print(f"Error in updating event: {e}")
        return {"error": str(e)}

@mcp.tool()
def calendar_delete_events(event: dict):
    """Delete a Google Calendar event"""
    try:
        delete_event(event=event)
        print(f"Successfully deleted {event["summary"]} from calendar")
        return {"message": f"Deleted {event['summary']} from calendar"}

    except Exception as e:
        print(f"Error in deleting event: {e}")
        return {"error": str(e)}
       


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
