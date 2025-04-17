import asyncio
import aiohttp
import os
import time
from data.clinician_zone_status import clinician_status_map
from email_service.send_email import send_email
from polygon_helpers.polygon_helpers import is_outside_polygon

async def get_clinician(client_session, limiter, clinician_id):
    print(clinician_status_map)
    url = os.getenv("URL") + str(clinician_id)
    try:
        async with limiter:
            async with client_session.get(url, timeout = 3, raise_for_status = True) as response:
                json = await response.json()
                #Ran into case where response successfully returned, but JSON was {"error" : "internal server error"}
                if 'error' in json:
                    print(f'Error in json: {json['error']}')
                    raise ValueError(f"API call returned error: {json['error']}")
                #Ran into case where features was missing from JSON, indicating there were no coordinates
                if 'features' not in json:
                    print('Feature missing from JSON: ', json)
                    raise ValueError(f"Missing 'features' in JSON response for clinician {clinician_id}")
                if clinician_status_map[clinician_id]['error']:
                    clinician_status_map[clinician_id]['error'] = False
    except Exception as e:
        print(f'Request to fetch Clinician {clinician_id} failed: {repr(e)}')
        #Alert about error when polling
        if not clinician_status_map[clinician_id]['error']:
            sent = await send_email(f'Error Occurred While Polling Clinician {clinician_id}',\
                f'An error had occurred while polling for Clinician {clinician_id}: {repr(e)}')
            if sent:
                clinician_status_map[clinician_id]['error'] = True
        return False
    
    point, polygons = [], []
    
    #Gather last known point of clinician, and the coordinates for their zones
    for feature in json['features']:
        if feature['geometry']['type'] == 'Point':
            point = feature['geometry']['coordinates']
        else:
            for coordinates in feature['geometry']['coordinates']:
                polygons.append(coordinates)
    
    #Only notify when a clinician goes from being in the zone to outside the zone
    clinician_outside = is_outside_polygon(point, polygons)
    
    #If clinician is outside, when they were previously in the zone, send an email. 
    #Else if theyre inside, but in-zone is False, reset it back to True
    if clinician_outside and clinician_status_map[clinician_id]['in-zone']:
        await send_email(f'Clinician {clinician_id} Departed', \
            f'The clinician with id: {clinician_id}, has left the expected zone. Last known coordinates: {point}')
        clinician_status_map[clinician_id]['in-zone'] = False
    elif not clinician_outside and not clinician_status_map[clinician_id]:
        clinician_status_map[clinician_id]['in-zone'] = True
    return True

#Run an indefinite loop for each clinician id. Used for running concurrently
async def loop_clinicians(client_session, limiter, id):
    while True:
        await get_clinician(client_session, limiter, id)

#Process clinicians cocurrently, better for scaling to a large number of clinicians. More resource intensive
async def poll_clinicians_concurrently(limiter):
    async with aiohttp.ClientSession() as client_session:
        while True:
            start_time = time.time()
            tasks = [asyncio.create_task(loop_clinicians(client_session, limiter, id)) for id in range(1, 7)]
            await asyncio.gather(*tasks)
            elapsed = time.time() - start_time
            #If more than 1 second has passed since the last run, then start next batch immediately, else wait up to 1 second
            await asyncio.sleep(max(0, 1 - elapsed))

'''
TODO:
- Aggregate alerts to reduce alert clutter?
  - Group by alert type?
  - Send alert when batch finishes processing?
'''
#Process clinicians sequentially. Good for the assessment as it takes ~1 second to process 6 clinicians, resulting in 360 queries per minute
async def poll_clinicians_sequentially(limiter):
    async with aiohttp.ClientSession() as client_session:
        while True:
            for id in range(1, 7):
                await get_clinician(client_session, limiter, id)
                await asyncio.sleep(.1)