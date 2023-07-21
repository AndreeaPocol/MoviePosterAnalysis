# Movie Poster Diversity Analysis
## An assessment of the representation in top-grossing movie posters

I am using Deepface - a facial recognition system developed by Meta - to assess representation and diversity (e.g., age, gender, ethnicity) in movie posters, in the hopes of identifying trends across decades and genres. This can help answer questions like "how has female representation in movie posters changed over time? How does it differ across genres? How does it compare to male representation? Have movie posters become more inclusive of racial minorities, or is representation still lacking?"

Policymakers, social justice enthusiasts, the film industry, and other stakeholders want to know about diversity and representation in movie promotional material but don't have the data. One key promotional material is the movie poster. I can leverage Deepface to automatically analyze the age, gender, and ethnicity of all detectable humans in a movie poster, and then apply this analysis programmatically to a massive database of movie posters, in order to generate a novel `diversity dataset' that can be queried for trends. 


### Overview:

![workflow](workflow.png "Workflow")

### 1.  `obtainMovieTconsts.py`

#### Usage:
Ensure `title.basics.tsv` has been downloaded from [the IMDb data store](https://datasets.imdbws.com/) and exists in the script directory. 

#### Example:
```
python3 obtainMovieTconsts.py
```

#### Output:
The program outputs a list of tconsts in `tconsts.txt`.

### 2. `downloadMovieMetadata.py`

#### Usage:
Ensure `tconsts.txt` exists in the script directory.

#### Example:
```
python3 downloadMovieMetadata.py
```

#### Output:
The program outputs 
- `omdb_movies.json`
- `problematic_tconsts.txt`

### 3. `downloadMoviePosters.py`

#### Usage:

```
python3 downloadMoviePosters.py [ movieFile downloadFolder]
```

#### Example:

```
python3 downloadMoviePosters.py omdb_movies.json posters
```

#### Output:
Movie posters are saved to the specified download folder.


### 4. `analyzeMoviePosters.py`

#### Usage:

Supply the path to the folder containing the movie posters. 

```
python3 analyzeMoviePoster.py [path-to-image-folder]
```

#### Example:

```
python3 analyzeMoviePoster.py movies
```

#### Output:
The program outputs three CSVs:
* `ages.csv`
* `genders.csv`
* `races.csv`

The left column is the classification and the right column is the count.

The program also prints a list of posters for which it was unable to detect at least one face.