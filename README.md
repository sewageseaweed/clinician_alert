# Clinician Alert System
## Developer: Clyde Sumagang
This program is designed to poll an API that will retrieve the last known GPS location of a clinician, and determine if the they have left their designated zone. 

If they leave their designated zone, the service will send out an email alerting that they have left the zone.

If the there is an internal server error, or the API cannot be reached, the service will also send out an email regarding this error.

Due to the small number of clinicians (6), the service process the clinicians sequentially. However, I included a method to concurrently process the clinicians for it to be more scalable.

### TO DO IDEAS:
 - Aggregate alerts to reduce alert clutter?
    - Group by alert type?
    - Send alert when batch finishes processing?
 - If number of clinician increases, we will either have to scale wait time between requests/batches or round robin
 - Process ray casting in parallel?
 - Improve logging