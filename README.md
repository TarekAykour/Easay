# Beautiful Essay - Easay

## About
gets all the docs and puts them nicely in one doc.
The titles of the docs/ the name files are used as subtitles as well as to apply it in the table of contents page. 

Also all the urls collected are made into APA generator. We first check if the URLs are in APA and 
if they are, we just put them inside the file, if they are not then we Apply APA. Also the First letter of the returned APA url will be checked and then sorted accordingly, so the list of urls are in alphabetical order


## Problem It solves
making it easier for students to combine their work into one beautiful and organized essay.
problem: students that experience chaos with delivering their school essays.
Students that have a hard time assembling all their school work or previous essays that need to be assembled into one document. 

Why not use ChatGPT?
Because chatgpt and a lot of LLMs don't allow for file upload w/o payment
as well the fact that they might change the contents of the files, because they were'nt 
prompt-engineered right. With Easay you don't need to worry about all that stuff. 
You simply upload your files and we will do the rest for you

## How it works - In One Sentence
select files> press upload > press convert > download the final file


## How it works
- upload files
- script reads each file and looks for the header. Compares header to filename.
- If they are similar then take the entire file content including the title
and create new doc (if its the first file being analyzed) to insert into it. 
- Convert the title to a subtitle and insert into indexpage
- if urls found, convert to APA and the put inside "sources" section.
If all urls inside file analyzed (as they come last in file) then move onto the next file uploaded
- repeat process until all files analyzed



### The more technical explanation of how it works
You upload files to the app. The app places them in a temporary folder
Then when you click on the convert button, the code does the following
- get the files and place them in a list
- iterate through the list
- we take the first document, check the filetype. If .rtf then we execute code to read
the title, paragraph, images, etc. 
- To check the title of .rtf we check for the /fs24 or greater. We take that and insert into
titles array and convert it to fs22. Then we also check for the Url. If a paragraph has a http:// or HYPERLINK 
then we take that line and insert in Links array.
- we then insert all the contents of the file except for the url section of the file inside the new document

### The code structure
- a component for reading .rtf
- a component for reading .doc
- at the convert function inside app.py we check if the file is doc or rtf
- 



## Ideas
Image identification to place it in the right place. 

## Potential technologies

[look at genAI of IBM in OneNote for AI tools]

- Flask (backend) <- because fast and simple>
- Bootstrap (frontend) <-because fast and simple>
- Vue.js (frontend) <- because fast and simple>
- Bs4 <- simplicity>
- pylint
- codeium <- AI coding assistant tool
- docx

## Folder structure
- backend <- where the app.py is>
- components <- python files handling files & making the one final file>
- static <- js, css, images are here>
- templates <- where the pages of the webapp are stored>


## technical notes
16-6-24 make CI-CD pipeline to deploy quick and fast after changes in log.
        Create AI-generated LOGs when applying changes

17-6-24 flask --app example_app.py --debug run (works like nodemon for nodejs)
17-6-24 Converting figma design to HTML/CSS (saves time in development)





## Business process

- was reading book
- generating ideas
- was thinking about my own problems
- i had problem with delivering evidence for my endassessment
- wrote the idea done as url-apa generator
- expanded to combine files into one beautiful file with additional features
- created figma design



## The design

### The image
![alt text](image.png)


### Figma file
`<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450" src="https://www.figma.com/embed?embed_host=share&url=https%3A%2F%2Fwww.figma.com%2Fdesign%2F6adktb5CKbD1Gg4ERv02NC%2FBeautiful-Essay%3Ft%3DD8kSqhomsShOiPZ9-1" allowfullscreen></iframe>`


## Problems during developent and their solutions
17-6-24     Wanting to upload multiple files and display them on screen
            **solution**: reading the .files property of the input and listing the files in an *<ul>*

17-6-24     Generating HTML through JS after change on file-input or easier way by displaying it as
            block when input-file changes and none if nothing happens.

18-6-24     Added id=list attribute to ul, so we can get the ul by id and read its
            contents. 
            Appending the newly geenrated container, but need to prepend it. Instead appended it

18-6-24     Once file uploaded. We look at the fs-value of the text. If fs-value above fs28 then it is  a title. If between fs24-fs28 then subtitle and everyting below is the content. 
Links will be detected by reading 'HYPERLINK', we get the url and convert it to APA. 



18-6-24    Now the next step is to upload file to server.
           In JS we take the list of files uploaded and send it to /uploadfile.


19-6-24    Handling file requests with axios, couldn't use require and was too lazy to figure it out, so i used fetch instead. Upon fetching the files or uploading a new file, we check if the file is already in the list of files, if it is then we throw alert otherwise we upload file. 


19-6-24   Created a form inside JS to handle convert. appended btn to form and form to
          "uploaded files" container

19-6-24   Ran into problem reading docx content file. RTF files are being read well...
          **solution**: docx package

19-6-24   Need to know what text is the content and which is the title. Also need to check if
          file is empty. 
          
          **solution**: paragraph starts line with \fs22 and ends with \par
          if after \par there is another \par then its an another paragraph.
          

          For url if "fldinst"found and right after "{HYPERLINK" then read the entire url
          until the first "}" is found, take the URL and covert to APA> insert into new URL section
          in final file if it exists, otherwise create the section. Then move onto next URL


21-6-24   identify .doc  and use the textprocessor library to print out lines.
          For .Rtf files instead of using the library, used regex to identify paragraphs, titles, subtitles and urls.

22-6-24   For converting the url to APA. Scribbr API might be the solution. Or perhaps   webscrape? But that is a lot of effort for something that should not take that long


24-6-24 Added multiple regex matching to extract the title

25-6-24 Removing Unnecessary "Urls", "Links", characters and spaces

25-6-24 APA generator with beautifulsoup. Scrape the author, title, pub_date from url
        Insert them into an APA-formatted citation

26-6-24 Handling Images. Tried with bs64 and failed. Will update later

27-6-24 Finishing touches. SEO, error handling



## Deployment issues
Issue                                                   Solution
Too much memory used during file upload                 Only install packages you used during project
in Pythonanywhere

configuring static files                                Make sure to use directory of the webapp
                                                        SO /home/username/mysite/static. Put this
                                                        Inside the app.py and other .py files where you
                                                        need to access dirs


Files of other users displaying                  




## Challenges
- Getting back with Flask. After a full year with Django and building full-stack applications with it, I had to get a little used to how flasked worked and the different workflow it brought with it. Luckily for me, Flask is easy to use and very minimal. Which is why i chose it for this project

- Working with Regex. Since the moment I have been aware of Regex, I have been skipping it till this moment. The syntax gives me nightmares, but it is very powerful once you know how to use it. And it can simplify the code a lot by using pattern matching instead of using dozens of if-else statements. 




## SEO
on-page SEO (title and description based on google results)
off-page SEO (added meta-data for twitter & facebook)


## optional
- spellingcheck -/ grammarcheck
- styling of the final doc
- sentence/paragraph predictor