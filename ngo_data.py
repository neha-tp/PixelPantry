from pymongo import MongoClient

# Connect to the MongoDB client
client = MongoClient("mongodb://localhost:27017/")  # Use your MongoDB connection URL
db = client["Pixelpantry"]  # Use your database name

# Access the 'Ngo' collection
ngo_collection = db["Ngo"]

# NGO data
ngo_data = [
    {
        "ngo_id": "ngo_001",
        "name": "Farmers Relief NGO",
        "contact": "contact@farmersrelief.org",
        "location": {"latitude": 28.7041, "longitude": 77.1025},
    },
    {
        "ngo_id": "ngo_002",
        "name": "Green Earth NGO",
        "contact": "info@greenearth.org",
        "location": {"latitude": 28.7040, "longitude": 77.1000},
    },
    {
        "ngo_id": "ngo_003",
        "name": "Farmers Support Foundation",
        "contact": "farmersupport@ngo.org",
        "location": {"latitude": 23.0224, "longitude": 72.5710},
    },
    {
        "ngo_id": "ngo_004",
        "name": "Green Gujarat NGO",
        "contact": "info@greengujarat.org",
        "location": {"latitude": 23.0225, "longitude": 72.5709},
    },
    {
        "ngo_id": "ngo_005",
        "name": "Sustainable Agriculture NGO",
        "contact": "support@sustainableagriculture.org",
        "location": {"latitude": 26.8450, "longitude": 80.9480},
    },
    {
        "ngo_id": "ngo_006",
        "name": "Lucknow Farmers NGO",
        "contact": "info@lucknowfarmers.org",
        "location": {"latitude": 26.8470, "longitude": 80.9450},
    },
    {
        "ngo_id": "ngo_007",
        "name": "Green Mumbai Foundation",
        "contact": "info@greenmumbai.org",
        "location": {"latitude": 19.0750, "longitude": 72.8760},
    },
    {
        "ngo_id": "ngo_008",
        "name": "Mumbai Farmers Relief",
        "contact": "contact@mumbaifarmersrelief.org",
        "location": {"latitude": 19.0770, "longitude": 72.8780},
    },
    {
        "ngo_id": "ngo_009",
        "name": "Goa Agriculture NGO",
        "contact": "support@goaagriculture.org",
        "location": {"latitude": 15.3000, "longitude": 74.1250},
    },
    {
        "ngo_id": "ngo_010",
        "name": "Goa Green Foundation",
        "contact": "info@goagreen.org",
        "location": {"latitude": 15.2980, "longitude": 74.1220},
    },
    {
        "ngo_id": "ngo_011",
        "name": "Farmers Welfare Foundation",
        "contact": "farmerswelfare@delhi.org",
        "location": {"latitude": 28.6140, "longitude": 77.2100},
    },
    {
        "ngo_id": "ngo_012",
        "name": "Earth Care Foundation",
        "contact": "contact@earthcare.org",
        "location": {"latitude": 28.6150, "longitude": 77.2080},
    },
    {
        "ngo_id": "ngo_013",
        "name": "Farmers Support NGO",
        "contact": "support@farmerssupportchandigarh.org",
        "location": {"latitude": 30.7350, "longitude": 76.7770},
    },
    {
        "ngo_id": "ngo_014",
        "name": "Kolkata Agriculture Welfare",
        "contact": "contact@kolkataagriwelfare.org",
        "location": {"latitude": 22.5730, "longitude": 88.3620},
    },
    {
        "ngo_id": "ngo_015",
        "name": "West Bengal Farmers Relief",
        "contact": "support@wbfarmersrelief.org",
        "location": {"latitude": 22.5710, "longitude": 88.3650},
    },
    {
        "ngo_id": "ngo_016",
        "name": "Jaipur Farmers NGO",
        "contact": "contact@jaipurfarmers.org",
        "location": {"latitude": 26.9130, "longitude": 75.7860},
    },
    {
        "ngo_id": "ngo_017",
        "name": "Sustainable Rajasthan NGO",
        "contact": "info@sustainablerajasthan.org",
        "location": {"latitude": 26.9140, "longitude": 75.7880},
    }
]

# Insert NGO data into the collection
ngo_collection.insert_many(ngo_data)

print("NGO data inserted successfully!")
