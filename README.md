# Calendar-App
A basic web app that lets the user create a custom calendar (ics file) with his/her choice of Indian holidays.<br />

Run the flask-app.py file.

### How to use it:
1. After launching the app, select the desired holidays.<br />
![image](https://user-images.githubusercontent.com/37058545/118569314-5ccfd080-b797-11eb-82c6-867e61bee92e.png)
2. Click on the submit button below the table<br />
![image](https://user-images.githubusercontent.com/37058545/118569413-8983e800-b797-11eb-9ea2-9f11d6cc263a.png)
3. This will then show you the selections that you have made, if you are happy then you can proceed to get your unique ID for the desired selections, if unhappy then you can go back and change your selections.<br />
![image](https://user-images.githubusercontent.com/37058545/118569811-50984300-b798-11eb-83d6-d11f9706a422.png)
4. An ID is generated copy this ID and click on next. You can save this ID if ever want to download the same calendar again in the future.
5. Enter the ID and click on download, the ics file will be generated. <br />
![image](https://user-images.githubusercontent.com/37058545/118570169-327f1280-b799-11eb-920b-399b35e5277a.png)

## Updates
### v1.01 - 15/05/2021
1. Line 10 of generate_ics.py, a where clause was added to avaoid loading all the IDs in memory
2. Line 28 of the above file was modified to use prepared statements. Earlier string concatination was used.
3. Line 38 of the above file, comments were added.


 
