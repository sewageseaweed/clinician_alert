# Clinician Alert System
## Developer: Clyde Sumagang
This program is designed to poll an API that will retrieve the last known GPS location of a clinician, and determine if the they have left their designated zone. 

If they leave their designated zone, the service will send out an email alerting that they have left the zone.

If the there is an internal server error, or the API cannot be reached, the service will also send out an email regarding this error.

Due to the small number of clinicians (6), the service process the clinicians sequentially. However, I included a method to concurrently process the clinicians for it to be more scalable.

### Information:
- This program was develop using Python 3.12

### How To Run The Program:
- Change directories until youre in the root directory of the project. You can paste the following in your terminal:

    ```cd ~/clinician_alert/```
- In the root directory of the project, enter the following command in your terminal to run the program:

    ```python main.py```

    OR

    ```./scripts/run_program.sh```
- If the script doesn't run, you might have to give it execute permissions:
    
    ```chmod +x scripts/run_program.sh```

### To Run The Tests
- Change directories until youre in the root directory of the project. You can paste the following in your terminal:

    ```cd ~/clinician_alert/```
- In the root directory of the project, enter the following command in your terminal to run the program:
    ```./scripts/run_tests.sh```
- If the script doesn't run, you might have to give it execute permissions:
    
    ```chmod +x scripts/run_tests.sh```

### 

### TO DO IDEAS:
 - Aggregate alerts to reduce alert clutter?
    - Group by alert type?
    - Send alert when batch finishes processing?
 - If number of clinician increases, we will either have to scale wait time between requests/batches or round robin
 - Process ray casting in parallel?
 - Improve logging