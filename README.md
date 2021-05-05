# Wave Software Development Challenge

Applicants for the Full-stack Developer role at Wave must
complete the following challenge, and submit a solution prior to the onsite
interview.

The purpose of this exercise is to create something that we can work on
together during the onsite. We do this so that you get a chance to collaborate
with Wavers during the interview in a situation where you know something better
than us (it's your code, after all!)

There isn't a hard deadline for this exercise; take as long as you need to
complete it. However, in terms of total time spent actively working on the
challenge, we ask that you not spend more than a few hours, as we value your
time and are happy to leave things open to discussion in the on-site interview.

Please use whatever programming language and framework you feel the most
comfortable with.

Feel free to email [dev.careers@waveapps.com](dev.careers@waveapps.com) if you
have any questions.

## Project Description

Imagine that this is the early days of Wave's history, and that we are prototyping a new payroll system API. A front end (that hasn't been developed yet, but will likely be a single page application) is going to use our API to achieve two goals:

1. Upload a CSV file containing data on the number of hours worked per day per employee
1. Retrieve a report detailing how much each employee should be paid in each _pay period_

All employees are paid by the hour (there are no salaried employees.) Employees belong to one of two _job groups_ which determine their wages; job group A is paid $20/hr, and job group B is paid $30/hr. Each employee is identified by a string called an "employee id" that is globally unique in our system.

Hours are tracked per employee, per day in comma-separated value files (CSV).
Each individual CSV file is known as a "time report", and will contain:

1. A header, denoting the columns in the sheet (`date`, `hours worked`,
   `employee id`, `job group`)
1. 0 or more data rows

In addition, the file name should be of the format `time-report-x.csv`,
where `x` is the ID of the time report represented as an integer. For example, `time-report-42.csv` would represent a report with an ID of `42`.

You can assume that:

1. Columns will always be in that order.
1. There will always be data in each column and the number of hours worked will always be greater than 0.
1. There will always be a well-formed header line.
1. There will always be a well-formed file name.

A sample input file named `time-report-42.csv` is included in this repo.

### What your API must do:

We've agreed to build an API with the following endpoints to serve HTTP requests:

1. An endpoint for uploading a file.

   - This file will conform to the CSV specifications outlined in the previous section.
   - Upon upload, the timekeeping information within the file must be stored to a database for archival purposes.
   - If an attempt is made to upload a file with the same report ID as a previously uploaded file, this upload should fail with an error message indicating that this is not allowed.

2. An endpoint for retrieving a payroll report structured in the following way:

   _NOTE:_ It is not the responsibility of the API to return HTML, as we will delegate the visual layout and redering to the front end. The expectation is that this API will only return JSON data.

   - Return a JSON object `payrollReport`.
   - `payrollReport` will have a single field, `employeeReports`, containing a list of objects with fields `employeeId`, `payPeriod`, and `amountPaid`.
   - The `payPeriod` field is an object containing a date interval that is roughly biweekly. Each month has two pay periods; the _first half_ is from the 1st to the 15th inclusive, and the _second half_ is from the 16th to the end of the month, inclusive. `payPeriod` will have two fields to represent this interval: `startDate` and `endDate`.
   - Each employee should have a single object in `employeeReports` for each pay period that they have recorded hours worked. The `amountPaid` field should contain the sum of the hours worked in that pay period multiplied by the hourly rate for their job group.
   - If an employee was not paid in a specific pay period, there should not be an object in `employeeReports` for that employee + pay period combination.
   - The report should be sorted in some sensical order (e.g. sorted by employee id and then pay period start.)
   - The report should be based on all _of the data_ across _all of the uploaded time reports_, for all time.

As an example, given the upload of a sample file with the following data:

   | date       | hours worked | employee id | job group |
   | ---------- | ------------ | ----------- | --------- |
   | 2020-01-04 | 10           | 1           | A         |
   | 2020-01-14 | 5            | 1           | A         |
   | 2020-01-20 | 3            | 2           | B         |
   | 2020-01-20 | 4            | 1           | A         |

A request to the report endpoint should return the following JSON response:

   ```json
   {
     "payrollReport": {
       "employeeReports": [
         {
           "employeeId": "1",
           "payPeriod": {
             "startDate": "2020-01-01",
             "endDate": "2020-01-15"
           },
           "amountPaid": "$300.00"
         },
         {
           "employeeId": "1",
           "payPeriod": {
             "startDate": "2020-01-16",
             "endDate": "2020-01-31"
           },
           "amountPaid": "$80.00"
         },
         {
           "employeeId": "2",
           "payPeriod": {
             "startDate": "2020-01-16",
             "endDate": "2020-01-31"
           },
           "amountPaid": "$90.00"
         }
       ]
     }
   }
   ```

We consider ourselves to be language agnostic here at Wave, so feel free to use any combination of technologies you see fit to both meet the requirements and showcase your skills. We only ask that your submission:

- Is easy to set up
- Can run on either a Linux or Mac OS X developer machine
- Does not require any non open-source software

### Documentation:

Please commit the following to this `README.md`:

1. Instructions on how to build/run your application
1. Answers to the following questions:
   - How did you test that your implementation was correct?
   - If this application was destined for a production environment, what would you add or change?
   - What compromises did you have to make as a result of the time constraints of this challenge?

## Submission Instructions

1. Clone the repository.
1. Complete your project as described above within your local repository.
1. Ensure everything you want to commit is committed.
1. Create a git bundle: `git bundle create your_name.bundle --all`
1. Email the bundle file to [dev.careers@waveapps.com](dev.careers@waveapps.com) and CC the recruiter you have been in contact with.

## Evaluation

Evaluation of your submission will be based on the following criteria.

1. Did you follow the instructions for submission?
1. Did you complete the steps outlined in the _Documentation_ section?
1. Were models/entities and other components easily identifiable to the
   reviewer?
1. What design decisions did you make when designing your models/entities? Are
   they explained?
1. Did you separate any concerns in your application? Why or why not?
1. Does your solution use appropriate data types for the problem as described?



## Instruction

ARCHITECTURE


Clone the repo:

    git clone https://github.com/bonzanini/flask-api-template
    cd backend

Create virtualenv:

if using python2, run
``virtualenv venv ``

if using python 3, run
``python3 -m venv env``
     
    source venv/bin/activate
    pip install -r requirements.txt
    python setup.py develop # or install if you prefer

Run the server from root directory

    gunicorn -b 0.0.0.0:8000 --access-logfile - "backend.app:create_app()"

Try the endpoints:
    
    File upload endpoint:
    Use the sample UI at https://localhost:8000/
    
    PayrollReport endpoint:
    curl -XGET http://localhost:8000/timereport/payrollReport
    


How did you test that your implementation was correct?
    ``File Upload: ``
    
``To test the file upload end-point, I have created a simple UI for the user to mimic the upload functionality and succfully upload the csv file. This also handles error checking if report with the same ID has already been inserted.``
    
``Payroll Report: ``

``Test classes have been written to cover the complete functionality this endpoint.``

If this application was destined for a production environment, what would you add or change?
`concern 1: To dockerize the application to make it more sustainable`

`concern 2: Add more test cases on the file-upload endpoint ensuring a good test coverage and increase confidence in codebase`

`concern 3: Switch Front-End structure to REACT for modularity and scalability`

`concern 4: Move database to the cloud rather than having it locally stored`

`concern 5: Add user logins for securing access to the platform`

What compromises did you have to make as a result of the time constraints of this challenge?
`1: Use Flask Blueprints as a UI rather than REACT framework`
`2: Lack of modulairty within the endpoints codebase`
`3 Upload endpoint not completely robust, cannot be tested with a file being sent form a cURL POST request`
`4: Use Sqlite3 database, since its easy to setup, but maybe of an issue if space is of concern`


Codbase Structure

**blueprints:** folder contains files for the front-end aspect of the application
**lib:** folder contains various utils helper files
**database:** folder contains Sqlite3 database
**cli:** folder contains helper CLI commands for running tests

    ├── backend
    │ ├── app.py
    │ ├── blueprints
    │ │ ├── page
    │ │ │ ├── templates
    │ │ │ │ └── page
    │ │ │ │ └── home.html
    │ │ │ └── views.py
    │ │ └── timereport
    │ │ ├── __init__.py
    │ │ └── models.py
    │ ├── database
    │ │ ├── payroll.db
    │ │ └── payroll.db_test
    │ ├── extensions.py
    │ ├── lib
    │ │ ├── tests.py
    │ │ ├── util_json.py
    │ │ ├── util_logger.py
    │ │ └── util_sqlalchemy.py
    │ ├── static
    │ │ └── css
    │ │ └── main.css
    │ ├── templates
    │ │ └── layouts
    │ │ └── base.html
    │ └── tests
    │ ├── __init__.py
    │ ├── conftest.py
    │ ├── pages
    │ │ ├── __init__.py
    │ │ └── test_pages.py
    │ └── timereports
    │ ├── __init__.py
    │ ├── test_models.py
    │ └── test_views.py
    ├── config
    │ ├── __init__.py
    │ ├── sample_data
    │ │ ├── time-report-42.csv
    │ │ └── time-report-43.csv
    │ └── settings.py
    └── requirements.txt
