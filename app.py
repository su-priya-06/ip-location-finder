import requests
import folium
import tkinter as tk
from tkinter import messagebox
import webbrowser

# Function to get geolocation data from IP
def get_location():
    url = "http://ipinfo.io/json"  # Using ipinfo.io for IP geolocation
    response = requests.get(url)
    data = response.json()  # Convert the response to a JSON object
    return data

# Function to show the location on a map
def show_map(lat, lon, location_info):
    # Create a folium map centered around the provided latitude and longitude
    map = folium.Map(location=[lat, lon], zoom_start=12)
    
    # Format popup information to include city, ISP, and country
    popup_info = f"City: {location_info['city']}\nISP: {location_info['org']}\nCountry: {location_info['country']}"
    
    # Add a marker to the map at the specified location
    folium.Marker([lat, lon], popup=popup_info).add_to(map)
    
    # Save the map as an HTML file
    map.save("location_map.html")
    print("Map saved as 'location_map.html'")

# Function to fetch and display location info
def fetch_location():
    try:
        # Get location data from the API
        location = get_location()
        
        # Extract latitude and longitude from the location info
        lat, lon = location['loc'].split(',')
        lat, lon = float(lat), float(lon)
        
        # Update the labels with location info
        ip_label.config(text=f"IP: {location['ip']}")
        city_label.config(text=f"City: {location['city']}")
        country_label.config(text=f"Country: {location['country']}")
        isp_label.config(text=f"ISP: {location['org']}")
        
        # Show the location on a map
        show_map(lat, lon, location)
        
        # Show a message box confirming the map generation
        messagebox.showinfo("Success", "Location map generated successfully!")
        
        # Open the map in the browser automatically
        webbrowser.open("location_map.html")
    except Exception as e:
        # Show an error message if something goes wrong
        messagebox.showerror("Error", f"An error occurred: {e}")

# Creating the main window (GUI)
root = tk.Tk()
root.title("IP Location Finder")
root.geometry("400x300")

# Labels to display IP, city, country, and ISP
ip_label = tk.Label(root, text="IP: ", font=("Arial", 12))
ip_label.pack(pady=10)

city_label = tk.Label(root, text="City: ", font=("Arial", 12))
city_label.pack(pady=10)

country_label = tk.Label(root, text="Country: ", font=("Arial", 12))
country_label.pack(pady=10)

isp_label = tk.Label(root, text="ISP: ", font=("Arial", 12))
isp_label.pack(pady=10)

# Button to fetch location data
fetch_button = tk.Button(root, text="Find My Location", font=("Arial", 14), command=fetch_location)
fetch_button.pack(pady=20)

# Run the GUI event loop
root.mainloop()
