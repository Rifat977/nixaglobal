



Assalamualaikum, I'm Abdullah Al Mamun, Department of Software Engineering in Daffodil International University. I've developed a Spring Boot project for managing DIU student information and results. Today, I'd like to take a few minutes to show the code of our Student Result Web Application and explore how it usage Object-Oriented Programming (OOP) concepts to achieve its functionality.

This App class serves as the entry point for the Spring Boot application.
It contains the main method, which is the starting point for the Java application.

The HomeController class implicitly inherits from the Spring Framework's Controller class.
The code encapsulates related functionalities within the HomeController class.
Private fields, such as studentResultRepository, are encapsulated within the class and accessed through public methods.

In the repository pattern, the StudentResultRepository interface extends JpaRepository as abstraction.


The @GetMapping and @PostMapping annotations demonstrate polymorphic behavior, allowing different HTTP methods to be handled by the same HomeController class.


The showForm method handles rendering HTML templates on a Get Request to the root URL, aligning with encapsulation principles.

The makeApiCalls method showcases polymorphism, handling different parameter types like RequestParam and Model.

The code addresses potential IOExceptions during IO operations, reflecting careful exception handling.

Utilizing the RestTemplate class abstracts the complexity of HTTP requests, promoting efficiency.

In the model directory, the StudentResult class defines database columns using encapsulation with getter and setter methods.

