### Postman Usage

Folliwng link can be used on postman to request data : 
`http://127.0.0.1:8000/api`

Constraints: 

Request type must be a POST
Body raw and JSON data type selected.
JSON example:
{
	"city": "johannesburg",
	"from_time": "20:45",
	"to_time": "23:50"
}

### Browser Usage:

Enter required inputs of city , start time and end time
Click on submit button to request the data from the API

Chart will be plotted below the form with the requested city weather data based on the hours interval 

On fail an alert message is displayed

#### Start and End time constraints

Start cannot be greather than End
End cannot be less than Start
Start cannot be less than the current time (no historical data)
Start and End has to be within the same day (hourly interval)