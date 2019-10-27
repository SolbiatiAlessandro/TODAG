(what is this? this doc is about future ideas and how the development is going)

TODAG DEFINITIONS
=====
- child: higher level abstraction task
- parent: lower level abstraction task

IDEAS/SPARSE FEATURES
====
The main development workflow can be found in the git commit messages.
This space is mainly for development ideas.

- gamification: rewards to be considered as gems with higher and higher value, and to get the next gem the game become more difficult ('game of life?'), cfr. Ray Dalio Principles cap. 8, he speaks about this concept
- priority: every reward has a priority and I print the todos in order of the priority of their own reward, the idea is that I need to have tons of reward and when I want to do something I just iterates on the todos
- weight: every reward has a weight (not a priority), and the weight of the todo is the some of all the weight of all the rewards card it leads to
- deadline: need to implement some sort of control that let you add some deadline, and when deadline is approaching weight get higher and higher
- relevance: this idea of having weights on the graph and making it do the computation is great, but I should add some sort of  "distance" factor that express how relevant is the current todo with the goal reward. For instance: how relevant is doing leetcode problems to improve my daily life situation? Is not that relevant since the DAG goes like this : leetcode -> join google -> get experience -> build AI bot -> improve daily situation
- deadlines: so deadlines is an important part in the TODO process, now I am writing [DEADLINE] or [DUE DATE] in the name of the TODO and than when I get it as a current todo and today is not DUE DATE I skip it, let's think about how to integrate time dimension into TODAG
- notes: i like the feature to write 'why' and it tells me the components, would be nice to write 'notes' and I can input some notes and progress about the todo
- daily todo: what about when I start every morning I can write I sort of temporary todo queue that is parallel to the TODAG, to keep track of low level todo (buy this, do that, go there))
- recalibrate todag: change rewards and weight

- integrate TODAG with facebook calendar
- incorporate metrics
- move on cloud exposing APIs
- add TAGS, and make different TODOs in different part of the days
- not really tags but tree nodes 

- [ ] to add new todos, should write them on some temp list and then when I am at machine put them into the TODAG -> write them on google todo and then push to todag regulrarly ?
  
- [X] feature request: priority of events coming up (need to be reminded)
- [ ] feature request: integrate outlook with TODAG

- [X] metrics on mood -> productivity SHIPPED
- [ ] estimate of how much time is required for a task!

- [X] time tracker, what did I do today? 

- [X] when I have todos, I can 'check' or 'done'
- [X] priority increases the less time I saw a card

- [X] in the action I can do 'start' and a timer starts -> then check

- [ ] how long is required for a task? can put an additional arguement like python todo --available-time-to-work 2 hours
  and he chooses to give me tasks with that size

- [X] ship mood feature to oana
- [ ] add time on mood dashboard, now is cool but I can't visually see time patterns since x axis is just 1 by 1 and not time scaled

- [?] new feature-> log time without using the todo.py
 
- [ ] add 'take a break' for time counter

- add notification when mood updates come!
- [X] add float support for mood

- [ ] add  'gamification' for toing todag in terms of metrics
 
- [X] added 'do specific task' -> concept: 
1) is ok if you want to do something and todag let you do it
2) what is not ok is for you to 'pick something to do' from the todag

- [ ] technical vs non technical task, command line option? or location based?
  it was really nice today to go out in the park and do non-technical task. This might be a good solution for life-task. A temporary solution might be using location.
  -l 0.12 technical office task
  -l 0.10 techinical personal task
  -l (else) non technical task

- [ ] mood dashboard: put mood from the phone! not only from computer

- [ ] DATA STUDIO DASHBOARDS this are some ideas for the datastudio dashboard
  -> what is the current priority distribution on the todag?  (this work when is correctly calibrated) how urgent are the tasks
  -> how many different tasks of different kind are there
  -> how much did I work today? Day recap

-> single note feature, instead of editing on the terminal, why no having a actual text file that I edit with vim?

GAE TIME
dashboard now is being built on a webapp (read more here http://www.lessand.ro/10/post)

- [ ] write down iteration B for webapp
main ideas:
there are two routines, one is  (could be temporally combined at the end of day)
End Of Day Routine
 -> you see what you did during the day
 -> metrics and working hours

Start Of Day Routine
 -> you see what is planned for tomorrow
 -> todag prioritization gives you a draft and you can either confirm or modify it

-> put comments on the day, like the mood comments feature of datastudio?
-> track productivity, should integrate some chrome extension like toby. When I am working on the task am I actually working on the task or I got distracted by workpalce and so on
-> add count of tasks per day
-> for productivity is really interesting to intergrate chrome activity logger
-> also before come oana try to put metrics that I can use when I am with her

-> TODAG feature: when you search for cards make a feature like you can input the name of the card and he give you option for the code so you don;t need to copy paste all the time the card ID. this can be done in different part, in todo.py -t or in D.
-> D feature, improve the printing, show also code of card

-> planning is ok, but fix when todo.py go to next planning item. think how to do
-> checked plan on todag app

totally need to implement take a break
i need to think better about this taking a break , I often forget about it and just leave the logging going forever

-> now that I have this myactivity logging , I can add some sort of 'analyise task' because at time I do a task that is like 2 hours and I think: how could I spend this much time on this shit?

-> i often quit by accident the task, shuold quit with q not just pressing enter

reiterating on the take a break feature, how can  I detect when I close my laptop?
I  could send a signal that  i stop working when I close my laptop.
https://apple.stackexchange.com/questions/104486/macbook-air-pro-run-script-upon-lid-close

ITERATION A
====

Iteration started 05.05.2019, London

- [x] add feature: edit priority
- [x] fix feature: change questions

- [x] add feature: todo based on location

Location notes:
subprocess.check_output('/Users/lessandro/coding/SCRIPTS/whereami')
Longitude of house(Fabric) -> -0.1019
Longitude of office(Rathbone) -> -0.1305

- [x] add feature: record metrics on location and time

- [ ] infra upgrade: move the whole thing on cloud and expose APIs
sub tasks

infra upgrade
- GCP Storage to keep .pkl files for cards and .csv for logs
- GCP Function to have serverless API end points to call todo.py
- open.py will not be implemented in GCP Function but just keep on my local machine accessing data from GCP Storage

figured out a good calibration:
no need to figure out 'priority' every time, just add to parent,and set deadlines to daily tasks. e.g. PERSONAL (1) -> Codeforces (4) -> Contest (0) + deadline

- [ ] write tests before shipping to the cloud

- [ ] add feature: integration with Google Assistant to use todo

- [ ] think about some system to figure out: what increases my mood, what decreases my mood
  

OFFLINE ITERATION
========

(beginning)

Started offline branch.
it feels like going  offline was an amazing thing, I feel now
I focus more on product improvement compared to infra improvement. 
is really true that looking backward any bad things look like positive.

Now I am keeping the TODAG better shorter  then longer.
I keep few cards, I document them, and I write a lot of stuff.

You can see it as an evernote app with a prioritization schema , now I spend time
on the todag as planning. Do you remember in china when the todag started when I
had the idea of having planning/doing. Is this, now the planning is on the todag
and it makes a lot of sense.

- [ ] should I add a "elaboration session" where I actually write down stuff? Like what I think about the task. for instance social life, I had some great ideas, i would like not to write only the todo but also the ideas behind that. I could also use evernote, probably using evernote is better and just put a link as a 'launch and iterate'

 I am not sure how to find the balance between writing longer description or splitting cards. What  is exactly the cons of keeping all there? Too confused, I don't get focused on the single task I am working on. Should totally use a incremental process where the more it grows the more I split.

(2 weeks later, 18.08)
I have been using  it offline, it works, can be improved. Need to review my day so I can start allocating time for reflections and so on. 
Make  sure review day works,  if it doesn't work still do it manually. At the end of the review there is a metric computation momemnt
What to do in the review process? I would like to add some comments. Do I this on evernote? Or on the datamonitor

what about tracking specific staff.
I want to track sleep and meditation, I put specific bookmark when I create the event

(22.09)
Todag is going great. I am using a lot todo.py -t with arguemnt, and trying to get back to use todo.py.Documenting cards is great. 
Feature requests:
- more work on metric computation. Metric are computed in the weekly review. Extend work metric to all the week, add mood metric (that shhould be easy)
- tracking without timer (just start time and end time), without pressure
- ask about mood in task
- ask about productivity in thetask

(13.10)
Still using it, at times I use todo.py alone for office tasks.
IDEA: sunburst chart to represent todag, it read interactively from todag
Width is priority ? click open another subburst from a different node.
Every card has a mission, and that is the tooltip.
CURRENT FEATURES REQUEST:
- dashboard for time counter (4 work, 1 personal  a day)
- automatically write weekly recap
- open automaitcally links
- deadlines: instead of setting  deadlines write [MONDAY] and automatically parse prioritise /send notification

(27.10)
Using todag daily, reduced how much I use todo.py -t. I went to a really nice configuration of my cards.rd
I started offline journaling a lot, that looks like a good substitute for online journaling
Some new ideas I got watching videos about wunderlist/todoist:
- theme stuff (do ADMIN this on monday, PERSONAL PROJECT on Tuesday)
- take ideas by using wunderlist/todoist
- check how often I am using todo.py without argumenent -t


