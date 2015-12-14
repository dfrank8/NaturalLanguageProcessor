Douglas Franklin

Artificial Intelligence

Northeastern University: CS 4100

Final Project

Natural Language Processing: Can you spot evil?

Project Description:
Have you ever read something, and immediately knew that the writer was deranged, evil, cynical, sinister, or dangerous? The FBI has enormous branches dedicated specifically to criminal profiling through social media, blogs, and other publications. Could this monotonous tasks of reading countless blogs and posts be reduced using the help of a computer program? My project is meant to do exactly that. Using feature-based machine learning algorithms to process an enormous sample set of both “evil” and “good/pleasant/neutral” posts, my application will do its best to sort additional posts into “potentially threatening” or “not potentially threatening” categories. Most mass-murders have some sort of publication, and the safety of the public is the goal but identifying potential criminals before they commit any crimes. From a law-enforcement perspective, this technology could be incredibly dangerous (think of the movie Minority Report), but the results could still be very interesting. My prediction was I would find words such as “beautiful, love, joy” to be identifiable in the “good/pleasant/neutral” posts, and words such as “hate, death” in the “evil” posts. 
Other than stopwords, other lists of words were necessary for the feature-based learning software. www.enchantedlearning.com was a great resource, as it provided lists of vocab words, such as the one for weaponry-related terms, to be analyzed when processing the data. Other online searches were made as well to gather these lists. 
The main analysis will be done using a modified version of q-learning, where a database of writings will be analyzed at the start-up of the application, and features (listed below) will be applied. Then, when a new post is entered into the application, the app returns a score leaning towards “good” or “bad”, and adds it to the appropriate data set.  

Algorithms:
-	TF-IDF (Term Frequency-Inverse Document Frequency) and Stop-Word removal
o	TF-IDF is an algorithm that identifies significant words based on its frequency in a document, but can also ignore words if they occur frequently in documents it is grouped with. I paired this feature with a feature that removes stop-words (such as: “like, and, the, a, but”) from the documents, since these words would never be identifiable. 
-	Feature-based Q-Learning
o	This type of Q-learning is interesting because all the learning is done all at once out of the database. When a new state is introduced, the program determines the likelihood of the submission being the writing of someone dangerous. 
o	The afore-mentioned tf-idf results are an example of a feature that is stored and updated in the feature-based machine learning structure. 
o	Each feature is given a weight, which provides an overall prediction on whether or not a post is good/evil. 
o	List of features:
♣	Tf-idf results (word and its weight)
♣	Mention of names
♣	Mention of religious terms
♣	Mention of weapons/weaponry
♣	Mentions of Government

The analysis section is quite simple, if a word in the new blog is common in the previous database, it adds to the score relative to that word’s tf-idf score. Then, each density (by features mentioned above) are found for the new blog. Then, the densities in the database are compared to the blog’s densities. Based on the similarities, the score is updated as well. 

Concluding Remarks
Please, do not believe that this program actually has ANY conclusive results as to whether a person is going to do something drastic or crazy, or conversely, that they aren’t.  This was merely an experiment, and fun thing to do with some code, and a HW assignment. I hope you like it! Feel free to play around.

