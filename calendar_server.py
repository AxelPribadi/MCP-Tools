from datetime import datetime
from dateutil.parser import isoparse
from mcp.server.fastmcp import FastMCP

from calendar_functions import * 

mcp = FastMCP("Calendar Helper")

@mcp.tool()
async def read_calendar(
    time_start: str,
    time_end: str,
    top_n: int
) -> dict:
    """Read Google Calendar events from a selected timeframe (in ISO Date Format)"""
    print(f"Fetching events between {time_start} and {time_end}")
    try:
        events = get_events(top_n, time_start, time_end)
        print(f"Events found: {len(events)}")
        
        if not events:
            print("No events between the given dates")
            return {"message": "No Events Found"}
        
        return {i: event for i, event in enumerate(events)}
            
    except Exception as e:
        print(f"Error in read_calendar: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
