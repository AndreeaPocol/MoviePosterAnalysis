import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

titleTemplate = "Featured in the Posters of 50 Highest-Grossing Movies of All Time"

racesByGenre = {
    "Horror": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Romance": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Comedy": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Action": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Animation": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Crime": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Drama": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Sci-Fi": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Thriller": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Fantasy": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Family": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0},
    "Adventure": {"Asian": 0, "Indian": 0, "Black": 0, "White": 0, "Middle-Eastern": 0, "Latino-Hispanic": 0}
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
    ax.pie(races)
    plt.title(f"Races {titleTemplate}", fontsize = 20, wrap=True)
    patches, texts = plt.pie(races, startangle=90)
    plt.legend(patches, labels, loc="lower center", prop={'size': 12})
    plt.tight_layout()
    # plt.show()
    plt.savefig('races.png')


def processGenders(df):
    men = df['men'].sum()
    women = df['women'].sum()

    genders = np.array([men, women])
    labels = ['Men', 'Women']

    fig, ax = plt.subplots()
    ax.pie(genders)
    plt.title(f"Genders {titleTemplate}", fontsize = 20, wrap=True)
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    patches, texts = plt.pie(genders, startangle=90, colors=colors)
    plt.legend(patches, labels, loc="best", prop={'size': 12})
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
        colors = {
            'White': 'yellowgreen', 
            'Asian': 'gold', 
            'Black': 'lightskyblue', 
            'Middle-Eastern': 'lightcoral',
            'Latino-Hispanic': 'purple'
        }
        
        patches, texts = ax.pie(counts, colors=[colors[v] for v in raceLabels])
        # plt.legend(patches, raceLabels, loc="lower center", prop={'size': 12})
        plt.title(f"Races in {genre}", fontsize = 20, wrap=True)
        plt.axis('equal')
        plt.savefig(f'{genre}-races.png')
        fig.clear()
    plt.legend(patches, raceLabels, loc="lower center", prop={'size': 12})
    plt.show()


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


def processGendersByYear(df):
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df = df.sort_values(by=['year'])
    years = []
    countsWomen = []
    countsMen = []
    for index, row in df.iterrows():
        men = row['men']
        women = row['women']
        year = row['year']
        if year in years:
            countsWomen[-1] += women
            countsMen[-1] += men
        else:
            years.append(year)
            countsWomen.append(women)
            countsMen.append(men)
    
    # pctWomen = []
    # for i in range(0, len(years)):
    #     pctWomen.append((countsWomen[i]/(countsWomen[i]+countsMen[i]))*100)
    
    plt.bar(years, countsWomen)
    plt.xlabel("Year", fontsize=14)
    plt.xticks(years, rotation=70)
    plt.ylabel("Number of Women", fontsize=12)
    plt.title(f"Number of Women {titleTemplate}", fontsize = 20, wrap=True)
    plt.savefig(f'num-women-by-year.png', bbox_inches='tight')


def main():
    diversityDatasetFile = ""

    if len(sys.argv) == 2:
        diversityDatasetFile = sys.argv[1]
    else:
        print(
            "Usage: {name} [ diversityDatasetFile ]".format(
                name=sys.argv[0]
            )
        )
        exit()

    df = pd.read_csv(diversityDatasetFile)

    # processRaces(df)
    # processRacesByGenre(df)
    # processGenders(df)
    # processGendersByGenre(df)
    processGendersByYear(df)

if __name__ == "__main__":
    main()
    