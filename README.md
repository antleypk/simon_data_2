# simon_data_2
#take home test v2

Welcome to the etsy store analyzer v1.1.0

-- Operational Notes

    To operate the application, first clone the repo.

    After cloning the repo navigate to application folder.

    !!You must go to /application/secretdotkey and convert it to the proper file format to run the application!!

    Once in the src folder, execute 'app.sh' -> "you@yourmachine$ ./app.sh"

    This will call two python files: 'scraper.py', and 'analyzer.py'

            scraper.py: builds lists of companies to do analysis on. It saves
        the list in /application/data/shops_epocTimestamp.

            analyzer.py: finds the distribution of words found for a specific shop.
        It will either get the most recent list of shops, or can also take a epoch_timestamp
        as positional argument $1. The timestamp must be one from /application/data/shops_epocTimestamp.csv  
        analyzer.py saves the results at /application/data/distribution_epocTimestamp 

    The python files can be called multiple times; they do not need to be called together.

    scraper.py must run at least one time before analyzer.py can return meaningful results. 

    Due to relative file paths all files must be run from inside the application directory.

    configuration settings can be found in /application/config.py

-- Development Notes

    With regards to the take home assignment:
        -Fault tolerance: I elected to make two seperate scripts with a decoupled storage directory. I did this so that if connection fails at anytime the program fails cleanly. It also allows the user to run either part of the application as many times as desired. The program works if the ./data dir is erased. The application can create missing storage directories. The program also logs its progress and saves its findings in a human readable format. The logs are in ./data/logs.csv/ The next level of fault tolerance would be to create classes for shops and listings, and then save everything scrapped. 
    The next level beyond that would be to utilize S3, and aws based compute resources... Ideally Lambda because of the nature of this project. My machines harddrive is the weakest point in this system; moving to s3 would make our data safer.
        -Readability: I tried to follow python guidlines (lower case, with full words). I also used comments. I think this could have been improved with the use of Diagrams. 
        -Communication: It was a solo project. So the only Communication was with myself and the git comments. I should have used more feature based git. I did most of the project as developer based git instead of feature based git. Feature based is easier for observers to follow.  I did do one feature branch at the end. 
        -Automation:  I elected to make the entire project fully automated. Aside from git clone, and starting a script everything is fully automated.Everything is fully automated and fails gracefully if issues occur with the api. The next level of automation would require aws deployment. With AWS deployment sqs or another message broker could send messages to SES and warning messages could be sent to developers when failure occurs. Right now there is automated error logging and graceful failure. There is not developer alerting which is not ideal. 

    Classes: 
        I wanted to use a 'Shop' class. However the way it all turned out; I processed data row by row and never really needed to connect methods with data. If I was going to start over and had this project as a baseline. I think I would utilize a Shop.py class. I would use multi threading to populate all of the instances of the Shop, and then I would run the compute over them to analyze the word count. Then I would serialize the entire Shop and produce the aggretaion csv as two seperate outfiles. However without S3 that would start to make a decent amount of data and is slightly outside of scope of the given requirements.

