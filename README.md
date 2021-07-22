**Building the spiders**:

1.  Install Scrapy — their documentation is awesome. You should have no issues if you follow the [installation guide](https://docs.scrapy.org/en/latest/intro/install.html)

2.  Install dependencies: [boto]([installation guide](https://docs.scrapy.org/en/latest/intro/install.html)) (might already be installed depending on how you install Scrapy) & [dotenv](https://github.com/theskumar/python-dotenv) (this is to not check AWS secrets into our VCS)

3. Set up a new Scrapy project with `scrapy startproject directoryname`

You should have a `scrapy.cfg` file and a directory (named in the step above.) Inside of the directory, you’ll see what makes Scrapy tick. Primarily, we’ll be working with the `settings.py` and the `/spiders` directory.

Once you have your spiders up and running, the next step is to get your `settings.py` file set up correctly.

There is a fair amount of boilerplate code that Scrapy starts you out with. I’m only including the relevant parts I’ve changed. You’ll notice a couple of important things:

1.  We’re being good citizens of the internet by obeying robots.txt and manually checking Terms of Service of each site before we scrape. We don’t scrape sites who ask not to be scraped.
    
2.  We’re using dotenv to protect our AWS access key id and secret access key. This means you’ll have a .env file in the same directory as settings.py. You’ll want to include the .env in your .gitignore.
    
3.  The super legit part of Scrapy is that all you need are those couple of options set for it to handle pushing to S3.

Cool. We’ve got Scrapy all set. Spiders are built and settings.py is all set up to be pushing the data to S3 once we give it the correct credentials.


**Setting up AWS**:

AWS can be fairly intimidating if you’re not familiar with it. We need to do two things:

1.  Create an IAM user and get an access key id and secret access key
2.  Set up a bucket and add the correct permissions

IAM users can be a little tricky so I’d suggest reading AWS’s documentation. Essentially, you need to log into your AWS console, go into the IAM section, create a new user and generate an access key. I would recommend creating this user solely for the purpose of making API calls to your bucket. You’re going to need three strings from your created user. Save them somewhere safe.

  -  User ARN
  -  Access Key ID
  -  Secret Access Key

Now, let’s set up a new bucket. It’s pretty simple. Create your bucket and then navigate to the “Permissions” tab. You need to set a bucket policy that allows the IAM user you just created to push data to this bucket


**Deploy to ScrapingHub**:

[ScrapingHub](https://scrapinghub.com) is a nifty service run by the awesome folks that support Scrapy and a dozen or so other open source projects. It’s free for manually triggering spider crawls but it has a very reasonably priced $9 / month plan that allows for a single spider running concurrently at any given time. For our needs, it allowed us to schedule different spiders every 5 minutes i.e. 280+ unique spiders, as long as their run time is <5 minutes.


We’re in the home stretch. This part is easy. You’ll create a ScrapingHub account, log in, and generate an API key. You’ll (install)[https://github.com/scrapinghub/shub] `shub`, ScrapingHub’s CLI and follow the directions to add your key and project ID.

Once everything is set up you’ll use shub deploy to push your project to ScrapingHub.


The last thing you need to do is enter the Spider Settings area and manually add in the AWS credentials `AWS_ACCESS_KEY_ID` & `AWS_SECRET_ACCESS_KEY`. You’ll notice we also added a timeout  `CLOSESPIDER_TIMEOUT` to make sure we were failing gracefully if any errors occurred.

You’re done! Well, almost.


I’d recommend running your spider manually at least once first, checking your S3 bucket for the generated file and making sure you’re happy with all the results. Once you’re happy with that, go over to the Periodic Jobs section of your project and set your spiders to run at whatever intervals you need. E.g. Daily at 04:30 UTC.

