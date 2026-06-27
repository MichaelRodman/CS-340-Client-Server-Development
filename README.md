# CS-340 Client/Server Development

Portfolio repository for CS-340 Client/Server Development coursework.

## Project Two: Grazioso Salvare Rescue Animal Dashboard

This repository includes my final dashboard code and Project Two README for CS-340. The project is an interactive dashboard for Grazioso Salvare that connects a Dash web application to a MongoDB animal shelter database. The dashboard allows users to filter animal records based on rescue dog profiles and view the results through an interactive data table, pie chart, and geolocation chart.

## Reflection

### How do you write programs that are maintainable, readable, and adaptable?

I write maintainable, readable, and adaptable programs by separating responsibilities, using clear naming, and keeping reusable code in its own module when possible. In this course, the CRUD Python module from Project One helped make the Project Two dashboard easier to manage because the database connection and query logic were separated from the dashboard layout and callback logic. Instead of writing MongoDB connection code repeatedly inside the dashboard, I could import the `AnimalShelter` class and use its `read()` method to retrieve data from the database.

This approach made the project easier to read and update. If the database connection details or CRUD operations needed to change, those changes could be made in the module instead of throughout the dashboard. In the future, the same CRUD module could be reused in other applications that need to connect to the animal shelter database, such as a reporting tool, an administrative dashboard, or another web application with different filters.

### How do you approach a problem as a computer scientist?

I approach problems as a computer scientist by first identifying the client’s requirements, then breaking the problem into smaller parts that can be designed, built, tested, and improved. For the Grazioso Salvare dashboard, I started by focusing on what the client needed: a way to identify dogs that matched specific rescue profiles. From there, I connected the dashboard to MongoDB, created queries for each rescue category, and tested that the dashboard widgets updated correctly.

This project was different from some earlier assignments because it required connecting multiple parts of a full client/server application. I had to think about the database, the Python CRUD module, the dashboard interface, and the user’s interaction with the system. In future database projects, I would use the same strategy of reviewing the client request, identifying the required data fields, designing queries around those requirements, and testing the results against realistic user needs.

### What do computer scientists do, and why does it matter?

Computer scientists design and build systems that solve real problems using data, software, and logical processes. This matters because well-designed software can help organizations work more efficiently and make better decisions. In this project, the dashboard helps a company like Grazioso Salvare search through animal shelter records more quickly than they could by manually reviewing the database.

The dashboard also makes the data easier to understand. Instead of requiring the user to write MongoDB queries, the application provides simple filter options and visual outputs. This kind of work can help a company save time, reduce errors, and focus on its mission. For Grazioso Salvare, that means identifying strong rescue dog candidates more effectively and supporting the organization’s search-and-rescue work.
