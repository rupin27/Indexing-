# Indexing Implementation
<p>
The purpose of this project is to explore indexing and query processing on a small collection of documents with Positional Information.
</p>

# Downloading Dependencies:
<p>
Download the zip and you will find the following components in file: 
</p>

<pre>
1) <b><i>src/*</b></i> : Contains the source code, source text, and a test file to check input the query.
               a)invertedIndex.py
               b)shakespeare-scenes.json: This dataset has been preprocessed by stripping out punctuation and using the Krovetz Stemmer. 
                                          No stopwords have been removed.
               c)input.txt 
              
The results from various test queries are returned as shown below:
<b><i>terms0.txt/*</b></i>: Find scene(s) where the words thee or thou are used more frequently than the word you.
</pre>
Examples of input Queries:
<ul>
        <li>Find scene(s) where the place names venice, rome, or denmark are mentioned.</li>
        <li>Find the play(s) where the name goneril is mentioned.</li>
        <li>Find the play(s) where the word soldier is mentioned.</li>
        <li>Find scene(s) where "poor yorick" is mentioned.</li>
        <li>Find the scene(s) where "wherefore art thou romeo" is mentioned.</li>
        <li>Find the scene(s) where "let slip" is mentioned.</li>
</ul>
<p>
With these results obtained, we can move forward towards processing the queries.

To process the queries, the code consists of a general query-processing language for all types of input queries through which it should take very little effort to run minor variations on queries. Once it processes the queries, we find the result according to what is requested based on the information stored in the lists and return it as a txt file. When we retrieve plays, you return the "playId" and for scenes, we return the "sceneId" key.
</p>

# Building the Code:
To build the code, simply run the invertedIndex.py in the src folder to get the result of the query as inserted in the input.txt file:
<pre>
invertedIndex.py : Imports the required file(shakespeare-scenes.json) and builds a simple inverted index with positional information.
                   It does so by storing the data into two lists of the format:
                    (a) <i>self.sId_cnt</i>: {word: [[playId, sceneId, sceneNum, count], ....]}    
                         Stores the word information along with it's count in that text.

                    (b) <i>self.sId_loc</i>: {word: [[playId, sceneId, sceneNum, location], ....]}
                         Stores the word information along with it's location in that text.
</pre>
Input Format: An example scene looks like below:
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code> 

{
  "playId" : "antony_and_cleopatra",
  "sceneId" : "antony_and_cleopatra:2.8",
  "sceneNum" : 549 ,
  "text" : "scene ix another part of the plain enter mark antony and domitiu enobarbu mark antony
            set we our squadron on yond side o the hill in eye of caesar s battle from which place
            we may the number of the ship behold and so proceed accordingly exeunt "
}
</code></pre></div></div>
<div>
It consists of a general query-processing technique for all types of input queries. Once it processes the queries,
we find the result accoring to what is requested based on the information stored in the lists and return it as a txt file. 
</div>
   
# Running the Code:

The src file import the input text file and running the code will return the output file in the main directory. 
The query to be searched needs to be written in the input.txt file.
