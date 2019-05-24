DOCS
====
child: higher level abstraction task
parent: lower level abstraction task


IDEAS
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

- to add new todos, should write them on some temp list and then when I am at machine put them into the TODAG -> write them on google todo and then push to todag regulrarly ?
- OK feature request: priority of events coming up (need to be reminded)
- feature request: integrate outlook with TODAG

- metrics on mood -> productivity SHIPPED
- estimate of how much time is required for a task!

- time tracker, what did I do today? 

- OK when I have todos, I can 'check' or 'done'
- OK priority increases the less time I saw a card

- OK in the action I can do 'start' and a timer starts -> then check

- how long is required for a task? can put an additional arguement like python todo --available-time-to-work 2 hours
  and he chooses to give me tasks with that size

- ship mood feature to oana
- add time on mood dashboard, now is cool but I can't visually see time patterns since x axis is just 1 by 1 and not time scaled

- new feature-> log time without using the todo.py
 
 
 

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
  

ITERATION B
====
- [ ] add feature: events (facebook events, codeforces contests)
(more)
