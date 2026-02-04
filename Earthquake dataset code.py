# Montle Segomotso 202107060
# Import necessary libraries
import pandas as pd  
import matplotlib.pyplot as plt

# Reading the earthquake data from the attached CSV file
file_path = r"C:\Users\202107060\Downloads\earthquake_data.csv"

def earthquake_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data[['Location', 'Magnitude']]
    except Exception as e:
        print(f"Error reading file: {e}")
        return None       
              
           
# Creating earthquake magnitude intensity into classes dictionary
def magnitude_class(data):
    magnitude_category = {
        'Minor': [],
        'Light': [],
        'Moderate': [],
        'Strong': [],
        'Major': []
    }
    
    for _, row in data.iterrows():  
        magnitude = row['Magnitude']  
        location = row['Location']  
        
        if magnitude < 4:
            magnitude_category['Minor'].append((location, magnitude))  
        elif 4 <= magnitude < 5:
            magnitude_category['Light'].append((location, magnitude))
        elif 5 <= magnitude < 6:
            magnitude_category['Moderate'].append((location, magnitude))
        elif 6 <= magnitude < 7:
            magnitude_category['Strong'].append((location, magnitude))
        else:
            magnitude_category['Major'].append((location, magnitude))
    
    return magnitude_category

# Displaying total count of the number of earthquakes in each magnitude category
def total_count(magnitude_category):  
    for category, events in magnitude_category.items():  
        print(f"Magnitude category {category}: {len(events)}")  

# Display of the earthquake magnitude distribution via a histogram
def display_histogram(magnitude_category):
    count = [len(events) for events in magnitude_category.values()]  
    labels = list(magnitude_category.keys())  
    
    # Histogram 2D Plot
    plt.bar(labels, count, color=['blue'])
    plt.title('Earthquake Distribution')
    plt.xlabel('Magnitude Category')
    plt.ylabel('Number of Earthquakes')
    plt.grid(axis='y', linestyle='--')  
    plt.show()

# Search function 
def earthquake_search(magnitude_category):
    print("Select search choice:")
    print("1. Location")
    print("2. Magnitude")
    print("3. Exit")
    
    while True:
        search_choice = input("Enter search choice (1/2/3): ")

        if search_choice == '3':
            print("Exiting search bar!")
            break

        elif search_choice == '2':  
            try:
                Magnitude = float(input("Enter earthquake magnitude between 4.0 and 8.0: "))
                Magnitude_lowerbound = Magnitude * 0.9
                Magnitude_upperbound = Magnitude * 1.1
                output_results = []

                for category, events in magnitude_category.items():  
                    for loc, mag in events:  
                        if Magnitude_lowerbound <= mag <= Magnitude_upperbound:
                            output_results.append((loc, mag))
                if output_results:
                    print(f"Earthquakes within ±10% of {Magnitude}:")
                    for loc, mag in output_results:
                        print(f"Location: {loc}, Magnitude: {mag}")
                else:
                    print("No earthquakes found in this magnitude range.")
            except ValueError:
                print("Invalid input! Please enter numeric values.")
                continue

        elif search_choice == '1':  
            Location = input("Enter location: ")
            output_results = []
            for events in magnitude_category.values():
                for loc, mag in events:
                    if Location.lower() in loc.lower():  
                        output_results.append((loc, mag))
            if output_results:
                print(f"Earthquakes in {Location}:")
                for loc, mag in output_results:
                    print(f"Location: {loc}, Magnitude: {mag}")
            else:
                print("No earthquakes found in this location.")
        else:
            print("Invalid search choice, choose 1 or 2")

if __name__ == "__main__":
    file_path = r"C:\Users\202107060\Downloads\earthquake_data.csv"
    data = earthquake_data(file_path)  

    if data is not None:
        category = magnitude_class(data)  
        total_count(category)
        display_histogram(category)
        earthquake_search(category)  
