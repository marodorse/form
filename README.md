# Project: Form in Python with Flask

  

## Problem statement:

The company Hackers Poulette™ sells DIY kits and accessories for Rasperri Pi. They want to allow their users to contact their technical support. Your mission is to develop a Python script that displays a contact form and processes its response: sanitization, validation, and then sending feedback to the user.

  

## Performance criteria:

* If the user makes an error, the form should be returned to them with valid responses preserved in their respective input fields.

* Ideally, display error messages near their respective fields.

* The form will perform server-side sanitization and validation.

* If sanitization and validation are successful, a "Thank you for contacting us." page will be displayed, summarizing all the encoded information.

* Implementation of the honeypot anti-spam technique.

  

#### Form fields

First name & last name + email + country (list) + message + gender (M/F) (Radio box) + 3 possible subjects (Repair, Order, Others) (checkboxes). All fields are mandatory, except for the subject (in this case, the value should be "Others").

  

## Contact Form (Python)

* Presentation: server/client architecture (transmissive, 10")

* Sanitization: neutralizing any harmful encoding (<script>)

* Validation: mandatory fields + valid email

* Sending + Feedback

* NO NEED FOR JAVASCRIPT OR CSS

----------------------------------------------------------------

  

## Project Overview

  

This project utilizes several Python libraries and frameworks to create a web application for handling contact form submissions securely.

  ----------------------------------------------------------------

Libraries Used:

**FastAPI**

FastAPI is used as the main web framework to handle HTTP requests and responses efficiently.

**Jinja2Templates**

Jinja2Templates is used for server-side HTML templating, allowing dynamic rendering of HTML pages with data from the backend.

**SQLAlchemy**

SQLAlchemy is employed for database management, providing an ORM (Object-Relational Mapping) to interact with the SQLite database.

**Uvicorn**

Uvicorn is the ASGI server used to run the FastAPI application, facilitating concurrent handling of HTTP requests.

**Bleach**

Bleach is used for sanitizing HTML inputs, ensuring that only safe HTML elements and attributes are allowed to prevent XSS attacks.


----------------------------------------------------------------
## Security Measures :
Protection Against XSS and SQL Injection Attacks :

1. Input Sanitization with Bleach:

  - Bleach is utilized to sanitize user inputs susceptible to HTML injections, ensuring that any potentially dangerous HTML tags or attributes are removed before rendering.

> ``# Example of using bleach for HTML sanitization in FastAPI application``
> 	``first_name = bleach.clean(first_name, strip=True)``
> 	``last_name = bleach.clean(last_name, strip=True)``
> 	``email = bleach.clean(email, strip=True)``
> 	``continent = bleach.clean(continent, strip=True)``
> 	``message = bleach.clean(message, strip=True)``

2. Parameterized Queries with SQLAlchemy:

- Parameterized queries are used to interact with the SQLite database, ensuring that user inputs are properly escaped to prevent SQL injection attacks.
> `# Example of parameterized queries with SQLAlchemy`
> `contact = Contact(`
>     `first_name=first_name,`
>     `last_name=last_name,`
>     `email=email,`
>     `continent=continent,`
>     `message=message,`
>     `gender=gender,`
>     `subject=subject`
> `)`
> `db.add(contact)`
> `db.commit()`

3. Protection Against XSS Vulnerabilities

- Contextual Escaping with Jinja2Templates:**
    - Jinja2Templates automatically performs contextual escaping when rendering templates, preventing XSS vulnerabilities by encoding HTML entities in user inputs.

----------------------------------------------------------------

### Difference Between POST and GET Requests

1. **POST Request:**
    
    - POST requests are used to submit data to be processed to a specified resource. In this project, POST requests are employed when users submit the contact form with their information. The data is sent in the request body.
	    - @app.post("/")
		async def process_form(...):
2. **GET Request:**

	- GET requests are used to request data from a specified resource. In this project, GET requests are used to initially render the HTML form page for users to view and fill out.
		@app.get("/")
		def get_form(...):
    ...
----------------------------------------------------------------
### Honeypot and Anti-Spam Technique

1. **Honeypot Field:**
    - A honeypot field named `website` is added to the form but hidden from regular users. If this field is filled out (indicating a bot), the form submission is flagged as potential spam.
	    - # Honeypot field in the FastAPI form handling
	if website:
	    errors["message"] = "Spam detected"
	    return templates.TemplateResponse("errors.html", {"request": request, "errors": errors})
