### Represent complex data on a Heat Map

<br/>
Simple application to visualize road accidents in the city of Lille. I recovered an open source database of past road accidents with conditions.
<br/>
<br/>

### Accident Database :

| Table        | Data Example |
| ---------------- | --------------------- |
| Cause    |Intersection, Passing, Parking, Drunkenness... |
| Date     |1985-01-07 18:10:00, 1999-10-10 17:10:00, 1998-02-25 06:55:00... |
| Condition|Moist, Wet, Freezing, Snow cover, Muddy Fat... |
| Involved |Bicycle, Bus, Light car, truck, Pedestrian minus 10 years... |
| Weather  |Fair weather, Heavy rain, Snow, Strong storm wind, Mist... |
| Location |Latitude (10430), Longitude(10430)...|
| Brightness|Half day, Light night, Insufficient night light, Night without lighting... |
|Risk      |Normal, Dangerous, Very Dangerous... |
|Involvement|Human, Two wheels, Vehicle, Other reason... |

<br/>
I connect to the database using the python library named pymysql 


```python
import pymysql
conn = pymysql.connect(host="localhost",
                       port=3306, user="root",
                       passwd="root",
                       database="Accident_Database")
cursor = conn.cursor()
```
<br/>


In the first menu we find a brief description with two buttons, the user can choose a static or dynamic map. In the second menu the user chooses the weather, brightness and the month of the year of the accidents he wants to consult
<img src="/data/menu.png"/>

Once the parameters are validated, it is executed in the database and a dataframe (pandas library) is loaded with the result of the query, that is to say all the accidents corresponding to the parameters chosen

```SQL
SELECT MLieu.x,MLieu.y,(nb_morts*10+nb_blesses_graves*5+nb_blesses_legers) AS gravite 
	    FROM MAccident 
			JOIN MLieu ON MLieu.lieu_id=MAccident.lieu_id 
			JOIN MLuminosite ON MAccident.lum_id=MLuminosite.code 
			JOIN MIntemperie ON MIntemperie.code=MAccident.intemp_id 
			JOIN MDate ON MDate.date_id=MAccident.date_id 
		WHERE MLuminosite.libelle_luminosite=:luminosite 
			AND MIntemperie.libelle=:libelle 
			AND MONTH(MDate.DateFormatStandard)=:month;
```

<br/>
The severity of the accident is weighted by the number of serious injuries and fatalities.

Each accident is represented by a heat point which is more or less important depending on the severity

These heat points are placed on a layer according to their coordinates. The city map in the background is positioned in the same coordinate as the heat layer 


<a href="https://imgur.com/R3x9eQs"><img src="https://i.imgur.com/R3x9eQs.png" title="source: imgur.com" /></a>



### Here is the Result : "https://www.youtube.com/embed/W0pJmPhz6oo" 

Evolution of accidents over the months

Zoom in on an accident
