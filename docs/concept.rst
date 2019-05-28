 What's the idea behind TODAG?
Build a tool that can help the planning of activities on any time-scale, and is able to embrace and reflect the abstraction of complex decision trees.

The TODO process
=======================================================


1 - The TODO process is the activity of planning ahead starting from the goals we want to set, and backtraing to the current moment, specifying a more or less detailed path with the 'TODO' actions that need to be done to achieve the goal. This can be on everytime scale, days, weeks, months or years.

2 - The TODO process is often not given enough importance, since we are commonly distracted by our day-to-day activites, is hard to dedicate enough energy to the analysis of the 'bigger picture', i.e. a long term planning. On the other hand, the reward given by the TODO process are considerably high, mainlyconsiting in a substancial life-situation improvement of the human user.

3 - The TODO process is a deterministic process that can be represented with analytical tools in a relatively straightforward way: is common to find TODO-list applications/utilites. A closer representation to the actual structure of TODO planning is a decision tree, instead of a list. This is the concept behind TODAG.

4 - The TODO process can be improved substantially in both quality and efficiency, using a computer aided tool for the representation and analysis of the decision tree. This improvement comes from the fact that the 'computationally expensive part' of analysing the decision tree is left to the machine, whereas is left for the human user only the practical side of executing the TODOs told by the machine.

===========================================================
First part of the process - Populating the decision tree
===========================================================

The population of the decision tree is the more abstract, and is the one that mainly imporves the quality of the TODO process. 

1 - Stating clearly the goals the will give a desired reward will increase the chance of achieving them, improving the overall life situation for the user

2 - Populating the compelete decision tree that leads to these rewards will give a feedback system to validate what part of the process has already been executed, and how long is takes to reach the reward.

The user-cases for the first part of the TODO process are visualize the decision tree, and modify it. The implementation of these user-cases is found in bin/open.py

===========================================================
Second part of the process - Runtime execution of the TODOs
===========================================================

The runtime execution part of the process needs to be as less-distracting, computationally efficient as possible for the human user. The workflow must look like this:

| USER QUERIES THE TODAG -> THE TODAG GIVES BACK A TODO -> USER EXECUTES TODO or USER REQUEST A DIFFERENT TODO | 

The whole efficiency of the TODAG workflow is that the whole energy of the user will be concentrated in executing the TODO without questioning or analysisng the decision tree at 'runtime'.

The implementation of the above mentioned workflow is found in bin/todo.py

=======================================================
Reflections after using the TODAG for more then 6 months
=======================================================

The first strength of the TODAG is when it makes you do things that you would otherwise not do. Remember, your evaluation of priority is often biased, whereas TODAG is not. Adding timing counter if you don't want to do something you can just do it for 1 minute just to check it. This on the long run really makes a difference on what you get done in your life, especially regarding the small things.

The second strength of the TODAG is that is SO easy to get distracted if you don't use it. Your activity flow start digressing, LinkedIn, github, Twitter.. Even if is work related it still not focused and not productive. TODAG + the counter really gives you an amazing productivity boost
