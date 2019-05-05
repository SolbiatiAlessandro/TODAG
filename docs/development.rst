The main development workflow can be found in the git commit messages.
This space is mainly for development ideas.

IDEAS
====
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


ITERATION A
==

Iteration started 05.05.2019, London

- [x] add feature: edit priority
- [x] fix feature: change questions
- [ ] add feature: events (facebook events, codeforces contests)
