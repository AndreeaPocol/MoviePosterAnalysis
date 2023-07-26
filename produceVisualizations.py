import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

titleTemplate = "Featured in the Posters of 50 Highest-Grossing Movies of All Time"

racesByGenre = {
    "Horror": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Romance": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Comedy": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Action": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Adventure": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Animation": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Crime": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Drama": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Sci-Fi": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Thriller": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Fantasy": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Family": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0}
}

gendersByGenre = {
    "Horror": {"Woman": 0, "Man": 0},
    "Romance": {"Woman": 0, "Man": 0},
    "Comedy": {"Woman": 0, "Man": 0},
    "Action": {"Woman": 0, "Man": 0},
    "Adventure": {"Woman": 0, "Man": 0},
    "Animation": {"Woman": 0, "Man": 0},
    "Crime": {"Woman": 0, "Man": 0},
    "Drama": {"Woman": 0, "Man": 0},
    "Sci-Fi": {"Woman": 0, "Man": 0},
    "Thriller": {"Woman": 0, "Man": 0},
    "Fantasy": {"Woman": 0, "Man": 0},
    "Family": {"Woman": 0, "Man": 0}
}

def processRaces(df):
    asians = df['asians'].sum()
    indians = df['indians'].sum()
    blacks = df['blacks'].sum()
    whites = df['whites'].sum()
    middleEasterns = df['middle-easterns'].sum()
    latinoHispanics = df['latino-hispanics'].sum()

    races = np.array([asians, indians, blacks, whites, middleEasterns, latinoHispanics])
    labels = ['Asian', 'Indian', 'Black', 'White', 'Middle-Eastern', 'Latino-Hispanic']

    fig, ax = plt.subplots()
    ax.pie(races, labels=labels)
    plt.title(f"Races {titleTemplate}", fontsize = 20, wrap=True)
    plt.tight_layout()
    # plt.show()
    plt.savefig('races.png')

def processGenders(df):
    men = df['men'].sum()
    women = df['women'].sum()

    genders = np.array([men, women])
    labels = ['Men', 'Women']

    fig, ax = plt.subplots()
    ax.pie(genders, labels=labels)
    plt.title(f"Genders {titleTemplate}", fontsize = 20, wrap=True)
    plt.tight_layout()
    # plt.show()
    plt.savefig('genders.png')

def processRacesByGenre(df):
    highestNumRaces = 0
    mostDiversePoster = 0

    for index, row in df.iterrows():
        movieGenres = row['genre'].split(",")

        asians = row['asians']
        indians = row['indians']
        blacks = row['blacks']
        whites = row['whites']
        middleEasterns = row['middle-easterns']
        latinoHispanics = row['latino-hispanics']

        races = np.array([asians, indians, blacks, whites, middleEasterns, latinoHispanics])
        numRaces = np.count_nonzero(races)
        if numRaces > highestNumRaces:
            highestNumRaces = numRaces
            mostDiversePoster = row['id']

        if whites == 0:
            print(f"No whites in {row['id']}")
            
        for genre in movieGenres:
            (racesByGenre[genre.strip()])['Asian'] += asians
            (racesByGenre[genre.strip()])['Indian'] += indians
            (racesByGenre[genre.strip()])['Black'] += blacks
            (racesByGenre[genre.strip()])['White'] += whites
            (racesByGenre[genre.strip()])['Middle-Eastern'] += middleEasterns
            (racesByGenre[genre.strip()])['Latino-Hispanic'] += latinoHispanics
    
    print(f"Most diverse poster: {mostDiversePoster}")

    for genre in racesByGenre.keys():
        print(f"Processing {genre}...")
        racesForGenre = racesByGenre[genre]

        raceLabels = []
        counts = []

        for race, count in racesForGenre.items():
            if count == 0:
                continue
            print(f"{race}: {count}")
            raceLabels.append(race)
            counts.append(count)

        if all(count == 0 for count in counts):
            continue

        fig, ax = plt.subplots()
        ax.pie(counts, labels=raceLabels)
        plt.title(f"Races in {genre}", fontsize = 20, wrap=True)
        plt.axis('equal')
        plt.savefig(f'{genre}-races.png')
        fig.clear()

def processGendersByGenre(df):
    for index, row in df.iterrows():
        movieGenres = row['genre'].split(",")

        men = row['men']
        women = row['women']
        if women > 0 and men == 0:
            print(f"Just women in {row['id']}")
            
        for genre in movieGenres:
            (gendersByGenre[genre.strip()])['Man'] += men
            (gendersByGenre[genre.strip()])['Woman'] += women
        
    for genre in gendersByGenre.keys():
        print(f"Processing {genre}...")
        gendersForGenre = gendersByGenre[genre]

        genderLabels = []
        counts = []

        for gender, count in gendersForGenre.items():
            if count == 0:
                continue
            print(f"{gender}: {count}")
            genderLabels.append(gender)
            counts.append(count)

        if all(count == 0 for count in counts):
            continue

        fig, ax = plt.subplots()
        ax.pie(counts, labels=genderLabels)
        plt.title(f"Genders in {genre}", fontsize = 20, wrap=True)
        plt.axis('equal')
        plt.savefig(f'{genre}-genders.png')
        fig.clear()


df = pd.read_csv('/Users/andreeapocol/Documents/Andreea/School/Graduate/CS 898 - Data Sources/Project/GLOBAL-diversity-dataset.csv')

processRaces(df)
processRacesByGenre(df)
processGenders(df)
processGendersByGenre(df)
    