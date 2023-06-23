# Movie Poster Diversity Analysis
## An assessment of the representation in top-grossing movie posters

I am using Deepface - a facial recognition system developed by Meta - to assess representation and diversity (e.g., age, gender, ethnicity) in movie posters, in the hopes of identifying trends across decades and genres. This can help answer questions like "how has female representation in movie posters changed over time? How does it differ across genres? How does it compare to male representation? Have movie posters become more inclusive of racial minorities, or is representation still lacking?"

Policymakers, social justice enthusiasts, the film industry, and other stakeholders want to know about diversity and representation in movie promotional material but don't have the data. One key promotional material is the movie poster. I can leverage Deepface to automatically analyze the age, gender, and ethnicity of all detectable humans in a movie poster, and then apply this analysis programmatically to a massive database of movie posters, in order to generate a novel `diversity dataset' that can be queried for trends. 



### Usage:

Simply supply the path to the folder containing the movie posters. 

```
python3 analyzeMoviePoster.py [path-to-image-folder]
```

### Example:

```
python3 analyzeMoviePoster.py "/Users/andreeapocol/Documents/Andreea/School/Graduate/CS 898 - Data Sources/Project/top-selling-movies/*.jpg"
```

### Output:
The program outputs three CSVs:
* ages.csv
* genders.csv
* races.csv

The left column is the classification and the right column is the count.

The program also prints a list of posters for which it was unable to detect at least one face.